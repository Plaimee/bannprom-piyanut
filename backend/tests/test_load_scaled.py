"""AC-07-08 แบบย่อส่วน (T-09) ย่อจากผู้ใช้ 500 คน เป็น 20 คำขอพร้อมกัน (บันทึกใน ac-results.md)
ฉบับวัดได้จริงรอ CR-02 (quality-requirements.md) ผลบนเครื่องนักศึกษาเป็นเพียงสัญญาณ ไม่ใช่ผลตรวจรับจริง"""
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import session as db_session
from app.db.migrations.m001_init import upgrade
from app.db.models import Customer, ServiceAddress, Technician, TimeSlot
from tests.conftest import NOW


@pytest.fixture()
def scaled_client(tmp_path, monkeypatch):
    # REQ-QA-003: ใช้ฐานข้อมูลไฟล์เพื่อให้แต่ละ request thread ได้ connection แยกกัน
    engine = create_engine(
        f"sqlite:///{tmp_path / 'scaled-load.db'}",
        connect_args={"check_same_thread": False},
        pool_size=20,
        max_overflow=0,
    )
    upgrade(engine)
    test_sessions = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    monkeypatch.setattr(db_session, "SessionLocal", test_sessions)

    from app import main

    monkeypatch.setattr(main, "engine", engine)
    with test_sessions() as db:
        customer = Customer(name="ผู้ทดสอบ", phone="000")
        db.add(customer)
        db.flush()
        address = ServiceAddress(
            customer_id=customer.id,
            text="ที่อยู่ทดสอบ",
            lat=13.7400,
            lng=100.5300,
        )
        technician = Technician(
            name="ช่างทดสอบ",
            skills="ประปา",
            base_lat=13.7050,
            base_lng=100.5300,
        )
        db.add_all([address, technician])
        db.flush()
        start = (NOW + timedelta(days=1)).replace(hour=14, minute=0)
        slot = TimeSlot(
            technician_id=technician.id,
            start=start,
            end=start + timedelta(hours=2),
        )
        db.add(slot)
        db.commit()
        address_id, technician_id, slot_id = address.id, technician.id, slot.id

    try:
        with TestClient(main.app) as client:
            yield client, address_id, technician_id, slot_id
    finally:
        engine.dispose()


# รองรับ AC-07-08 (REQ-QA-003) ฉบับย่อส่วน
def test_AC_07_08_search_under_load_scaled(scaled_client):
    client, address_id, technician_id, slot_id = scaled_client
    url = f"/technicians?category=ประปา&address_id={address_id}&now={NOW.isoformat()}"
    expected = [{
        "technician_id": technician_id,
        "name": "ช่างทดสอบ",
        "slots": [{
            "slot_id": slot_id,
            "start": ((NOW + timedelta(days=1)).replace(hour=14, minute=0)).isoformat(),
            "end": ((NOW + timedelta(days=1)).replace(hour=16, minute=0)).isoformat(),
        }],
    }]

    def timed_get(_):
        t0 = time.perf_counter()
        response = client.get(url)
        return response.status_code == 200, response.json(), time.perf_counter() - t0

    # Given ลูกค้า 20 คน (ย่อจาก 500) ส่งคำขอค้นหาช่างพร้อมกัน
    with ThreadPoolExecutor(max_workers=20) as pool:
        results = list(pool.map(timed_get, range(20)))
    # Then ทุกคำขอได้รายการช่างครบ
    assert all(ok and technicians == expected for ok, technicians, _ in results)
    # Then 19 ใน 20 (ย่อจาก 95 ใน 100) ใช้เวลาไม่เกิน 2 วินาที
    fast = [elapsed for _, _, elapsed in results if elapsed <= 2.0]
    assert len(fast) >= 19

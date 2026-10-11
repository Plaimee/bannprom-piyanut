"""AC-07-01, AC-07-02, AC-07-03, AC-07-04 จาก booking.feature (T-03, T-04, T-07)"""
from datetime import datetime, timedelta

from sqlalchemy import select

from app.db.models import Job, Payment, TimeSlot
from app.notify.queue import queue
from tests.conftest import NOW, TOMORROW_14, book


# รองรับ AC-07-01 (REQ-FN-008)
def test_AC_07_01_booking_success(client, db, seed, gateway):
    # Given ลูกค้าล็อกช่วงเวลา พรุ่งนี้ 14:00-16:00 ของช่าง ประสิทธิ์ ไว้
    r = client.post(f"/slots/{seed['slot'].id}/hold?now={NOW.isoformat()}", json={"customer_id": seed["somchai"].id})
    assert r.status_code == 200
    # When ลูกค้ากดยืนยัน และ Payment Gateway ตอบ approved
    gateway.mode = "approved"
    res = book(client, customer_id=seed["somchai"].id, slot_id=seed["slot"].id, address_id=seed["addr"].id)
    # Then มีงาน 1 รายการสถานะ ยืนยันแล้ว ของช่าง ประสิทธิ์
    assert res.status_code == 201, res.text
    job = db.get(Job, res.json()["job_id"])
    db.refresh(job)
    assert job.status == "confirmed" and job.technician_id == seed["prasit"].id
    # And ช่วงเวลานั้นมีสถานะ จองแล้ว
    db.refresh(seed["slot"])
    assert seed["slot"].state == "booked"
    # And มีรายการชำระมัดจำ 1 รายการเท่านั้น (GAP-06: เพิ่ม assert นี้หลังพบว่า test เดิมผ่านแม้ตัดเงินซ้ำ)
    assert db.scalar(select(Payment).where(Payment.job_id == job.id, Payment.result == "success")) is not None
    assert len(db.scalars(select(Payment).where(Payment.job_id == job.id)).all()) == 1


# รองรับ REQ-FN-008 และ REQ-FN-041: slot เดิมสร้างงานและชำระซ้ำไม่ได้
def test_AC_07_01_cannot_book_same_slot_twice(client, db, seed, gateway):
    slot = seed["slot"]
    held = client.post(
        f"/slots/{slot.id}/hold?now={NOW.isoformat()}",
        json={"customer_id": seed["somchai"].id},
    )
    assert held.status_code == 200

    first = book(
        client,
        customer_id=seed["somchai"].id,
        slot_id=slot.id,
        address_id=seed["addr"].id,
    )
    assert first.status_code == 201
    assert len(db.scalars(select(Job).where(Job.slot_id == slot.id)).all()) == 1
    assert len(db.scalars(select(Payment)).all()) == 1

    gateway.calls.clear()
    second = book(
        client,
        customer_id=seed["somchai"].id,
        slot_id=slot.id,
        address_id=seed["addr"].id,
    )
    assert second.status_code == 409
    assert second.json()["reason"] == "slot_taken"
    assert not gateway.calls
    assert len(db.scalars(select(Job).where(Job.slot_id == slot.id)).all()) == 1
    assert len(db.scalars(select(Payment)).all()) == 1


# รองรับ AC-07-02 (REQ-FN-008, BR-02)
def test_AC_07_02_slot_not_rebookable(client, db, seed):
    # Given ช่วงเวลา พรุ่งนี้ 14:00-16:00 ของช่าง ประสิทธิ์ มีสถานะ จองแล้ว
    res = book(client, customer_id=seed["somchai"].id, slot_id=seed["slot"].id, address_id=seed["addr"].id)
    assert res.status_code == 201
    # When ลูกค้าอีกคนค้นหาช่าง ประปา ที่ที่อยู่เดียวกัน
    r = client.get(f"/technicians?category=ประปา&address_id={seed['addr'].id}&customer_id={seed['other'].id}&now={NOW.isoformat()}")
    assert r.status_code == 200
    # Then ผลค้นหาไม่มีช่วงเวลา พรุ่งนี้ 14:00-16:00 ของช่าง ประสิทธิ์ (และไม่มีช่าง ไกลมาก ตาม BR-03)
    offered = {(t["technician_id"], s["slot_id"]) for t in r.json() for s in t["slots"]}
    assert (seed["prasit"].id, seed["slot"].id) not in offered
    offered_technicians = {t["technician_id"] for t in r.json()}
    assert seed["prasit"].id in offered_technicians
    assert seed["far"].id not in offered_technicians
    assert len(offered) >= 1  # ช่วงอื่นของ ประสิทธิ์ ยังถูกเสนอ


# รองรับ REQ-FN-041 (Q-18): ล็อก 10 นาทีและล็อกซ้ำได้หลังหมดอายุเท่านั้น
def test_AC_07_04_hold_expires_before_relock(client, db, seed):
    slot = seed["slot"]
    first_hold = client.post(
        f"/slots/{slot.id}/hold?now={NOW.isoformat()}",
        json={"customer_id": seed["somchai"].id},
    )
    assert first_hold.status_code == 200
    expires_at = datetime.fromisoformat(first_hold.json()["hold_expires_at"])
    assert expires_at == NOW + timedelta(minutes=10)

    before_expiry = NOW + timedelta(minutes=9)
    renewed_early = client.post(
        f"/slots/{slot.id}/hold?now={before_expiry.isoformat()}",
        json={"customer_id": seed["somchai"].id},
    )
    assert renewed_early.status_code == 409
    assert renewed_early.json()["reason"] == "slot_taken"
    db.refresh(slot)
    assert slot.held_by_customer_id == seed["somchai"].id
    assert slot.hold_expires_at == expires_at

    at_expiry = client.post(
        f"/slots/{slot.id}/hold?now={expires_at.isoformat()}",
        json={"customer_id": seed["other"].id},
    )
    assert at_expiry.status_code == 200
    db.refresh(slot)
    assert slot.held_by_customer_id == seed["other"].id
    assert slot.hold_expires_at == expires_at + timedelta(minutes=10)


# รองรับ AC-07-03 (REQ-FN-012)
def test_AC_07_03_notify_both_within_60s(client, db, seed):
    # Given ลูกค้าจองสำเร็จ
    res = book(client, customer_id=seed["somchai"].id, slot_id=seed["slot"].id, address_id=seed["addr"].id)
    assert res.status_code == 201
    job_id = res.json()["job_id"]
    job = db.get(Job, job_id)
    db.refresh(job)
    # When ระบบสร้างงานสถานะ ยืนยันแล้ว
    assert job.status == "confirmed"
    msgs = queue.for_job(job_id)
    # Then มีข้อความถึงลูกค้า 1 ข้อความ และถึงช่าง 1 ข้อความ อยู่ในคิวส่ง
    assert len(msgs) == 2
    assert sorted(m.to_role for m in msgs) == ["customer", "technician"]
    assert {m.to_id for m in msgs if m.to_role == "customer"} == {seed["somchai"].id}
    assert {m.to_id for m in msgs if m.to_role == "technician"} == {seed["prasit"].id}
    # And ทั้งสองข้อความมีกำหนดส่งภายใน 60 วินาทีนับจากเวลาสร้างงาน
    assert all(m.created_at == job.created_at for m in msgs)
    assert all(m.due_at <= job.created_at + timedelta(seconds=60) for m in msgs)
    queued = client.get("/notifications/queue")
    assert queued.status_code == 200
    exposed_msgs = [msg for msg in queued.json() if msg["job_id"] == job_id]
    assert len(exposed_msgs) == 2
    assert {msg["to_role"] for msg in exposed_msgs} == {"customer", "technician"}
    assert all(
        datetime.fromisoformat(msg["due_at"]) <= job.created_at + timedelta(seconds=60)
        for msg in exposed_msgs
    )


# รองรับ AC-07-04 (REQ-FN-041, UC-07 E2, CR-01)
def test_AC_07_04_no_charge_when_slot_taken(client, db, seed, gateway):
    slot = seed["slot"]
    # Given ลูกค้า สมชาย เลือกช่วงเวลา 14:00-16:00 ของช่าง ประสิทธิ์ (ล็อกไว้แล้วแต่ล็อกหมดอายุ)
    client.post(f"/slots/{slot.id}/hold?now={NOW.isoformat()}", json={"customer_id": seed["somchai"].id})
    # And ลูกค้า คนอื่น จองช่วงเวลานั้นสำเร็จไปก่อน (หลังล็อกของสมชายหมดอายุ 10 นาที)
    later = NOW + timedelta(minutes=11)
    res_other = book(client, customer_id=seed["other"].id, slot_id=slot.id, address_id=seed["addr_other"].id, now=later)
    assert res_other.status_code == 201
    gateway.calls.clear()
    # When ลูกค้า สมชาย กดยืนยัน
    res = book(client, customer_id=seed["somchai"].id, slot_id=slot.id, address_id=seed["addr"].id, now=later + timedelta(minutes=1))
    # Then ไม่มีรายการตัดเงินของ สมชาย
    jobs_of_somchai = db.scalars(select(Job).where(Job.customer_id == seed["somchai"].id)).all()
    assert jobs_of_somchai == []
    assert not any(c.startswith("authorize") for c in gateway.calls)
    # And ระบบแจ้งว่าช่วงเวลาถูกจองแล้ว
    assert res.status_code == 409 and res.json()["reason"] == "slot_taken"
    # And ระบบเสนอช่วงเวลาที่ว่างอย่างน้อย 2 ตัวเลือก ซึ่งเริ่มห่างจากเวลาที่เลือกไม่เกิน 3 ชั่วโมง (CR-01)
    alts = res.json()["alternatives"]
    assert len(alts) >= 2
    for a in alts:
        gap = abs((datetime.fromisoformat(a["start"]) - TOMORROW_14).total_seconds()) / 3600
        assert gap <= 3

# Tasks: การจองงานบริการซ่อมบำรุง (UC-07)

Feature: SPEC-BOOKING | Spec ID: SPEC-BOOKING | อ้างอิง: plan.md (plan v1) | วันที่: 2569-10-04
สรุป: 10 task | 5 task รอ Q-xx

## รายการ task

### T-01 ตั้งโครงโปรเจกต์และฐานข้อมูล
- รองรับ: REQ-DAT-002, REQ-PRV-002, REQ-CON-001
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-02 ถึง T-10
- ไฟล์ที่แตะ: backend/requirements.txt, backend/pytest.ini, backend/app/config.py, backend/app/db/session.py, backend/app/db/models.py, backend/app/db/migrations/m001_init.py, backend/app/main.py, backend/tests/conftest.py, frontend/package.json, frontend/vite.config.js
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: pytest และ npm test รันได้ และ upgrade(engine) สร้างตารางหลักและสถานะงานตาม MD-STM-01 ได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 ค้นช่างว่างตามประเภทงาน/ที่อยู่/ระยะทาง
- รองรับ: REQ-FN-008, BR-02, BR-03, AS-06
- ตรวจด้วย: AC-07-02
- ไฟล์ที่แตะ: backend/app/technicians/service.py, backend/app/technicians/router.py, backend/app/clock.py, backend/tests/test_booking.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: test_AC_07_02 ผ่าน โดยแสดงเฉพาะช่างที่ว่างและอยู่ในระดับ 15 กิโลเมตรตาม BR-03
- สถานะ: เสร็จ รอทีมตรวจ

### T-03 ล็อกช่วงเวลาและหมดอายุอัตโนมัติ
- รองรับ: REQ-FN-041, AS-07, BR-02
- ตรวจด้วย: AC-07-04
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py, backend/app/technicians/service.py, backend/tests/test_booking.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: POST /slots/{id}/hold ให้ hold_expires_at = now + HOLD_MINUTES และระบบยอมให้ล็อกซ้ำได้เฉพาะเมื่อครบกำหนดเวลา
- สถานะ: เสร็จ รอทีมตรวจ

### T-04 สร้างงานยืนยันแล้วจากการจอง
- รองรับ: REQ-FN-008, REQ-FN-041, REQ-IF-001, REQ-CON-003
- ตรวจด้วย: AC-07-01, AC-07-04
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/booking/router.py, backend/app/payments/gateway.py, backend/app/payments/service.py, backend/tests/test_booking.py
- ต้องทำหลัง: T-02, T-03
- เสร็จเมื่อ: test_AC_07_01 และ test_AC_07_04 สำหรับ path จองสำเร็จผ่าน และระบบไม่ยอมสร้างงานซ้ำบน slot เดียวกัน
- สถานะ: เสร็จ รอทีมตรวจ

### T-05 ชำระมัดจำและตรวจสถานะ gateway
- รองรับ: REQ-IF-001, REQ-IF-005, REQ-CON-003
- ตรวจด้วย: AC-07-05, AC-07-06, AC-07-07
- ไฟล์ที่แตะ: backend/app/payments/service.py, backend/app/payments/gateway.py, backend/tests/test_payment.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: authorize แบบครั้งเดียว, capture หลังยืนยัน, และเมื่อ gateway timeout ใช้ status inquiry ด้วย reference เดิมตามเงื่อนไขชั่วคราว
- สถานะ: เสร็จ รอทีมตรวจ

### T-06 ส่งข้อความแจ้งให้ลูกค้าและช่างภายใน 60 วินาที
- รองรับ: REQ-FN-012, IF-02
- ตรวจด้วย: AC-07-03
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py, backend/app/main.py, backend/tests/test_booking.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: test_AC_07_03 ผ่าน และข้อความถูกส่งไปสองฝ่ายภายใน 60 วินาทีหลังสร้างงาน
- สถานะ: เสร็จ รอทีมตรวจ

### T-07 คืนมัดจำตาม BR-01
- รองรับ: REQ-BR-001, BR-01, MD-STM-01
- ตรวจด้วย: AC-07-10
- ไฟล์ที่แตะ: backend/app/refund/rules.py, backend/app/refund/service.py, backend/app/refund/router.py, backend/tests/test_refund.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: BR-01 R1, R2, R4, R5, R6 ผ่าน และ R3 ใช้พฤติกรรมชั่วคราวตาม D-07-04 จนกว่าจะมีคำตอบจาก Q-14
- สถานะ: เสร็จ รอทีมตรวจ (R3 ใช้พฤติกรรมชั่วคราวตาม D-07-04; Q-14 ยังเปิด)

### T-08 ซ่อนเบอร์ลูกค้าและป้องกัน log รั่ว
- รองรับ: REQ-SEC-004, REQ-PRV-002
- ตรวจด้วย: AC-07-09
- ไฟล์ที่แตะ: backend/app/privacy.py, backend/app/booking/service.py, backend/app/booking/router.py, backend/tests/test_privacy.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: ช่างเห็นเบอร์ได้เฉพาะ 2 ชั่วโมงก่อนนัดจนถึงปิดงาน และ log ไม่มีค่า phone
- สถานะ: เสร็จ รอทีมตรวจ

### T-09 ทดสอบประสิทธิภาพสำหรับ AC-07-08
- รองรับ: REQ-QA-003
- ตรวจด้วย: AC-07-08
- ไฟล์ที่แตะ: backend/tests/test_load_scaled.py, specs/002-booking/quality-requirements.md, specs/002-booking/ac-results.md
- ต้องทำหลัง: T-02, T-04
- เสร็จเมื่อ: ตามสมมติฐาน CR-02, test_AC_07_08_search_under_load_scaled ส่ง 20 คำขอ GET /technicians พร้อมกัน ตรวจผลลัพธ์ครบทุกคำขอ และอย่างน้อย 19/20 ตอบภายใน 2 วินาที; รายงานชัดเจนว่าเป็นการทดสอบย่อส่วน ไม่ใช่ผลจริง 500 คำขอ
- สถานะ: เสร็จ รอทีมตรวจ (ใช้สมมติฐาน CR-02 ตามคำสั่งทีม; ผลจริง 500 คำขอและการอนุมัติ SH-01 ยังรอ)

### T-10 หน้าจอเลือกช่างและยืนยันการจอง
- รองรับ: REQ-FN-008, REQ-FN-041
- ตรวจด้วย: AC-07-04 (หน้าจอ)
- ไฟล์ที่แตะ: frontend/src/App.jsx, frontend/src/api/client.js, frontend/src/pages/TechnicianPicker.jsx, frontend/src/pages/ConfirmBooking.jsx, frontend/src/pages/BookingResult.jsx, frontend/src/__tests__/AC-07-04.test.jsx
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: UI แสดงช่างที่ว่างและช่วงเวลาให้เลือก, ถ้าช่วงถูกล็อกแล้วให้แสดง 409/ข้อความช่วงใกล้เคียง และผู้ใช้สามารถยืนยันการจองได้
- สถานะ: เสร็จ รอทีมตรวจ

## ตารางตรวจความครบ

### 1) AC ID | task ที่ตรวจ AC นี้
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-07-01 | T-04 |
| AC-07-02 | T-02 |
| AC-07-03 | T-06 |
| AC-07-04 | T-03, T-04, T-10 |
| AC-07-05 | T-05 |
| AC-07-06 | T-05 |
| AC-07-07 | T-05 |
| AC-07-08 | T-09 |
| AC-07-09 | T-08 |
| AC-07-10 | T-07 |

### 2) Constraint ID | task ที่ทำให้เป็นจริง
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| REQ-CON-001 | T-01 |
| REQ-CON-003 | T-04, T-05 |

## สิ่งที่ยังไม่ทำ
- Q-14: BR-01 R3 ควรคืนเงินเท่าไรและยกเลิกได้หรือไม่ | รอ T-07
- Q-18: ระยะล็อก 10 นาทีเป็นลายลักษณ์อักษรหรือไม่ | รอ T-03
- Q-22: ServiceAddress.geoPoint ต้องเป็น PII หรือไม่ | รอ T-08
- Q-23: ถ้าลูกค้าปิดเบราว์เซอร์ระหว่างล็อก ใครปลดล็อก | รอ T-03, T-04ญา API ใน plan.md ข้อ 4)- เสร็จเมื่อ: npm test ผ่าน AC-07-04.test.jsx
- สถานะ: เสร็จ

### T-11 ต่อหน้าจอกับ API จริง
- รองรับ: REQ-FN-008
- ตรวจด้วย: ไม่มี AC ตรง ๆ ตรวจด้วยตา: npm run dev + uvicorn แล้วจองได้จนเห็นหน้าผลการจอง
- ไฟล์ที่แตะ: frontend/vite.config.js (proxy /api), backend/seed_demo.py
- ต้องทำหลัง: T-03, T-04, T-05, T-10
- เสร็จเมื่อ: กดค้นหา เลือกช่วงเวลา ยืนยัน แล้วเห็น "งาน #1 สถานะ ยืนยันแล้ว" บนหน้าจอ
- สถานะ: เสร็จ

## ตารางตรวจความครบ

| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-07-01 | T-04 |
| AC-07-02 | T-03 |
| AC-07-03 | T-07 |
| AC-07-04 | T-02, T-04, T-10 (หน้าจอ) |
| AC-07-05 | T-05 |
| AC-07-06 | T-05 |
| AC-07-07 | T-05 |
| AC-07-08 | T-09 (ย่อส่วน รอ CR-02) |
| AC-07-09 | T-08 |
| AC-07-10 | T-06 (R3 รอ Q-14) |

| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| REQ-CON-003 | T-04 (interface Gateway ไม่เปลี่ยนราย) |
| REQ-CON-001 | ทุก task ตัด A2 ออก (D-07-02) |
| REQ-PRV-002 | T-01 (ไม่มีตาราง log), T-08 (privacy.py) |
| REQ-SEC-004 | T-08 |
| REQ-IF-001 | T-04 |
| REQ-IF-005 | T-05 |
| REQ-DAT-002 | T-01 |

## สิ่งที่ยังไม่ทำ

- Q-14 BR-01 R3: T-06 ทำแถวอื่นแล้ว R3 ใช้พฤติกรรมชั่วคราว "ไม่อนุญาต" รอคำตอบ 11 ต.ค.
- Q-18 ระยะล็อก: ทำเป็น config HOLD_MINUTES = 10 ถ้าคำตอบต่าง แก้ config
- Q-19 ทีมยืนยัน gateway-timeout = 30 วินาที; ตรวจสัญญาจริงต่อใน GAP-07
- Q-22 geoPoint: เก็บแต่ไม่ส่งออก ยังไม่มี task เพราะไม่มี REQ รองรับ
- Q-23 ใครปลดล็อก: ใช้ AS-07 หมดอายุเอง (T-02) รอกลุ่มยืนยันกับเจ้าของ

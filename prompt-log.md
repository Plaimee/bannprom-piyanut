# prompt-log.md บันทึกการใช้ AI ของกลุ่ม X

กติกา: เพิ่มต่อท้ายเท่านั้น ห้ามแก้หรือลบบันทึกเดิม ทุกบันทึกมี เลขที่ | วันที่ | เครื่องมือ | คำสั่ง | สิ่งที่ AI ถามหรือรายงาน | คำตอบหรือการตัดสินใจของทีม | สิ่งที่ AI เดา (ถ้ามี)
บันทึก #1 ถึง #19 อยู่ในบทเรียนก่อนหน้า (ร่าง spec v1, matrix, baseline) คัดเฉพาะหัวข้อไว้ตอนต้น

## บันทึกจากบทเรียนก่อนหน้า (สรุป)

- #12 ถึง #15 (6 ก.ย.) ร่าง spec ส่วน 4 ถึง 6 จาก UC-07 + catalogue ด้วย prompt "บรรณาธิการสเปก" AI เดา 2 อย่างแล้วถูกตัด: ระยะล็อก 15 นาที, สถานะ "รอรีวิว"
- #16 ถึง #19 (6 ก.ย.) ร่างโครง RTM และ Baseline B1 ทีมตรวจและลงชื่อ

## #20 | 4 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /clarify specs/002-booking/spec.md

AI รายงาน 3 ส่วน
A จุดที่กำกวม (7 ข้อ)
1. REQ-FN-041 "ชั่วคราว" คือกี่นาที  ทีม: รู้ เพราะ EV-041 ฝ่ายปฏิบัติการบอก 10 นาที (ปากเปล่า) -> ใส่ใน v2 และคง Q-18 ขอยืนยันเป็นลายลักษณ์อักษร
2. "ช่างที่ว่างใน 7 วัน" นับรวมวันนี้ไหม  ทีม: ไม่รู้ ตัดสินใจเอง ไม่รวมวันนี้ -> AS-06
3. ถ้าลูกค้าปิดเบราว์เซอร์ระหว่างล็อก ใครปลดล็อก  ทีม: ไม่รู้ ต้องถามเจ้าของ -> Q-23 พฤติกรรมชั่วคราว หมดอายุเอง AS-07
4. gateway-timeout 30 วินาทีใน spec ข้อ 9 กับ 60 วินาทีใน Interface Contract IF-01 (docs/srs) อันไหนถูก  ทีม: ไม่รู้ ต้องถาม Dev lead (Q-19) ชั่วคราวใช้ spec = 30
5. AC-07-04 "ใกล้เคียง" กี่ชั่วโมง  ทีม: ไม่รู้ ตอนนั้นตอบว่ารอดูตอน implement (ผิดพลาด ควรตอบตั้งแต่ตอนนี้ ดู GAP-05)
6. BR-01 R3 รอ Q-14 ให้ทำอย่างไร  ทีม: รู้ spec ข้อ 9 มีพฤติกรรมชั่วคราว "ไม่อนุญาต"
7. REQ-QA-003 วัดที่หน้าจอหรือที่ API  ทีม: ไม่รู้ ต้องถามเจ้าของ -> ต่อมากลายเป็น GAP-08 และ CR-02
B สมมติฐานที่ซ่อนอยู่: ลูกค้าหนึ่งคนล็อกได้ทีละ 1 ช่วง (ทีมรับเป็น AS-07 ส่วนหนึ่ง)
C สิ่งที่อยากเดาแต่ไม่ได้เดา: ส่ง SMS ซ้ำ 3 ครั้งถ้าส่งไม่สำเร็จ (ไม่มี REQ รองรับ ไม่ใส่)
ผล: spec.md v2 (Change Log 1.1) commit "spec v2"

## #21 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /plan specs/002-booking/spec.md

AI หยุดถามก่อนเขียนไฟล์: spec ไม่ระบุภาษา framework ฐานข้อมูล เสนอ 3 ชุด (ก) Python FastAPI + React, (ข) Node Express + React, (ค) Django ครบชุด พร้อมข้อดีข้อเสีย
ทีม: เลือก (ก) Python FastAPI + SQLAlchemy + PostgreSQL หลังบ้าน และ React (Vite) + Tailwind CSS หน้าจอ เพราะสมาชิก 3 ใน 4 เคยใช้ และวิชาอื่นใช้ PostgreSQL อยู่แล้ว (บันทึกใน plan.md ข้อ 2 ว่า "ทีมเลือกเอง ไม่ได้มาจาก spec")
AI รายงาน 3 เรื่อง
1. Constraint ที่ยังไม่ได้ใช้: REQ-IF-005 รอ Q-19 (ต่อมาทีมแก้ตารางข้อ 5 เป็น "ใช้แล้ว" เมื่อตั้งค่าชั่วคราว 30)
2. AC ที่ทดสอบยาก: AC-07-08 ต้องการผู้ใช้ 500 คน เสนอย่อส่วนเป็น 20 คำขอ ทีมต้องตัดสินใจ
3. สิ่งที่อยากเดาแต่ไม่ได้เดา: ใช้ Redis เป็นคิว (ไม่อยู่ใน Constraints จึงเขียน "ทีมเลือกเอง" และใช้คิวในหน่วยความจำก่อน)
ทีมเทียบกับแผนที่เขียนเอง (plan-compare.md) พบว่าแผนของทีมลืม REQ-SEC-004 -> GAP-02
ผล: plan.md v1 commit "plan v1"

## #22 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /tasks specs/002-booking/spec.md

AI รายงาน: 11 task, 0 รอ Q | task ยากสุด T-05 (timeout + inquiry) | AC ทดสอบยาก AC-07-08
ทีมตรวจตารางความครบ พบ AC-07-08 "ว่าง" -> สั่ง "เพิ่ม task สำหรับ AC-07-08" ได้ T-09
ทีมพบ T-06 ตั้ง "พร้อมทำ" ทั้งที่ R3 รอ Q-14 -> GAP-03
แก้รอบที่ 1: สั่ง "T-06 ทำเฉพาะ R1, R2, R4, R5, R6 ส่วน R3 ใช้พฤติกรรมชั่วคราวตาม spec ข้อ 9 และข้าม test R3 พร้อมเหตุผล" AI แก้แล้ว
ผล: tasks.md v1 commit "tasks v1"

## #23 | 4 ต.ค. 2569 | Copilot Chat (Agent) | /implement T-01 specs/002-booking/tasks.md

AI ตรวจ 3 อย่างก่อนเริ่ม ผ่าน repo ยังไม่มีโค้ด จึงสร้างโครงตาม plan.md ข้อ 2 ก่อน (backend/requirements.txt, pytest.ini, frontend/package.json, vite.config.js) แล้วสร้าง config.py, session.py, models.py, m001_init.py, main.py, conftest.py
ตรวจ 5 ข้อ: ข้อ 1 ไฟล์ที่แตะ **ไม่ตรง** AI แก้ booking/router.py เพิ่มด้วย (ไฟล์ของ T-04) -> GAP-04 สั่ง revert แล้วทำใหม่
สิ่งที่ AI ถามแทนการเดา: จะเก็บ job_status_history แยกตารางหรือเก็บใน jobs  ทีม: แยกตาราง (REQ-DAT-002 ต้องเก็บประวัติ 24 เดือน)
test: test พื้นฐานสร้างตาราง 8 ตาราง ผ่าน

## #24 | 4 ต.ค. 2569 | /implement T-02

สร้าง hold_slot, release_expired_holds, POST /slots/{id}/hold  ผ่านตรวจ 5 ข้อ
AI ถาม: ลูกค้าคนเดิมล็อกซ้ำช่วงเดิมได้ไหม  ทีม: ได้ ต่ออายุให้ (บันทึกเป็นพฤติกรรม ไม่ต้องมี REQ ใหม่เพราะไม่ขัดกับ REQ-FN-041)

## #25 | 4 ต.ค. 2569 | /implement T-03

สร้าง technicians/service.py, router.py, clock.py และ test_AC_07_02 ผ่าน
AI ถาม: ระยะทาง BR-03 คำนวณอย่างไรเมื่อยังไม่มี IF-03 จริง  ทีม: ใช้สูตร haversine ชั่วคราว ใส่คอมเมนต์ว่า IF-03 ในระบบจริง
AI เพิ่ม now=... ใน query เพื่อให้ test กำหนดเวลาได้ ทีมรับ แต่กำกับว่าระบบจริงไม่รับค่านี้ (ต้องมี task ปิดก่อนขึ้นระบบจริง ยังไม่สร้างเพราะไม่มี REQ รองรับ -> จดไว้ใน README)

## #26 | 4 ต.ค. 2569 | /implement T-04

AI หยุดถาม: AC-07-04 "ใกล้เคียง" กี่ชั่วโมง เขียน assert ไม่ได้  ทีม: ไม่รู้ -> เปิด CR-01 (3 ชั่วโมง ที่มา EV-004) RE lead อนุมัติ แก้ spec v3 และ booking.feature v1.1 ก่อน แล้วสั่งทำต่อ (GAP-05)
สร้าง create_booking, payments/gateway.py, payments/service.py, POST /bookings  test_AC_07_01, test_AC_07_04 ผ่าน
ตรวจ 5 ข้อ: ข้อ 4 test ตรวจ Then ครบไหม พบ test_AC_07_01 ไม่ได้นับจำนวน Payment (ทดลองให้ตัดเงิน 2 ครั้ง test ยังผ่าน) -> GAP-06 สั่งเพิ่ม assert

## #27 | 4 ต.ค. 2569 | /implement T-05

สร้าง GatewayTimeout, status_inquiry, test_payment.py
pytest รอบแรก: test_AC_07_05 **ไม่ผ่าน** assert timeout 30 แต่ AI ตั้ง GATEWAY_TIMEOUT_SECONDS = 60 ตาม IF-01 ใน docs/srs
AI รายงานว่า "เอกสารสองฉบับบอกไม่ตรงกัน ไม่เดา" ทีม: spec.md ข้อ 9 ชนะ (30) ตั้ง config 30 -> GAP-07 บันทึกให้ Dev lead เช็คสัญญาจริง (Q-19)
รอบสอง test_AC_07_05, 06, 07 ผ่าน

## #28 | 4 ต.ค. 2569 | /implement T-06

AI ตรวจก่อนเริ่ม: T-06 มีหมายเหตุ R3 รอ Q-14 ถามว่าจะทำต่อไหม ทีม: ทำตามแก้รอบที่ 1 (เฉพาะแถวอื่น R3 ตอบ 409)
สร้าง refund/rules.py, service.py, router.py, test_refund.py  ผ่าน 5 แถว + R6 + R3 ชั่วคราว, R3 ข้าม
AI ถาม: "ปัดขึ้นหลักสิบ" ของ 175 คือ 180 ใช่ไหม  ทีม: ใช่ ตาม rules.md ตัวอย่าง

## #29 | 4 ต.ค. 2569 | /implement T-07

สร้าง notify/queue.py, enqueue ใน create_booking, GET /notifications/queue  test_AC_07_03 ผ่าน
AI ไม่ได้ถามอะไร ไม่มีการเดา

## #30 | 4 ต.ค. 2569 | /implement T-08

สร้าง technician_view, GET /jobs/{id}/technician-view, privacy.py, test_privacy.py
ตรวจ 5 ข้อ: ข้อ 3 Constraint เห็นในโค้ดจริงไหม พบ router log ทั้ง dict รวมเบอร์โทร (ขัด REQ-PRV-002) -> GAP-09 สั่งให้ทุก logger ผ่าน privacy.py และเพิ่ม assert ใน test
พิสูจน์ชั้น 3: เปลี่ยน PHONE_REVEAL_HOURS เป็น 3 test พัง เปลี่ยนกลับ test ผ่าน

## #31 | 4 ต.ค. 2569 | /implement T-09

AI บอกว่า AC-07-08 ทดสอบจริงไม่ได้ในสภาพแวดล้อมนี้ เสนอ test ย่อส่วน 20 คำขอ ทีม: รับ แต่ต้องบันทึกใน ac-results.md ว่าย่อส่วน และเปิด CR-02 ให้สเปกวัดได้ (GAP-08)
สร้าง test_load_scaled.py ผ่าน

## #32 | 4 ต.ค. 2569 | /implement T-10

สร้างหน้าจอ 3 หน้าและ AC-07-04.test.jsx
npm test รอบแรกพัง: toHaveTextContent ไม่รู้จัก (ไม่มี jest-dom ใน template) -> GAP-10 สาเหตุ env AI เสนอเพิ่ม @testing-library/jest-dom ทีมอนุมัติ (แตะ package.json, vite.config.js, setupTests.js นอกรายการไฟล์เดิม ทีมเพิ่มในช่อง "ไฟล์ที่แตะ" ของ T-10 ก่อนให้ทำ)
AI ถาม: ยอดมัดจำบนหน้าจอเอาจากไหนก่อนจอง  ทีม: ใช้ตารางเดียวกับหลังบ้าน (ประปา 350) ชั่วคราว ระบบจริงต้องมี API ราคาประเมิน (UC-07 ขั้น 4 ยังไม่มี REQ แยก จดไว้)

## #33 | 4 ต.ค. 2569 | /implement T-11

เพิ่ม seed_demo.py และยืนยัน proxy /api ใน vite.config.js เปิด uvicorn + npm run dev กดจองจนเห็น "งาน #1 สถานะ ยืนยันแล้ว"
ไม่มีการเดา

## #34 | 4 ต.ค. 2569 | รัน test ทั้งชุด

cd backend && pytest -v -k "AC_" 2>&1 | tee ../specs/002-booking/test-run.txt  ผล 15 passed, 1 skipped
cd frontend && npm test  ผล 1 passed
กรอก ac-results.md รอบที่ 2 และสรุป gaps.md 10 แถว

## #35 | 4 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /tasks specs/002-booking/spec.md

AI ตรวจ spec.md + plan.md + AGENTS.md ก่อนลง task และพบว่ามี Open Questions หลายข้อที่ยังต้องคงไว้ตาม spec จึงไม่เดา
AI สร้าง tasks.md ใหม่พร้อมทั้งตารางตรวจความครบและรายการ Open Questions โดยมี 10 task รวม
- 5 task ที่รอคำตอบหรือ CR/Q ระดับต่าง ๆ (T-03, T-05, T-07, T-09, T-03/T-04 ต่อ Q-23)
- 5 task ที่พร้อมเริ่มทำทันทีโดยไม่ต้องตัดสินใจมากเกินไป
AI สรุป 3 เรื่อง:
1. task ที่ยากที่สุดคือ T-05 เพราะมีความซับซ้อนของ payment timeout + status inquiry + gateway contract
2. AC ที่ทดสอบยากที่สุดคือ AC-07-08 เพราะต้องมีโหลดแบบพร้อมผู้ใช้ 500 คน โดยใช้แบบย่อส่วน (scaled probe) แทนการทดสอบเต็ม production-like
3. AC-07-04 เป็นความท้าทายเฉพาะ UI เพราะต้องอธิบาย "ใกล้เคียง" และรอความชัดเจนจาก CR-01/ลูกค้าในเวลาต่อไป
ผล: tasks.md ถูกจัดใหม่เพื่อให้ทุก AC มี task ป้องกัน gap และบันทึก Open Questions ให้ทีมตรวจก่อนเริ่มพัฒนา

## #36 | 4 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-10 specs/002-booking/tasks.md

AI ตรวจว่า T-10 ใน repo มีอยู่แล้วและตรงกับงานหน้าจอเลือกช่างและยืนยันการจองที่ต้องทำตาม AC-07-04
AI รัน test แบบเจาะจงของหน้าจอ: cd frontend && npm test -- --run src/__tests__/AC-07-04.test.jsx
ผล: 1 file passed, 1 test passed
สิ่งที่ตรวจ: UI แจ้ง "ช่วงเวลาถูกจองแล้ว" ปรับให้แสดงปุ่มช่วงใกล้เคียงและไม่เรียก onConfirmed เมื่อกรณี slot_taken
ข้อสรุป: T-10 เสร็จและพร้อมให้ทีมตรวจ diff ก่อนรันชุด frontend ทั้งหมด

## #37 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-01 specs/002-booking/tasks.md

ทีมเลือก T-01 ให้เริ่มก่อนตามลำดับ T-xx
AI ตรวจ spec.md, plan.md, tasks.md, AGENTS.md, models.md และ rules.md พบว่า T-01 มีสถานะ "พร้อมทำ", ไม่มี prerequisite และมีเกณฑ์เสร็จครบ ไฟล์โครงสร้างฐานข้อมูลที่ระบุใน task มีอยู่แล้วจากการทำงานก่อนหน้า จึงไม่แก้โค้ดใน scope
ผลตรวจ migration: upgrade(engine) สร้างตารางหลักครบ 8 ตาราง และ JOB_STATUSES มี 8 ค่า ตาม MD-STM-01
ผล test: cd backend && pytest -v -k "AC_" = 14 passed, 1 skipped, 1 failed; failure คือ test_AC_07_08_search_under_load_scaled ล้มจาก concurrent request ทำให้ TimeSlot.start เป็น None ที่ technicians/service.py:58 (อยู่นอก scope T-01) รันซ้ำโดยตัด AC-07-08 ออกได้ 14 passed, 1 skipped, 1 deselected
ผล frontend: cd frontend && npm test = 1 test passed
สิ่งที่ AI เกือบต้องแก้ข้าม scope: failure ของ AC-07-08 อยู่ในงาน load test/เส้นทางค้นหาช่าง ไม่ใช่ไฟล์ใน T-01 จึงหยุด ไม่แก้ T-09/T-02 แทนทีม
ข้อสรุป: ยังไม่เปลี่ยนสถานะ T-01 เพราะ pytest ทั้งชุดยังไม่ผ่าน; รอแก้ปัญหา AC-07-08 ใน task ที่เกี่ยวข้องก่อน

## #38 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | แก้ test AC-07-08 ที่ไม่ผ่าน

ทีมอนุญาตให้แก้ปัญหาการทดสอบที่ไม่ผ่านตามเห็นสมควร
AI รันซ้ำ test_AC_07_08_search_under_load_scaled และยืนยันต้นเหตุ: fixture เดิมใช้ SQLite in-memory กับ StaticPool ที่แชร์ DBAPI connection เดียวกันข้าม request threads; SQLite แจ้ง InterfaceError: bad parameter or other API misuse (อีกรอบพบ TimeSlot.start เป็น None)
แก้ backend/tests/test_load_scaled.py ให้ใช้ SQLite แบบไฟล์ชั่วคราวและ connection pool แยก session ต่อ request แทน fixture in-memory ที่ใช้กับ test อื่น; อัปเดต specs/002-booking/ac-results.md เพิ่มผล rerun
ผล test: test AC-07-08 เจาะจงผ่าน 1 passed; `cd backend && pytest -v -k "AC_"` ผ่าน 15 passed, 1 skipped; Pylance syntax check ไม่พบ syntax errors
ไม่มีการเปลี่ยน business logic หรือเกณฑ์ AC; AC-07-08 ยังเป็น scaled test 20 requests ไม่ใช่ผลตรวจรับจริงที่ 500 concurrent users และ CR-02 ยังรอ SH-01

## #39 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | ปิด T-01 หลังแก้ test ที่บล็อก

หลังแก้ AC-07-08 แล้ว รัน `cd backend && pytest -v -k "AC_"` ผ่าน 15 passed, 1 skipped; รัน test AC-07-08 เจาะจงผ่าน และ `cd frontend && npm test` ผ่าน 1 test จากการตรวจ T-01 ก่อนหน้า; ตรวจ migration พบ 8 ตารางและ 8 สถานะงาน
เปลี่ยนสถานะ T-01 เป็น "เสร็จ รอทีมตรวจ" ตามเกณฑ์ใน tasks.md
T-09 ยังคงรอ CR-02 เพราะผล AC-07-08 เป็น scaled test 20 requests ไม่ใช่การตรวจรับจริงที่ 500 concurrent users

## #40 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-02 specs/002-booking/tasks.md

ทีมสั่งเริ่ม T-02 ถึง T-11 ตามลำดับ; เริ่มทำ T-02 ซึ่งเป็น task แรกที่พร้อมทำและมี prerequisite T-01 เสร็จแล้ว
ตรวจ AC-07-02: เดิม test ตรวจว่าช่วงที่จองแล้วไม่ถูกเสนอและช่างที่อยู่นอก BR-03 ไม่แสดง แต่ไม่ได้ยืนยันชัดว่าช่างในระยะให้บริการยังปรากฏ จึงเพิ่ม assertion ยืนยันว่าช่างประสิทธิ์ปรากฏและช่างไกลมากไม่ปรากฏ
ไฟล์โค้ด/test ที่แก้: backend/tests/test_booking.py; ผล `cd backend && pytest -v tests/test_booking.py::test_AC_07_02_slot_not_rebookable` = 1 passed
เปลี่ยนสถานะ T-02 เป็น "เสร็จ รอทีมตรวจ"
ไม่มีการเดาหรือปิด Q-xx ใน T-02; หยุดหลัง task เดียวตามขั้นตอน /implement

## #41 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-03 specs/002-booking/tasks.md

ทีมขอใช้คำตอบ Q-18 และ implement T-03; spec ข้อ 9 ระบุ Q-18 = 10 นาที (config HOLD_MINUTES) อยู่แล้ว จึงไม่สร้างค่าคำตอบใหม่
ก่อน implement พบว่าบันทึกทีม #24 เคยอนุญาตให้ลูกค้าคนเดิมต่ออายุ hold ก่อนหมดเวลา แต่เกณฑ์ T-03 ฉบับปัจจุบันระบุว่าล็อกซ้ำได้เมื่อหมดอายุแล้วเท่านั้น ทีมเลือกให้ยึดเกณฑ์ T-03 และไม่ต่ออายุก่อนครบ 10 นาที
แก้ backend/app/booking/service.py ให้ปฏิเสธการล็อกซ้ำทุกกรณีเมื่อช่วงยังมีสถานะ held; เมื่อถึง hold_expires_at ระบบเคลียร์ล็อกหมดอายุและอนุญาตให้ลูกค้าอื่นล็อกใหม่
เพิ่ม test_AC_07_04_hold_expires_before_relock ใน backend/tests/test_booking.py ตรวจเวลา hold 10 นาที, การปฏิเสธก่อนหมดอายุ และการล็อกใหม่ที่เวลาหมดอายุ
ผล test เจาะจง: 3 passed (test ใหม่ AC-07-04, AC-07-04 no-charge, AC-07-02); backend acceptance suite `pytest -v -k "AC_"`: 16 passed, 1 skipped; Pylance syntax checks ของ service.py และ test_booking.py ผ่าน
เปลี่ยนสถานะ T-03 เป็น "เสร็จ รอทีมตรวจ"; ไม่มีการแก้ไฟล์นอก task scope นอกจาก tasks.md และ prompt-log.md สำหรับติดตามงาน

## #42 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-04 specs/002-booking/tasks.md

ทีมสั่ง implement T-04; task มีสถานะพร้อมทำ, prerequisites T-02 และ T-03 เสร็จรอทีมตรวจแล้ว, และไฟล์/เกณฑ์เสร็จครบ
ตรวจ AC-07-01 และ AC-07-04: implementation สร้างงานสถานะ confirmed หลัง payment approved, เปลี่ยน slot เป็น booked, และปฏิเสธ slot ที่ booked ก่อนเรียก payment gateway อยู่แล้ว; เพิ่ม test_AC_07_01_cannot_book_same_slot_twice ยืนยันว่าการจองซ้ำได้ 409 โดยไม่มี job/payment เพิ่มและไม่มี gateway call ซ้ำ
ไฟล์โค้ด/test ที่แก้: backend/tests/test_booking.py; ผล focused tests AC-07-01 success, AC-07-01 duplicate booking, AC-07-04 no-charge = 3 passed
ผล backend acceptance suite `cd backend && pytest -v -k "AC_"` = 17 passed, 1 skipped (R3 ยังรอ Q-14); Pylance syntax check ผ่าน
ไม่มี Q-xx ของ T-04 ที่ต้องสมมติ และไม่ได้เปลี่ยน contract ของ Payment Gateway เดิม (REQ-CON-003); เปลี่ยนสถานะ T-04 เป็น "เสร็จ รอทีมตรวจ"

## #43 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-05 specs/002-booking/tasks.md

ก่อนเริ่ม T-05 มีสถานะ "รอ Q-19"; ทีมตอบให้ปิด Q-19 ด้วยค่า 30 วินาที แล้วเริ่ม implement
อัปเดต specs/002-booking/spec.md: REQ-IF-005 ระบุ timeout 30 วินาทีที่ทีมยืนยัน และ Q-19 ระบุว่ายืนยันแล้ว โดยคง GAP-07 ไว้เพื่อตรวจสัญญา gateway จริง; อัปเดต tasks.md ให้ T-05 พร้อมทำแล้วเป็นเสร็จรอทีมตรวจ และปรับรายการ Q-19 เดิมให้สอดคล้อง
การทำงาน payments ตาม AC มีอยู่แล้ว; เพิ่ม assertions ใน backend/tests/test_payment.py ให้ตรวจ authorize ครั้งเดียว, reference เดิมใน authorize/status-inquiry/capture/void, capture เฉพาะกรณี approved, และ timeout 30 วินาที
ผล test `cd backend && pytest -v tests/test_payment.py` = 3 passed; backend acceptance suite `cd backend && pytest -v -k "AC_"` = 17 passed, 1 skipped (Q-14); Pylance syntax check และ git diff --check ผ่าน
ใช้ Gateway interface เดิม (REQ-CON-003); ก่อนทดสอบไม่พบ requirement ที่ต้องเดาอีก และหยุดหลัง T-05 ตามขั้นตอนหนึ่ง task ต่อครั้ง

## #44 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-06 specs/002-booking/tasks.md

ตรวจสถานะ T-06 พร้อมทำและ prerequisite T-04 เสร็จรอทีมตรวจแล้ว; ตรวจ spec, plan, AC-07-03, models, rules และ AGENTS.md
การ enqueue ข้อความ customer/technician เมื่อสร้างงาน confirmed, due_at = created_at + NOTIFY_WITHIN_SECONDS (60), และ GET /notifications/queue มีอยู่แล้วตาม plan; ไม่เพิ่ม provider จริงเพราะ plan ระบุ in-memory queue และ sender แยกทำงาน
เพิ่ม assertions ใน backend/tests/test_booking.py:test_AC_07_03_notify_both_within_60s ตรวจงาน confirmed, ข้อความพอดี 2 รายการถึง customer/technician IDs ที่ถูกต้อง, created_at ตรงกับ Job.created_at, deadline ไม่เกิน 60 วินาที และข้อความปรากฏผ่าน GET /notifications/queue
ผล test เฉพาะ AC-07-03 = 1 passed; backend acceptance suite `pytest -v -k "AC_"` = 17 passed, 1 skipped (R3/Q-14); Pylance syntax check ผ่าน
ไม่มีสิ่งต้องเดาหรือ Q-xx สำหรับ T-06; เปลี่ยนสถานะ T-06 เป็น "เสร็จ รอทีมตรวจ"; หยุดหลัง task เดียวตาม /implement

## #45 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-07 specs/002-booking/tasks.md

ตรวจ T-07 พร้อมทำและ prerequisite T-04 เสร็จรอทีมตรวจแล้ว; อ่าน spec, plan, AC-07-10, rules, models และ AGENTS.md; คง Q-14 เปิดและคง R3 ตามพฤติกรรมชั่วคราว D-07-04
ตรวจ implementation ใน refund/rules.py, refund/service.py และ refund/router.py แล้วพบว่ารองรับ R1, R2, R4, R5, R6 และปฏิเสธ R3 ตามที่กำหนดอยู่แล้ว; เพิ่ม assertions ใน backend/tests/test_refund.py ให้ยืนยันสถานะ Job/slot และรายการ Refund จริง (R5, R6 และ R3 ชั่วคราวต้องไม่มีรายการคืน; R1/R2/R4 ต้องมีจำนวนเงินและ rule ถูกต้อง)
ผล `cd backend && pytest -v tests/test_refund.py` = 6 passed, 1 skipped (R3 decision scenario รอ Q-14); ผล `cd backend && pytest -v -k "AC_"` = 17 passed, 1 skipped; Pylance syntax check ผ่าน; `git diff --check` ผ่าน; มี StarletteDeprecationWarning เรื่อง httpx แต่ไม่มี test fail
ไม่มีการเดาคำตอบ Q-14; เปลี่ยนสถานะ T-07 เป็น "เสร็จ รอทีมตรวจ" โดยคงบันทึกว่า R3 ใช้พฤติกรรมชั่วคราวและ Q-14 ยังเปิด; หยุดหลัง task เดียวตาม /implement

## #46 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-08 specs/002-booking/tasks.md

ตรวจ T-08 พร้อมทำและ prerequisite T-04 เสร็จรอทีมตรวจแล้ว; อ่าน spec, plan, AC-07-09, rules, models และ AGENTS.md
พบ implementation ใน app/booking/service.py จำกัดการส่ง customer_phone ตาม PHONE_REVEAL_HOURS=2 และสถานะงานที่ยังไม่ปิด; app/booking/router.py ใช้ privacy.get_logger, app/privacy.py มี PhoneFilter สำหรับ REQ-PRV-002 อยู่แล้ว
ขยาย backend/tests/test_privacy.py: เริ่ม caplog ก่อน booking เพื่อครอบคลุม log ตลอด flow; คงการตรวจไม่เปิดเบอร์ที่ 11:30, เปิดที่ 12:00, ไม่มีเบอร์รูปแบบมี/ไม่มีขีดใน log; เพิ่ม test_AC_07_09_phone_hidden_after_job_closed สำหรับ done, cancelled, auto_cancelled
ผล `cd backend && pytest -v tests/test_privacy.py` = 4 passed; ผล `cd backend && pytest -v -k "AC_"` = 20 passed, 1 skipped (R3/Q-14); Pylance syntax check และ `git diff --check` ผ่าน; มี StarletteDeprecationWarning เรื่อง httpx แต่ไม่มี test fail
ไม่พบ requirement หรือคำถามเปิดที่ต้องเดา; เปลี่ยนสถานะ T-08 เป็น "เสร็จ รอทีมตรวจ"; หยุดหลัง task เดียวตาม /implement

## #47 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-09 specs/002-booking/tasks.md

T-09 เดิมรอ CR-02; ทีมสั่งให้สมมติ CR-02 จึงใช้ข้อเสนอใน changes/CR-02.md ตามที่เขียน: AC-07-08 วัด GET /technicians, เกณฑ์ 95/100 ภายใน 2 วินาที และแบบย่อส่วน 20 คำขอในห้องเรียน; บันทึกสมมติฐานใน quality-requirements.md โดยไม่อ้างว่า SH-01 อนุมัติ และไม่ย้าย AC ใหม่เข้า booking.feature ซึ่ง CR-02 กำหนดให้รออนุมัติ
ขยาย backend/tests/test_load_scaled.py:test_AC_07_08_search_under_load_scaled ให้ตรวจทุกคำขอได้รับรายการช่างและ slot ที่คาดครบถ้วน นอกเหนือจาก status 200 และเกณฑ์เวลา 19/20 ภายใน 2 วินาที; อัปเดต ac-results.md ให้รายงานผลย่อส่วนอย่างชัดเจนว่าไม่ใช่ผลจริง 500 คำขอ; ปรับเงื่อนไข/สถานะ T-09 ใน tasks.md ให้ตรงกับสมมติฐาน CR-02
ผล `cd backend && pytest -v tests/test_load_scaled.py` = 1 passed; ผล `cd backend && pytest -v -k "AC_"` = 20 passed, 1 skipped (R3/Q-14); Pylance syntax check และ `git diff --check` ผ่าน; มี StarletteDeprecationWarning เรื่อง httpx แต่ไม่มี test fail
การทดสอบนี้ไม่ใช่การวัด load จริง 500 คำขอ; ผลจริงยังต้องรันบนเครื่องทดสอบตามข้อเสนอ CR-02 และ SH-01 ยังต้องอนุมัติอย่างเป็นทางการ; หยุดหลัง T-09 ตาม /implement

## #48 | 11 ต.ค. 2569 | Copilot Chat (Agent) ใน Codespaces | /implement T-10 specs/002-booking/tasks.md

ตรวจ T-10 สถานะพร้อมทำ; ช่องต้องทำหลังระบุว่าไม่มี prerequisite; อ่าน spec, plan, AC-07-04, models, rules และ AGENTS.md
ตรวจไฟล์ UI ใน scope แล้วพบ App, client, TechnicianPicker, ConfirmBooking และ BookingResult มี flow ค้นหา/เลือก/ล็อก/ยืนยันอยู่แล้ว; test เดิมจำลอง API 409 และตรวจข้อความ "ช่วงเวลาถูกจองแล้ว", alternatives และไม่มีการเปลี่ยนไปหน้าสำเร็จ
เพิ่ม test ใน frontend/src/__tests__/AC-07-04.test.jsx ให้ทดสอบ end-to-end ระดับหน้าจอด้วย API จำลอง: ค้นหา GET, เลือกช่วงแล้วล็อก, ยืนยัน POST booking, แสดงงานและสถานะ "ยืนยันแล้ว"; คง test 409 เดิม
ผล `cd frontend && npm test -- --run` = 2 tests passed; `cd frontend && npm run build` = build ผ่าน; `git diff --check` ผ่าน
ไม่มีข้อกำหนดที่ต้องเดา; เปลี่ยนสถานะ T-10 เป็น "เสร็จ รอทีมตรวจ"; หยุดหลัง task เดียวตาม /implement

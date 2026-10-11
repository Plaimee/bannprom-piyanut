// test หน้าจอของ AC-07-04 (REQ-FN-041, UC-07 E2): API จำลองตอบ 409 slot_taken พร้อมช่วงใกล้เคียง 2 ช่วง
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import App from '../App.jsx'
import ConfirmBooking from '../pages/ConfirmBooking.jsx'

const held = {
  category: 'ประปา',
  technician: { technician_id: 1, name: 'ประสิทธิ์' },
  slot: { slot_id: 1, start: '2026-10-05T14:00:00', end: '2026-10-05T16:00:00' },
}

test('AC-07-04 แสดง "ช่วงเวลาถูกจองแล้ว" และปุ่มช่วงใกล้เคียงอย่างน้อย 2 ปุ่ม โดยไม่ตัดเงิน', async () => {
  // Given ลูกค้าอื่นจองช่วงเวลานั้นไปก่อน (หลังบ้านจำลองตอบ 409 พร้อม alternatives)
  const api = {
    createBooking: vi.fn().mockResolvedValue({
      status: 409,
      body: {
        reason: 'slot_taken',
        alternatives: [
          { slot_id: 2, technician_id: 1, technician_name: 'ประสิทธิ์', start: '2026-10-05T16:00:00', end: '2026-10-05T18:00:00' },
          { slot_id: 3, technician_id: 1, technician_name: 'ประสิทธิ์', start: '2026-10-05T11:00:00', end: '2026-10-05T13:00:00' },
        ],
      },
    }),
  }
  const onConfirmed = vi.fn()
  const onPickAlternative = vi.fn()
  render(<ConfirmBooking api={api} customerId={1} addressId={1} held={held} onConfirmed={onConfirmed} onPickAlternative={onPickAlternative} />)

  // When ลูกค้ากดยืนยัน
  fireEvent.click(screen.getByRole('button', { name: /ยืนยันและชำระมัดจำ/ }))

  // Then ระบบแจ้งว่าช่วงเวลาถูกจองแล้ว
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('ช่วงเวลาถูกจองแล้ว'))
  // And ไม่ไปหน้าผลการจอง (ไม่มีการตัดเงิน)
  expect(onConfirmed).not.toHaveBeenCalled()
  // And เสนอช่วงเวลาใกล้เคียงอย่างน้อย 2 ตัวเลือก
  const altButtons = screen.getAllByRole('button', { name: /ช่าง ประสิทธิ์/ })
  expect(altButtons.length).toBeGreaterThanOrEqual(2)
  // And กดเลือกตัวเลือกแล้วส่งช่วงที่เลือกกลับไป
  fireEvent.click(altButtons[0])
  expect(onPickAlternative).toHaveBeenCalledWith(expect.objectContaining({ slot_id: 2 }))
})

test('AC-07-04 เลือกช่างและช่วงเวลาว่าง แล้วยืนยันการจองสำเร็จ', async () => {
  const api = {
    getTechnicians: vi.fn().mockResolvedValue({
      status: 200,
      body: [{
        technician_id: 7,
        name: 'ประสิทธิ์',
        slots: [{
          slot_id: 11,
          start: '2026-10-05T14:00:00',
          end: '2026-10-05T16:00:00',
        }],
      }],
    }),
    holdSlot: vi.fn().mockResolvedValue({
      status: 200,
      body: { hold_expires_at: '2026-10-05T14:10:00' },
    }),
    createBooking: vi.fn().mockResolvedValue({
      status: 201,
      body: {
        job_id: 42,
        status: 'confirmed',
        scheduled_start: '2026-10-05T14:00:00',
      },
    }),
  }

  render(<App api={api} customerId={1} addressId={3} />)

  fireEvent.click(screen.getByRole('button', { name: 'ค้นหาช่างที่ว่างใน 7 วัน' }))
  const slotButton = await screen.findByRole('button', { name: /14:00/ })
  expect(screen.getByText('ช่าง ประสิทธิ์')).toBeInTheDocument()
  fireEvent.click(slotButton)

  const confirmButton = await screen.findByRole('button', { name: /ยืนยันและชำระมัดจำ 350 บาท/ })
  expect(api.holdSlot).toHaveBeenCalledWith({ slotId: 11, customerId: 1 })
  fireEvent.click(confirmButton)

  expect(await screen.findByText('งาน #42')).toBeInTheDocument()
  expect(screen.getByText('สถานะ: ยืนยันแล้ว')).toBeInTheDocument()
  expect(api.createBooking).toHaveBeenCalledWith({
    customerId: 1,
    slotId: 11,
    addressId: 3,
    category: 'ประปา',
  })
})

# Evidence Files — Hướng dẫn đọc

> Các file `.evidence.json` là bằng chứng kiểm thử thực tế — chương trình đã gửi yêu cầu thật đến máy chủ Buff163 và lưu lại toàn bộ dữ liệu nhận được.  
> Thực hiện: 2026-06-21

---

## Danh sách file

### ep01_goods.evidence.json
**Hỏi Buff163:** "Cho tôi xem danh sách tất cả skin CS2 đang được bán."  
**Kết quả:** ✅ Thành công — Buff trả về **33.876 skin**, chia thành 11.292 trang.  
**Cần:** Đăng nhập (cookie)

---

### ep02_goods_info.evidence.json
**Hỏi Buff163:** "Cho tôi xem thông tin chi tiết của con dao có mã số 44000."  
**Kết quả:** ✅ Thành công — Buff trả về đầy đủ: tên item, ảnh, giá trên Steam, độ hiếm, loại vũ khí.  
**Cần:** Không cần đăng nhập

---

### ep03_sell_order.evidence.json
**Hỏi Buff163:** "Cho tôi xem danh sách người đang rao bán con dao mã 44000 — giá bao nhiêu, float thế nào."  
**Kết quả:** ⚠️ Buff từ chối — tài khoản chưa liên kết với Steam.  
**Cần:** Đăng nhập + liên kết tài khoản Steam  
**Quan trọng:** Đây là nguồn dữ liệu cốt lõi để phát hiện hàng rẻ bất thường.

---

### ep04_buy_order.evidence.json
**Hỏi Buff163:** "Ai đang muốn mua con dao mã 44000 và họ trả giá bao nhiêu?"  
**Kết quả:** ✅ Thành công — Buff trả về danh sách người mua và giá họ sẵn sàng trả.  
**Cần:** Không cần đăng nhập

---

### ep08_price_history.evidence.json
**Hỏi Buff163:** "Cho tôi xem lịch sử giá của con dao mã 44000 trong 30 ngày qua."  
**Kết quả:** ⚠️ Buff từ chối — tài khoản chưa liên kết với Steam.  
**Cần:** Đăng nhập + liên kết tài khoản Steam  
**Lưu ý:** Gọi endpoint này quá nhiều lần có thể bị khóa tài khoản.

---

### ep09_bill_order.evidence.json
**Hỏi Buff163:** "Cho tôi xem những giao dịch mua bán con dao mã 44000 gần đây nhất."  
**Kết quả:** ⚠️ Buff từ chối — tài khoản chưa liên kết với Steam.  
**Cần:** Đăng nhập + liên kết tài khoản Steam  
**Dùng để:** Theo dõi giá thực tế mà người ta đã mua bán thành công — an toàn hơn dùng lịch sử giá.

---

## Trạng thái

| Ký hiệu | Nghĩa |
|---|---|
| ✅ | Buff trả dữ liệu thành công |
| ⚠️ | Buff từ chối — cần liên kết Steam |

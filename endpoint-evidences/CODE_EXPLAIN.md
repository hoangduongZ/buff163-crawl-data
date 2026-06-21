# Giải thích code — Endpoint Verification Tool

> Dành cho người chưa biết Python.  
> Mục tiêu: hiểu tool này làm gì, tại sao viết vậy, mỗi file có vai trò gì.

---

## Bức tranh tổng thể

Tool này làm **một việc duy nhất**: gõ cửa máy chủ Buff163 và hỏi "anh có dữ liệu này không?" — rồi ghi lại toàn bộ câu trả lời vào file để làm bằng chứng.

Giống như bạn mở trình duyệt vào buff.163.com, nhưng ở đây máy tính tự động làm thay và lưu kết quả ra file.

---

## Sơ đồ hoạt động

```
Bạn chạy:  python3 ep01_goods.py
                    ↓
         Đọc cookie từ cookie.txt
                    ↓
         Gửi yêu cầu đến buff.163.com
                    ↓
         Nhận dữ liệu JSON từ Buff
                    ↓
         Lưu vào evidence/ep01_goods.evidence.json
                    ↓
         In kết quả ra màn hình
```

---

## Các file và vai trò

### `_common.py` — Bộ công cụ dùng chung

File này không chạy một mình được. Nó chứa các "công thức" mà tất cả file ep01–ep10 đều dùng lại, gồm 4 công thức chính:

**1. `load_cookie()`** — Lấy thông tin đăng nhập  
Giống như lấy thẻ từ ví trước khi vào cổng. Tool tìm cookie theo thứ tự:
- Tìm trong biến môi trường `BUFF_COOKIE` trước
- Nếu không có thì đọc file `cookie.txt`
- Nếu cả hai đều không có thì trả về "không có gì"

**2. `call(url, params, cookie)`** — Gửi yêu cầu đến Buff163  
Đây là bước quan trọng nhất. Tool dùng thư viện `curl_cffi` thay vì cách thông thường vì:
> Buff163 nhận ra và chặn các yêu cầu "trông giống robot". `curl_cffi` giả lập chính xác chữ ký của Chrome 124 — Buff tưởng đây là người dùng bình thường đang mở trình duyệt.

Hàm này trả về 5 thứ: mã HTTP, thời gian phản hồi, dữ liệu JSON, lỗi nếu có, và nội dung thô.

**3. `save_evidence(filename, payload)`** — Lưu bằng chứng  
Ghi toàn bộ kết quả ra file `.json` với định dạng dễ đọc.

**4. `print_result(...)`** — In kết quả ra màn hình  
Hiển thị dòng tóm tắt khi chạy, ví dụ:
```
HTTP 200  |  1265ms  |  ✅ JSON received
```

---

### `ep01_goods.py` — Hỏi: "Có bao nhiêu skin đang bán?"

```python
URL = "https://buff.163.com/api/market/goods"
PARAMS = {"game": "csgo", "page_num": 1, "page_size": 3}
```

**`URL`**: địa chỉ trang Buff cần hỏi  
**`PARAMS`**: các tham số đính kèm — giống như bộ lọc trên trang web:
- `game=csgo` → chỉ lấy skin CS2
- `page_num=1` → lấy trang đầu tiên
- `page_size=3` → mỗi trang chỉ lấy 3 item (để test nhẹ)

**Kết quả nhận được:** `total_count: 33876` — Buff đang có 33.876 skin CS2

---

### `ep02_goods_info.py` — Hỏi: "Con dao số 44000 là gì?"

```python
PARAMS = {"game": "csgo", "goods_id": 44000}
```

**`goods_id`**: mã số định danh của từng item trên Buff. Giống như mã SKU trong kho hàng.  
- Dota2 dùng mã từ 1–39.999  
- CS2/CSGO dùng mã từ 40.000 trở lên  

File này không cần cookie vì Buff cho phép tra cứu thông tin item mà không cần đăng nhập.

---

### `ep03_sell_order.py` — Hỏi: "Ai đang bán dao 44000, giá bao nhiêu?"

```python
PARAMS = {
    "game": "csgo",
    "goods_id": 44000,
    "page_num": 1,
    "sort_by": "price.asc",         # ← sắp xếp rẻ nhất lên đầu
    "allow_tradable_cooldown": 1,   # ← bao gồm cả hàng đang bị khóa giao dịch
}
```

Đây là endpoint **quan trọng nhất** của cả dự án — nó cho biết ai đang bán cái gì với giá nào. Dữ liệu này dùng để phát hiện hàng bị rao bán rẻ hơn giá thị trường.

**Vấn đề hiện tại:** Buff trả về `Steam Binding Required` — tài khoản chưa liên kết Steam nên chưa dùng được.

---

### `ep04_buy_order.py` — Hỏi: "Ai đang muốn mua dao 44000?"

Tương tự ep03 nhưng hỏi về phía người mua thay vì người bán. Dùng để tính:
- **Spread** = giá bán thấp nhất − giá mua cao nhất
- Spread nhỏ = item thanh khoản tốt, dễ mua bán

---

### `ep08_price_history.py` — Hỏi: "Dao 44000 có giá thế nào trong 30 ngày qua?"

```python
PARAMS = {"game": "csgo", "goods_id": 44000, "days": 30, "currency": "CNY"}
```

**⚠️ Nguy hiểm:** Cộng đồng ghi nhận Buff khóa tài khoản nếu gọi endpoint này thường xuyên — kể cả khi chờ vài giây giữa các lần gọi. File này chỉ dùng để kiểm tra một lần.

---

### `ep09_bill_order.py` — Hỏi: "Dao 44000 vừa được mua bán giá bao nhiêu?"

Khác với ep08 (lịch sử giá tổng hợp), ep09 trả về **từng giao dịch thực tế** đã diễn ra gần đây. An toàn hơn để dùng thường xuyên vì đây là dữ liệu giao dịch, không phải biểu đồ giá.

---

## Tại sao cần `cookie.txt`?

Buff163 yêu cầu đăng nhập để xem một số dữ liệu — giống như bạn phải có tài khoản mới xem được giá bán đầy đủ trên web.

Cookie là "thẻ đăng nhập" mà trình duyệt tự động gửi kèm mỗi lần bạn vào trang. Tool này lấy thẻ đó và dùng lại theo cách thủ công.

**Các cookie quan trọng:**
- `session` — chứng minh bạn đã đăng nhập
- `csrf_token` — mã bảo mật chống giả mạo
- `Device-Id` — nhận dạng thiết bị của bạn

---

## Tại sao dùng `curl_cffi` thay vì cách thông thường?

Python có sẵn thư viện `requests` để gửi yêu cầu HTTP — nhưng Buff163 phát hiện và chặn nó vì "chữ ký kết nối" trông không giống Chrome.

`curl_cffi` tái tạo lại chính xác cách Chrome 124 kết nối với máy chủ (gọi là TLS fingerprint). Buff nhìn vào và tưởng đây là người dùng bình thường.

---

## Đọc file evidence như thế nào?

Mở bất kỳ file `.evidence.json`, bạn sẽ thấy:

```json
{
  "endpoint": "/api/market/goods",   ← hỏi endpoint nào
  "params": { "game": "csgo" },      ← hỏi với tham số gì
  "auth_used": true,                 ← có dùng cookie không
  "status_code": 200,                ← máy chủ trả lời mã gì (200 = OK)
  "latency_ms": 1265,                ← máy chủ trả lời sau bao nhiêu ms
  "error": null,                     ← có lỗi không (null = không)
  "raw_response": { ... }            ← toàn bộ dữ liệu Buff trả về
}
```

Phần quan trọng nhất là `raw_response` — đây là dữ liệu thô từ Buff, chứa toàn bộ thông tin item, giá, số lượng, v.v.

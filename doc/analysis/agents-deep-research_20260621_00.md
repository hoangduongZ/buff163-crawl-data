# Buff163 API — Deep Research (2024–2026)

> Tổng hợp: 2026-06-21  
> Nguồn: GitHub repos, Reddit, Zhihu, GreasyFork  
> Phạm vi: dữ liệu thị trường CS2 — không bao gồm bypass anti-bot hay dùng session người khác

---

## 1. Kiểm thử trực tiếp (2026-06-20)

| Endpoint | HTTP | Code | Kết luận |
|---|---|---|---|
| `GET /api/market/goods/info?goods_id=44000` | 200 | `OK` | ✅ Hoạt động ẩn danh |
| `GET /api/market/goods/buy_order?game=csgo&goods_id=44000` | 200 | `OK` | ✅ Hoạt động ẩn danh |
| `GET /api/market/goods` | 200 | `Login Required` | 🔒 Cần cookie |
| `GET /api/market/goods/sell_order` | 200 | `Login Required` | 🔒 Cần cookie |
| `GET /api/market/category` | 200 | `Path Not Found` | ❌ Endpoint đã chết |
| `GET /api/market/itemset` | 200 | `Path Not Found` | ❌ Endpoint đã chết |
| `GET /api/market/steam_price_history` | 200 | `Path Not Found` | ❌ Endpoint đã chết |

---

## 2. Cookie — Yêu cầu xác thực

### 2.1. Cookie bắt buộc

Các dự án cộng đồng (`buff163Prices`, `tocsvBuff163`) đều yêu cầu tối thiểu 3 cookie lấy từ browser sau khi đăng nhập:

| Cookie | Bắt buộc? | Ghi chú |
|---|---|---|
| `session` | ✅ Có | Token đăng nhập chính |
| `csrf_token` | ✅ Có | Dùng trong header `X-CSRFToken` |
| `Device-Id` | ✅ Có | Một số endpoint báo lỗi nếu thiếu |
| `client_type=web` | ❌ Không | Phần lớn script không dùng vẫn hoạt động |

**Cách lấy cookie:**

1. Đăng nhập tại `https://buff.163.com`
2. Mở DevTools → tab **Network** → Refresh trang
3. Tìm request API bất kỳ → copy header `Cookie`
4. Lưu vào `cookie.txt` (không commit vào git)

### 2.2. Session lifecycle

- **Không thể tạo session** mà không đăng nhập qua NetEase/Steam — không có cách public.
- **Thời gian sống:** không có tài liệu chính thức; thực tế vài ngày đến một tuần. Bị vô hiệu sớm nếu Buff phát hiện hành vi bất thường.
- **Làm mới session:** không có endpoint public. Khi API trả `Login Required` → đăng nhập lại và cập nhật cookie.
- **Phát hiện hết hạn:** signal duy nhất là `code: "Login Required"` trong response.

---

## 3. Cấu trúc response các endpoint chính

### 3.1. `GET /api/market/goods` — 🔒 Cần cookie

Trả về `data.items[]`, mỗi item có:

| Field | Kiểu | Mô tả |
|---|---|---|
| `id` / `goods_id` | int | ID trên Buff |
| `market_hash_name` | string | Tên item |
| `sell_min_price` | string (CNY) | Giá ask thấp nhất hiện tại |
| `sell_num` | int | Số lệnh bán hiện tại |
| `buy_max_price` | string (CNY) | Giá bid cao nhất |
| `buy_num` | int | Số lệnh mua |
| `sell_reference_price` | string (CNY) | Giá tham chiếu do Buff định nghĩa |
| `goods_info.steam_price_cny` | string (CNY) | Giá Steam theo Buff (cập nhật thường xuyên, không có số liệu chính xác) |
| `has_paintwear_rank` | bool | Item có thể lọc theo float |
| `has_fade_name` | bool | Item có biến thể Fade |
| `paintwear_range` | array | Khoảng float hợp lệ |
| `paintseed_filters` | array | Pattern seed cho filter |

### 3.2. `GET /api/market/goods/sell_order` — 🔒 Cần cookie

Trả về `data.items[]`, mỗi listing có:

| Field | Kiểu | Mô tả |
|---|---|---|
| `id` | string | **sell_order_id** — dùng khi đặt mua |
| `price` | string (CNY) | **Giá ask thực tế** — đây là giá phải trả |
| `asset_info.paintwear` | string | Float value |
| `asset_info.info.paintseed` | int | Pattern seed |
| `asset_info.info.metaphysic.data.name` | string | Tên biến thể (Doppler phase, Fade %, ...) |
| `asset_info.info.sticker_infos` | array | Danh sách sticker |
| `asset_info.tradable_after` | int (Unix) | Timestamp khi item hết trade cooldown |
| `user_id` / `seller_id` | string | ID người bán (thường được hash, không có username) |

> `price` là giá ask của từng listing. `unit_price` xuất hiện trong một số context khác nhưng `price` mới là trường cần dùng.

**Sort/filter params:**

```
sort_by=price.asc          → listing rẻ nhất lên đầu
sort_by=paintwear.asc      → float thấp nhất lên đầu
min_paintwear=0.00
max_paintwear=0.07
paintseed=554
```

### 3.3. `GET /api/market/goods/buy_order` — ✅ Public

Trả về `data.items[]`, mỗi item có `price` (bid) và `num` (số lượng). Endpoint này an toàn để poll thường xuyên.

### 3.4. `GET /api/market/goods/bill_order` — 🔒 Cần cookie

Lịch sử giao dịch gần nhất. Tài liệu cộng đồng hạn chế:

- Mỗi phần tử của `items[]` có: `price`, `transact_time` (hoặc `created_at`), có thể có `asset_info.paintwear`
- Hỗ trợ phân trang: `page_num`, `page_size` (tối đa ~10)
- Dùng thay thế an toàn hơn cho `price_history`

> ⚠️ Cấu trúc field chi tiết ít được chia sẻ — cần tự verify bằng `ep09_bill_order.py` với cookie.

### 3.5. `GET /api/market/goods/price_history` — 🔒 ⛔ Rủi ro rất cao

Path đúng là `/api/market/goods/price_history` (không có suffix `/buff`).

**Cảnh báo từ cộng đồng (Zhihu):** Gọi endpoint này gây khóa tài khoản vĩnh viễn, kể cả với delay 1–10 giây giữa các request. Tác giả thử trên nhiều tài khoản phụ — tất cả đều bị khóa sau vài phút. **Không nên dùng endpoint này.**

**Thay thế:** Tự lưu snapshot từ `sell_order` và `buy_order` mỗi lần crawl → tự tính trend 1h/24h/7d.

---

## 4. Catalog goods_id

| Range | Game |
|---|---|
| ~1 – ~39,999 | Dota2 |
| ~40,000+ | CS2/CSGO |
| ~50,000 – ~90,000 | Phần lớn CS2 items |

**Nguồn catalog tốt nhất:** [`ModestSerhat/cs2-marketplace-ids`](https://github.com/ModestSerhat/cs2-marketplace-ids) — JSON chứa Name/ID của hàng chục nghìn CS2 items, stickers, charms, phases. Cập nhật tới 16-Jun-2026.

**Cách xây catalog:**

1. Tải dataset `cs2-marketplace-ids` làm seed
2. Verify từng `goods_id` qua `/goods/info` (public, không cần cookie)
3. Nếu cần catalog đầy đủ: login và gọi `/goods?category=...` từng category

**Không nên brute-force goods_id** — khoảng trống lớn, dễ bị block.

---

## 5. Rate limit và chống bot

Buff163 không công bố rate limit chính thức. Tổng hợp từ cộng đồng:

| Thông tin | Nguồn |
|---|---|
| Nhân viên hỗ trợ nói: "hãy hành xử như con người" | Reddit |
| Scraper 5–10 giây/request → bị khóa sau ~10 phút | Reddit |
| `/goods` gọi liên tục ít rủi ro hơn `/price_history` | Zhihu |
| `/price_history` mỗi 1–2 giây → khóa vĩnh viễn | Zhihu |

**Buff theo dõi:** `Device-Id`, `session`, IP, và mô hình truy cập.

**Crawl schedule an toàn:**

| Endpoint | Tần suất đề xuất |
|---|---|
| `/goods` (catalog) | 1 lần/ngày |
| `/sell_order` (item quan tâm) | 5–30 giây/item |
| `/buy_order` | 5–30 giây/item |
| `/bill_order` | 30–60 phút/item |
| `/price_history` | ❌ Không dùng |

---

## 6. Quản lý session

- **Phát hiện hết hạn:** `code: "Login Required"` trong response — đây là signal duy nhất.
- **Làm mới:** không có endpoint public. Phải đăng nhập lại và cập nhật `cookie.txt`.
- **Best practice:** Lưu thời điểm lấy cookie. Cảnh báo sau 5–7 ngày. Stop crawler khi nhận `Login Required` liên tiếp.

---

## 7. Snipe signal detection

| Yêu cầu | Field cần dùng |
|---|---|
| Giá ask của 1 listing | `price` trong `sell_order.items[]` |
| Listing rẻ nhất | `sort_by=price.asc` → item đầu tiên |
| Giá tham chiếu Buff | `sell_reference_price` trong `/goods` |
| Giá tham chiếu Steam | `goods_info.steam_price_cny` trong `/goods` |
| Float | `asset_info.paintwear` |
| Pattern seed | `asset_info.info.paintseed` |
| Sticker | `asset_info.info.sticker_infos` |
| Phân biệt StatTrak/Souvenir | `asset_info.info` (flags quality/is_souvenir) |

**Công thức snipe đơn giản:**

```
if price < sell_reference_price * 0.9:
    → possible snipe

if price < steam_price_cny * buff_ratio_threshold:
    → possible snipe
```

**Lưu ý:** `sell_min_price` trong `/goods` ≈ giá thấp nhất page 1 của `sell_order`. Tuy nhiên do chênh lệch float/sticker, 2 item cùng `goods_id` có thể chênh giá lớn — luôn gọi `sell_order` để có dữ liệu thực.

---

## 8. Buy flow (tham khảo — chưa triển khai)

Từ script GreasyFork (`Buff批量购买`):

**Bước 1 — Preview:**

```
GET /api/market/goods/buy/preview
  ?game=csgo
  &goods_id=<id>
  &sell_order_id=<id>
  &price=<price>
  &allow_tradable_cooldown=0
```

Trả về phương thức thanh toán và kiểm tra số dư.

**Bước 2 — Đặt mua:**

```
POST /api/market/goods/buy
Headers: X-CSRFToken, Referer, Cookie

Body (JSON):
{
  "game": "csgo",
  "goods_id": <id>,
  "sell_order_id": <id>,
  "price": <price>,
  "pay_method": 3,
  "allow_tradable_cooldown": 0,
  "token": "",
  "cdkey_id": ""
}
```

**Bước 3 — Yêu cầu seller gửi offer:**

```
POST /api/market/bill_order/ask_seller_to_send_offer
Body: { "bill_orders": [<order_id>], "game": "csgo" }
```

> Không triển khai buy flow cho đến khi tool ổn định ≥ 1 tháng.

---

## 9. Nguồn tham khảo

| # | Nguồn | URL |
|---|---|---|
| [1] | buff163Prices README | https://raw.githubusercontent.com/perrebser/buff163Prices/main/README.md |
| [2] | buff163-unofficial-api models | https://raw.githubusercontent.com/markzhdan/buff163-unofficial-api/master/buff163_unofficial_api/models.py |
| [3][6][7][11] | Zhihu — 爬虫日记02 网易buff | https://zhuanlan.zhihu.com/p/182880739 |
| [4] | BuffPricesManager.py | https://raw.githubusercontent.com/perrebser/buff163Prices/main/classes/BuffPricesManager.py |
| [5] | Reddit r/csgomarketforum | https://old.reddit.com/r/csgomarketforum/comments/ny7r6i/ |
| [8] | cs2-marketplace-ids README | https://raw.githubusercontent.com/ModestSerhat/cs2-marketplace-ids/main/README.md |
| [9][10] | Reddit r/Csgotrading | https://www.reddit.com/r/Csgotrading/comments/118ywe7/ |
| [12][14] | GreasyFork — Buff批量购买 | https://greasyfork.org/en/scripts/432032 |
| [13] | GreasyFork — shashumga 3000 | https://greasyfork.org/en/scripts/472920 |

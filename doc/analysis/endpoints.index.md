# Buff163 API — Endpoints Reference

Base URL: `https://buff.163.com`

---

## Auth & Headers

| Header | Giá trị |
|---|---|
| `User-Agent` | Chrome 124 (xem `fetch_goods.py`) |
| `Referer` | `https://buff.163.com/market/` |
| `Cookie` | Session cookie từ `cookie.txt` |
| `X-CSRFToken` | Bắt buộc với POST request |

**Cookie quan trọng:** `session`, `csrf_token`, `Device-Id`, `client_type=web`

- GET endpoints: có thể gọi không cần auth, nhưng rate limit thấp hơn (~30 req/min anonymous vs ~100–200 req/min logged-in)
- POST endpoints: bắt buộc session + CSRF + device verification

### Tổng hợp auth requirement

| # | Endpoint | Method | Auth? | Ghi chú |
|---|---|---|---|---|
| 1 | `/api/market/goods` | GET | 🔒 Auth | **[Verified]** Trả "Login Required" khi không có cookie |
| 2 | `/api/market/goods/info` | GET | ✅ Public | **[Verified]** Hoạt động ẩn danh; goods_id CSGO bắt đầu ~40000 |
| 3 | `/api/market/goods/sell_order` | GET | 🔒 Auth | **[Verified]** Trả "Login Required" khi không có cookie |
| 4 | `/api/market/goods/buy_order` | GET | ✅ Public | **[Verified]** Hoạt động ẩn danh |
| 5 | `/api/market/sell_order/preview` | GET | 🔒 Auth | Phụ thuộc sell_order_id từ #3 — thực tế cần auth |
| 6 | `/api/market/sell_order/buy` | POST | 🔒 Auth | Bắt buộc session + CSRF + device verification |
| 7 | `/api/market/category` | GET | ❌ Dead | **[Verified]** "Path Not Found" — endpoint đã bị xóa |
| 7 | `/api/market/itemset` | GET | ❌ Dead | **[Verified]** "Path Not Found" — endpoint đã bị xóa |
| 8 | `/api/market/goods/price_history` | GET | 🔒 Auth | Path đúng (không có `/buff` suffix); rủi ro ban account cao |
| 9 | `/api/market/goods/bill_order` | GET | 🔒 Auth | Yêu cầu session cookie |
| 10 | `/api/market/steam_price_history` | GET | ❌ Dead | **[Verified]** "Path Not Found" — endpoint đã bị xóa |

---

## Endpoints

### 1. Danh sách hàng trên thị trường — 🔒 Auth [Verified]

```
GET /api/market/goods
```

Script: [`first-base/fetch_goods.py`](../first-base/fetch_goods.py)

**Parameters**

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `game` | string | ✅ | `"csgo"` hoặc `"dota2"` |
| `page_num` | int | | Trang (1-indexed). Mặc định: `1` |
| `page_size` | int | | Số item/trang, tối đa 80. Mặc định: `20` |
| `category` | string | | Lọc vũ khí: `weapon_ak47`, `weapon_awp`, `knife`, `glove`, … |
| `category_group` | string | | Nhóm category cấp cao hơn (vd: `knife`) |
| `min_price` | number | | Giá sàn (CNY) |
| `max_price` | number | | Giá trần (CNY) |
| `exterior` | string | | Tình trạng skin (xem bên dưới) |
| `quality` | string | | Chất lượng item (xem bên dưới) |
| `rarity` | string | | Độ hiếm item (xem bên dưới) |
| `sort_by` | string | | Cách sắp xếp (xem bên dưới) |
| `search` | string | | Tìm kiếm theo tên |
| `tag_ids` | string | | Filter theo tag ID — endpoint `/category` đã dead, dùng param `category` thay thế |

**Giá trị hợp lệ**

| `exterior` | `quality` | `rarity` | `sort_by` |
|---|---|---|---|
| `factory_new` | `normal` | `ancient_weapon` (Covert) | `price.asc` |
| `minimal_wear` | `strange` (StatTrak) | `legendary_weapon` (Classified) | `price.desc` |
| `field_tested` | `tournament` (Souvenir) | `mythical_weapon` (Restricted) | `sell_num.desc` |
| `well_worn` | | `rare_weapon` (Mil-Spec) | `created.desc` |
| `battle_scarred` | | | `transacted_num.desc` |

**Response**

```json
{
  "code": "OK",
  "data": {
    "page_num": 1, "page_size": 80, "total_page": 1605, "total_count": 32083,
    "items": [{
      "id": 33453,
      "name": "AK-47 | Redline (Field-Tested)",
      "market_hash_name": "AK-47 | Redline (Field-Tested)",
      "short_name": "AK-47 | Redline",
      "sell_min_price": "12.34",
      "sell_reference_price": "12.34",
      "buy_max_price": "11.50",
      "quick_price": "12.00",
      "sell_num": 4567, "buy_num": 234,
      "goods_info": {
        "icon_url": "...", "original_icon_url": "...",
        "steam_price": "5.67",
        "steam_price_cny": "40.50",
        "info": { "tags": { "exterior": {}, "quality": {}, "rarity": {}, "type": {}, "weapon": {} } }
      }
    }]
  }
}
```

---

### 2. Chi tiết 1 item — ✅ Public

```
GET /api/market/goods/info
    ?game=csgo
    &goods_id=44000
```

Trả về toàn bộ metadata của item: tên, icon, tags, giá Steam, `steam_price_cny`. Dùng khi cần thông tin đầy đủ cho 1 `goods_id` cụ thể mà không muốn gọi lại endpoint `/goods` với filter.

---

### 3. Sell orders của 1 item — 🔒 Auth [Verified]

```
GET /api/market/goods/sell_order
    ?game=csgo
    &goods_id=44000
    &page_num=1
    &sort_by=default          (hoặc price.asc / paintwear.asc)
    &allow_tradable_cooldown=1
    &min_paintwear=0.00       (tuỳ chọn, lọc float)
    &max_paintwear=0.07       (tuỳ chọn, lọc float)
    &paintseed=661            (tuỳ chọn, lọc pattern)
```

Response chứa `items[]` với từng sell order kèm `asset_info` đầy đủ:

```json
{
  "paintwear": "0.16234567",
  "paintseed": 661,
  "info": {
    "stickers": [{ "name": "iBUYPOWER (Holo) | Katowice 2014", "wear": 0.0 }]
  }
}
```

> Layer quan trọng nhất cho float/sticker sniping — 2 skin cùng `goods_id` có thể chênh giá 100× vì float + sticker.

---

### 4. Buy orders của 1 item — ✅ Public

```
GET /api/market/goods/buy_order
    ?game=csgo
    &goods_id=44000
```

---

### 5. Preview sell order (kiểm tra giá còn không) — 🔒 Auth (thực tế phụ thuộc #3)

```
GET /api/market/sell_order/preview
    ?sell_orders={sell_order_id}
    &game=csgo
```

---

### 6. Mua hàng — 🔒 Auth

```
POST /api/market/sell_order/buy
Body: sell_orders, price, game, ...
```

Yêu cầu: CSRF token trong header `X-CSRFToken` + valid session + device verification.

---

### 7. Categories & Tags — ❌ Dead (Path Not Found)

```
GET /api/market/category?game=csgo    ← confirmed dead 2026-06-20
GET /api/market/itemset?game=csgo     ← confirmed dead 2026-06-20
```

**Thay thế:** Dùng param `category` trực tiếp trong endpoint #1:

```
category=weapon_ak47
category=weapon_awp
category=weapon_m4a1
category=weapon_m4a1_silencer
category=knife
category=sticker
category=container
```

Cách lấy giá trị category chính xác: mở buff.163.com trên browser đã login → chọn filter → quan sát param `category` trong Network tab.

---

### 8. Price history — 🔒 Auth

```
GET /api/market/goods/price_history
    ?game=csgo
    &goods_id=44000
    &days=30          (7 | 30 | 90)
    &currency=CNY
```

> **⚠️ Rủi ro cao:** Cộng đồng ghi nhận tài khoản bị khóa khi gọi endpoint này thường xuyên, kể cả với delay vài giây. **Khuyến nghị:** Tự lưu snapshot từ sell/buy order mỗi lần crawl, tự tính trend 1h/24h/7d thay vì gọi price_history liên tục.

---

### 9. Lịch sử giao dịch gần đây — 🔒 Auth

```
GET /api/market/goods/bill_order
    ?game=csgo
    &goods_id=44000
```

> Dữ liệu lịch sử price + bill_order là nguồn tốt nhất để train time-series model.

---

### 10. Lịch sử giá Steam — ❌ Dead (Path Not Found)

```
GET /api/market/steam_price_history    ← confirmed dead 2026-06-20
```

Endpoint này không còn hoạt động. Không có alternative trực tiếp từ Buff. Nếu cần giá Steam, dùng Steam Market API hoặc dataset cộng đồng.

---

## Ghi chú

- Tất cả giá trị giá (`sell_min_price`, `buy_max_price`, …) là **string** dù là số.
- `steam_price` = USD, `steam_price_cny` = CNY — hai field riêng biệt.
- `goods_id` là key để gọi các endpoint chi tiết (#2–#9).
- `market_hash_name` là key để cross-reference với Steam Market và các sàn khác.

### goods_id range

| Game | goods_id range | Ghi chú |
|---|---|---|
| Dota2 | ~1 – ~39999 | Verified: id=33453 là Dota2 item |
| CS2/CSGO | ~40000+ | Verified: id=44000 là ★ Bayonet \| Night (FN) |

**Không nên brute-force goods_id** — khoảng trống lớn, dễ bị block. Thay thế: dùng dataset `ModestSerhat/cs2-marketplace-ids` làm seed, verify từng id qua `/goods/info`.

### Rate limit (community)

- Không có rate limit chính thức từ Buff163.
- Cộng đồng ghi nhận: bị ban sau ~10 phút khi crawl random 5–10 giây/request.
- `/goods/price_history` rủi ro nhất — cân nhắc bỏ hoàn toàn.
- Crawl an toàn: catalog 1 lần/ngày, sell/buy order 5–30 phút/item.

**Tài liệu chi tiết response fields:** [`first-base/docs/buff163_goods_api.md`](../first-base/docs/buff163_goods_api.md)


# Các field cần thiết từ Buff163 API

Dựa trên web tool hiện tại (screenshot) và tài liệu endpoints.

---

## 1. Endpoint `/api/market/goods` — Hiển thị danh sách item

### Field bắt buộc

| Field | Kiểu | Mục đích |
|---|---|---|
| `id` | int | goods_id — key để gọi các endpoint chi tiết |
| `name` | string | Tên đầy đủ hiển thị trên UI |
| `market_hash_name` | string | Cross-reference với Steam Market |
| `sell_min_price` | string (CNY) | Giá bán thấp nhất — hiển thị ở cột giá bên phải |
| `buy_max_price` | string (CNY) | Giá mua cao nhất |
| `sell_num` | int | Số listing đang bán — đánh giá thanh khoản |
| `buy_num` | int | Số lệnh mua đang chờ — đánh giá thanh khoản |
| `goods_info.icon_url` | string | URL ảnh item hiển thị góc trái |
| `goods_info.steam_price` | string (USD) | Giá Steam bằng USD |
| `goods_info.steam_price_cny` | string (CNY) | Giá Steam bằng CNY — dùng để tính Buff/Steam ratio |

### Field metadata / lọc

| Field | Kiểu | Mục đích |
|---|---|---|
| `goods_info.info.tags.exterior.localized_name` | string | Tình trạng skin (Factory New, Field-Tested, …) |
| `goods_info.info.tags.quality.internal_name` | string | Chất lượng: `normal`, `strange` (StatTrak), `tournament` (Souvenir) |
| `goods_info.info.tags.rarity.internal_name` | string | Độ hiếm: `ancient_weapon` (Covert), `legendary_weapon`, … |
| `goods_info.info.tags.type.internal_name` | string | Loại item: `csgo_type_rifle`, `csgo_type_knife`, … |
| `goods_info.info.tags.weapon.internal_name` | string | Vũ khí cụ thể: `weapon_ak47`, `weapon_awp`, … |

### Field tính toán (derived)

| Giá trị | Công thức | Hiển thị |
|---|---|---|
| **Độ phổ biến** | chưa rõ công thức — do Buff tính sẵn | % màu cam trên mỗi item row |

---

## 2. Endpoint `/api/market/goods/sell_order` — Chi tiết từng listing

Gọi thêm endpoint này để lấy 2 thông tin hiển thị trên UI mà `/api/market/goods` không có:

| Field | Kiểu | Mục đích |
|---|---|---|
| `created_at` (timestamp) | int | Thời gian tạo listing → tính "Xm ago" |
| `asset_info.tradable_cooldown_end_at` | int\|null | Unlock time → hiển thị "Unlocked" hoặc thời gian còn lại |

---

## 3. Tóm tắt theo mục đích sử dụng

| Mục đích | Field cần |
|---|---|
| Hiển thị tên + ảnh | `name`, `goods_info.icon_url` |
| Hiển thị giá | `sell_min_price`, `goods_info.steam_price` |
| Tính Buff/Steam ratio (%) | `sell_min_price`, `goods_info.steam_price_cny` |
| Badge "Unlocked" / thời gian trade hold | `asset_info.tradable_cooldown_end_at` (sell_order endpoint) |
| Hiển thị "Xm ago" | `created_at` (sell_order endpoint) |
| Lọc theo loại / chất lượng / độ hiếm | `goods_info.info.tags.*` |
| Đánh giá thanh khoản | `sell_num`, `buy_num` |
| Gọi API chi tiết tiếp theo | `id` (goods_id) |
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

| # | Endpoint | Method | Public? | Ghi chú |
|---|---|---|---|---|
| 1 | `/api/market/goods` | GET | ✅ Public | Hoạt động không cần cookie, rate limit thấp hơn |
| 2 | `/api/market/goods/sell_order` | GET | ✅ Public | Trả về danh sách sell order; ẩn seller info nếu anonymous |
| 3 | `/api/market/goods/buy_order` | GET | ✅ Public | Tương tự sell_order |
| 4 | `/api/market/sell_order/preview` | GET | ✅ Public | Chỉ kiểm tra giá, không thao tác |
| 5 | `/api/market/sell_order/buy` | POST | 🔒 Auth | Bắt buộc session + CSRF + device verification |
| 6 | `/api/market/category` | GET | ✅ Public | Crawl 1 lần, cache local |
| 6 | `/api/market/itemset` | GET | ✅ Public | Crawl 1 lần, cache local |
| 7 | `/api/market/goods/price_history/buff` | GET | 🔒 Auth | Yêu cầu session cookie; trả về 403/redirect nếu anonymous |
| 8 | `/api/market/goods/bill_order` | GET | 🔒 Auth | Yêu cầu session cookie; trả về 403/redirect nếu anonymous |
| 9 | `/api/market/steam_price_history` | GET | ✅ Public | Dữ liệu Steam, không cần session |

---

## Endpoints

### 1. Danh sách hàng trên thị trường — ✅ Public

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
| `tag_ids` | string | | Filter theo tag ID, dùng sau khi crawl `/api/market/category` |

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
    &goods_id=33453
```

Trả về toàn bộ metadata của item: tên, icon, tags, giá Steam, `steam_price_cny`. Dùng khi cần thông tin đầy đủ cho 1 `goods_id` cụ thể mà không muốn gọi lại endpoint `/goods` với filter.

---

### 3. Sell orders của 1 item — ✅ Public

```
GET /api/market/goods/sell_order
    ?game=csgo
    &goods_id=33453
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
    &goods_id=33453
```

---

### 5. Preview sell order (kiểm tra giá còn không) — ✅ Public

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

### 7. Categories & Tags — ✅ Public

```
GET /api/market/category?game=csgo
GET /api/market/itemset?game=csgo
```

Crawl 1 lần, cache local. Dùng `tag_ids` từ đây để filter mạnh nhất ở endpoint #1.

---

### 8. Price history — 🔒 Auth

```
GET /api/market/goods/price_history/buff
    ?game=csgo
    &goods_id=33453
    &days=30          (7 | 30 | 90)
    &currency=CNY
```

---

### 8. Lịch sử giao dịch gần đây — 🔒 Auth

```
GET /api/market/goods/bill_order
    ?game=csgo
    &goods_id=33453
```

> Dữ liệu lịch sử price + bill_order là nguồn tốt nhất để train time-series model.

---

### 9. Lịch sử giá Steam — ✅ Public

```
GET /api/market/steam_price_history
    ?game=csgo
    &market_hash_name=AK-47%20%7C%20Redline%20(Field-Tested)
```

---

## Ghi chú

- Tất cả giá trị giá (`sell_min_price`, `buy_max_price`, …) là **string** dù là số.
- `steam_price` = USD, `steam_price_cny` = CNY — hai field riêng biệt.
- `goods_id` là key để gọi các endpoint chi tiết (#2–#9).
- `market_hash_name` là key để cross-reference với Steam Market và các sàn khác.

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
![alt text](image.png)
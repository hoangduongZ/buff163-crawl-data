# Endpoint Verification — Buff163

> Verified: 2026-06-21  
> Test item: `goods_id=44000` → `★ Bayonet | Night (Factory New)` (CSGO, appid 730)  
> Auth: cookie.txt có đủ `session` + `csrf_token` + `Device-Id`

---

## Kết quả tổng hợp

| # | Endpoint | HTTP | Code (no cookie) | Code (with cookie) | Kết luận |
|---|---|---|---|---|---|
| 1 | `/api/market/goods` | 200 | `Login Required` | ✅ `OK` | 🔒 Cần cookie |
| 2 | `/api/market/goods/info` | 200 | ✅ `OK` | ✅ `OK` | ✅ Public |
| 3 | `/api/market/goods/sell_order` | 200 | `Login Required` | ⚠️ `Steam Binding Required` | 🔒 Cần bind Steam |
| 4 | `/api/market/goods/buy_order` | 200 | ✅ `OK` | ✅ `OK` | ✅ Public |
| 5 | `/api/market/sell_order/preview` | — | — | ❌ Phụ thuộc #3 | 🔒 Cần bind Steam |
| 6 | `/api/market/sell_order/buy` | — | — | — | 🔒 SKIP — POST destructive |
| 7a | `/api/market/category` | 200 | `Path Not Found` | `Path Not Found` | ❌ Dead |
| 7b | `/api/market/itemset` | 200 | `Path Not Found` | `Path Not Found` | ❌ Dead |
| 8 | `/api/market/goods/price_history` | — | — | ⚠️ `Steam Binding Required` | 🔒 Cần bind Steam + ⛔ rủi ro ban |
| 9 | `/api/market/goods/bill_order` | — | — | ⚠️ `Steam Binding Required` | 🔒 Cần bind Steam |
| 10 | `/api/market/steam_price_history` | 200 | `Path Not Found` | `Path Not Found` | ❌ Dead |

---

## Phát hiện mới — Steam Binding Required

`/sell_order`, `/bill_order`, `/price_history` đều trả `Steam Binding Required` dù đã có cookie hợp lệ.

**Nguyên nhân:** Tài khoản Buff163 chưa được liên kết với Steam account.

**Cách fix:** Đăng nhập Buff163 → Settings → Liên kết Steam → lấy lại cookie mới sau khi bind.

---

## Field thực tế `/api/market/goods` (verified 2026-06-21)

`total_count: 33876` CS2 items, `total_page: 11292`

### Item fields

| Field | Kiểu | Ví dụ |
|---|---|---|
| `id` | int | 956398 |
| `name` | string | `"Kilowatt Case"` |
| `market_hash_name` | string | `"Kilowatt Case"` |
| `sell_min_price` | string | `"1.2"` |
| `buy_max_price` | string | `"1.2"` |
| `sell_reference_price` | string | `"1.2"` |
| `sell_num` | int | 36829 |
| `buy_num` | int | 17063 |
| `quick_price` | string | `"1.19"` |
| `pre_sell_min_price` | string | `"1.19"` |
| `has_buff_price_history` | bool | `true` |
| `bookmarked` | bool | `false` |
| `can_bargain` | bool | `true` |

### goods_info fields

| Field | Kiểu | Ví dụ |
|---|---|---|
| `icon_url` | string | URL ảnh |
| `original_icon_url` | string | URL ảnh gốc |
| `steam_price` | string | `"0.27"` (USD) |
| `steam_price_cny` | string | `"1.83"` (CNY) |

### goods_info.info.tags fields

| Tag | Ví dụ |
|---|---|
| `quality.internal_name` | `"normal"` / `"strange"` (StatTrak) / `"tournament"` (Souvenir) |
| `rarity.internal_name` | `"common"` / `"ancient_weapon"` (Covert) / ... |
| `type.internal_name` | `"csgo_type_weaponcase"` / `"csgo_type_rifle"` / ... |
| `category.internal_name` | `"csgo_type_weaponcase"` / ... |

---

## goods_id range (verified)

| Game | Range | Ghi chú |
|---|---|---|
| Dota2 | ~1 – ~39,999 | id=33453 = Dota2 item |
| CS2/CSGO | ~40,000+ | id=44000 = ★ Bayonet Night FN; id=956398 = Kilowatt Case |

Không brute-force. Dùng [`ModestSerhat/cs2-marketplace-ids`](https://github.com/ModestSerhat/cs2-marketplace-ids) làm seed.

---

## Cách chạy

```bash
cd endpoint-evidences

# Public — chạy ngay không cần cookie
python3 ep02_goods_info.py
python3 ep04_buy_order.py

# Cần cookie (cookie.txt) — hiện hoạt động
python3 ep01_goods.py

# Cần cookie + Steam binding
python3 ep03_sell_order.py
python3 ep05_sell_order_preview.py
python3 ep08_price_history.py    # ⛔ rủi ro ban account
python3 ep09_bill_order.py
```

Cookie format (`cookie.txt`):
```
Device-Id=...; session=...; csrf_token=...
```

---

## Evidence files

Sinh ra tại `evidence/` khi chạy script. Mỗi file chứa `raw_response` đầy đủ từ Buff.

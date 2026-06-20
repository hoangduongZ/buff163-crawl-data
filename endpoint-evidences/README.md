# Endpoint Verification — Buff163

Test item: `goods_id=44000` → `★ Bayonet | Night (Factory New)` (CSGO, appid 730)

> **Note về goods_id:** Dota2 chiếm range ~1–39999. CSGO/CS2 bắt đầu từ ~40000. Không brute-force — dùng dataset `ModestSerhat/cs2-marketplace-ids` làm seed.

---

## Kết quả (không có cookie)

| # | Endpoint | HTTP | Code | Kết luận |
|---|---|---|---|---|
| 1 | `/api/market/goods` | 200 | `Login Required` | ❌ Cần auth |
| 2 | `/api/market/goods/info` | 200 | `OK` | ✅ Public |
| 3 | `/api/market/goods/sell_order` | 200 | `Login Required` | ❌ Cần auth |
| 4 | `/api/market/goods/buy_order` | 200 | `OK` | ✅ Public |
| 5 | `/api/market/sell_order/preview` | — | — | ⏳ Phụ thuộc #3 (cần auth để lấy sell_order_id) |
| 6 | `/api/market/sell_order/buy` | — | — | 🔒 SKIP — POST, destructive |
| 7a | `/api/market/category` | 200 | `Path Not Found` | ❌ Path không tồn tại |
| 7b | `/api/market/itemset` | 200 | `Path Not Found` | ❌ Path không tồn tại |
| 8 | `/api/market/goods/price_history` | — | — | 🔒 Cần cookie ⚠️ Rủi ro ban account |
| 9 | `/api/market/goods/bill_order` | — | — | 🔒 Cần cookie |
| 10 | `/api/market/steam_price_history` | 200 | `Path Not Found` | ❌ Path không tồn tại |

## Kết luận quan trọng

1. **Thực tế Auth requirement khác doc** — Doc ghi #1, #3, #7, #10 là Public nhưng thực tế:
   - #1 `/goods` và #3 `/sell_order` → `Login Required`
   - #7 `/category`, #7b `/itemset`, #10 `/steam_price_history` → `Path Not Found` (endpoint bị xóa hoặc path sai)

2. **Endpoint còn hoạt động public**: chỉ #2 và #4

3. **Cần xác minh với cookie**: #1, #3, #5, #8, #9 — chạy ep08/ep09 sau khi có `cookie.txt`

---

## Cách chạy

```bash
cd endpoint-evidences

# Public — chạy ngay
python3 ep02_goods_info.py
python3 ep04_buy_order.py

# Cần cookie — đặt cookie vào cookie.txt trước
python3 ep01_goods.py
python3 ep03_sell_order.py
python3 ep05_sell_order_preview.py   # tự fetch sell_order_id từ ep03
python3 ep08_price_history.py
python3 ep09_bill_order.py
```

Cookie format (raw Cookie header string):
```
session=xxx; csrf_token=yyy; Device-Id=zzz; client_type=web
```

---

## Evidence files

Mỗi script tạo ra file `.evidence.json` kèm theo khi chạy thành công.

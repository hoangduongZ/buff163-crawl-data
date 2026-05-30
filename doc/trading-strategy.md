# Chiến lược mua/bán vật phẩm Buff163

---

## Tổng quan

Buff163 thu **2.5% phí** khi bán → cần spread tối thiểu **>2.6%** để hòa vốn.

```
profit = sell_price × 0.975 − buy_price
```

---

## 1. Buff/Steam Ratio Arbitrage

Chiến lược phổ biến nhất: mua trên Buff, bán sang Steam Market / CSFloat / Skinport.

### Công thức

```python
ratio  = sell_min_price / steam_price_cny   # Buff so với Steam
spread = buy_max_price  / sell_min_price    # khoảng cách bid/ask
```

### Ngưỡng lọc

| Điều kiện | Ngưỡng | Lý do |
|---|---|---|
| `ratio` | `< 0.70` | Item rẻ hơn Steam >30%, có margin sau phí |
| `spread` | `> 0.90` | Buyer sẵn sàng trả gần giá bán → thoát hàng nhanh |
| `buy_num` | `> 20` | Có thanh khoản thực |
| `sell_num` | `< 500` | Thị trường chưa bão hòa |
| `sell_min_price` | `> 10 CNY` | Đủ margin tuyệt đối sau phí |

### Pseudo-code

```python
candidates = [
    item for item in items
    if float(item["sell_min_price"]) / float(item["goods_info"]["steam_price_cny"]) < 0.70
    and item["buy_num"] > 20
    and item["sell_num"] < 500
    and float(item["sell_min_price"]) > 10
]
```
    
---

## 2. Float / Sticker Sniping

Gọi thêm `/api/market/goods/sell_order?goods_id=X` để lấy chi tiết từng listing.

Hai skin cùng `goods_id` có thể chênh giá **10x–100x** vì float + sticker.

### Float sniping

- Tìm skin có `paintwear` thấp nhưng giá ngang skin float cao
- FN (Factory New): `paintwear < 0.07` → càng gần 0 càng quý
- BS (Battle-Scarred): `paintwear > 0.40` → một số skin BS có pattern đặc biệt

### Sticker sniping

Các sticker có giá trị cao cần theo dõi:

| Sticker | Ghi chú |
|---|---|
| iBUYPOWER (Holo) \| Katowice 2014 | Hiếm nhất, giá trị cao nhất |
| Titan (Holo) \| Katowice 2014 | |
| Crown (Foil) | |
| Các sticker Katowice 2014 khác | |

**Logic:** Nếu `sticker_value > 0.15 × sell_price` → seller định giá sai → cơ hội mua.

---

## 3. Liquidity Analysis

Đọc tín hiệu thị trường từ `sell_num` và `buy_num`.

| Tín hiệu | Ý nghĩa | Hành động |
|---|---|---|
| `buy_num` cao, `sell_num` thấp | Demand > Supply → giá sắp tăng | Mua |
| `sell_num / buy_num > 10` | Bão hòa, khó thoát hàng | Tránh |
| `buy_num = 0` | Không có thanh khoản | Tránh tuyệt đối |
| `transacted_num` cao | Volume thực cao | Dễ flip nhanh |

---

## 4. Price History — Xác định đáy/đỉnh

Dùng 2 endpoint (cần auth):

```
GET /api/market/goods/price_history/buff?goods_id=X&days=30
GET /api/market/steam_price_history?market_hash_name=X
```

### Tín hiệu mua tốt

- Giá hiện tại đang ở **đáy 30 ngày** (`sell_min_price ≈ min(price_history)`)
- Giá Steam ổn định hoặc tăng trong khi giá Buff giảm → ratio càng tốt
- Volume giao dịch (`bill_order`) tăng ở vùng giá hiện tại → có người mua thực

### Tín hiệu bán

- Giá Buff đang về **trung bình 30 ngày** hoặc tiệm cận đỉnh
- `sell_num` tăng đột biến → nguồn cung tăng → giá sắp giảm

---

## 5. Pipeline xào data

```
[1] Crawl /api/market/goods (80 items/page, toàn bộ market)
         ↓
[2] Tính ratio + spread → lọc candidates sơ bộ
         ↓
[3] Gọi /api/market/goods/sell_order → check float + sticker từng listing
         ↓
[4] Gọi /api/market/goods/price_history/buff → xác nhận đang ở vùng giá tốt
         ↓
[5] Gọi /api/market/goods/buy_order → confirm có buyer sẵn sàng
         ↓
[6] Preview qua /api/market/sell_order/preview → kiểm tra listing còn không
         ↓
[7] BUY via POST /api/market/sell_order/buy
```

---

## 6. Scoring model — Ưu tiên item nào mua trước

Gán điểm để rank candidates:

```python
def score(item):
    ratio   = float(item["sell_min_price"]) / float(item["goods_info"]["steam_price_cny"])
    spread  = float(item["buy_max_price"])  / float(item["sell_min_price"])
    liq     = min(item["buy_num"] / 50, 1.0)   # normalize, cap tại 1

    return (1 - ratio) * 0.5 + spread * 0.3 + liq * 0.2
    # → điểm cao hơn = cơ hội tốt hơn
```

---

## 7. Rủi ro cần tránh

| Rủi ro | Cách phòng |
|---|---|
| Trade hold (cooldown) | Check `tradable_cooldown_end_at` — ưu tiên listing "Unlocked" |
| Item giá thấp < 5 CNY | Phí cố định ăn hết margin |
| `sell_num` quá cao (>1000) | Khó thoát hàng, giá dễ bị ép |
| Steam giảm giá đột ngột | Theo dõi `steam_price_history`, không mua khi Steam đang downtrend |
| Sticker bị worn (wear > 0.5) | Check `sticker.wear` trong `asset_info` |

---

## 8. Endpoints tham chiếu

| Endpoint | Auth | Dùng để |
|---|---|---|
| `GET /api/market/goods` | Public | Snapshot toàn bộ market |
| `GET /api/market/goods/sell_order` | Public | Float + sticker từng listing |
| `GET /api/market/goods/buy_order` | Public | Xác nhận thanh khoản |
| `GET /api/market/sell_order/preview` | Public | Kiểm tra listing còn không |
| `GET /api/market/goods/price_history/buff` | 🔒 Auth | Lịch sử giá Buff |
| `GET /api/market/goods/bill_order` | 🔒 Auth | Lịch sử giao dịch thực |
| `GET /api/market/steam_price_history` | Public | Lịch sử giá Steam |
| `POST /api/market/sell_order/buy` | 🔒 Auth | Mua hàng |

Chi tiết params & response: [endpoints.md](endpoints.md)

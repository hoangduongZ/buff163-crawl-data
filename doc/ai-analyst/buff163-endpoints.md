# Buff163 Market API — Endpoint Reference

> **Scope:** Dữ liệu thị trường công khai (giá, listing, lịch sử). Không bao gồm account/giao dịch.  
> **Lưu ý:** Buff163 không có tài liệu public chính thức. Các endpoint dưới đây được reverse-engineer từ cộng đồng.

---

## 1. Endpoint Overview

| Nhóm | Endpoint | Mục đích | Nên dùng? |
|---|---|---|---|
| Catalog | `/api/market/goods` | Danh sách item, goods_id, giá min, số lượng bán | Có |
| Chi tiết | `/api/market/goods/info` | Detail theo goods_id | Có |
| Lệnh bán | `/api/market/goods/sell_order` | Listing đang bán, giá, float, phase/fade | Có |
| Lệnh mua | `/api/market/goods/buy_order` | Buy order / bid price | Có |
| Lịch sử | `/api/market/goods/bill_order` | Sale history gần nhất | Có (crawl nhẹ) |
| Backpack | `/api/market/backpack` | Dữ liệu inventory cá nhân | Không |
| Giao dịch | `/api/market/goods/buy`, `/api/market/bill_order/deliver/cancel` | Mua/bán/cancel | Không |

---

## 2. Endpoint Detail

### `GET /api/market/goods`

Dùng để build bảng catalog goods.

| Param | Ví dụ | Ghi chú |
|---|---|---|
| `game` | `csgo` | Bắt buộc |
| `page_num` | `1` | |
| `page_size` | `20`, `50`, `80` | |
| `category` | | Lọc theo loại item |
| `min_price` | | |
| `max_price` | | |
| `sort_by` | `price.asc`, `price.desc`, `sell_num.desc` | |

---

### `GET /api/market/goods/sell_order`

Dùng để lấy listing đang bán theo goods_id.

| Param | Ví dụ | Ghi chú |
|---|---|---|
| `game` | `csgo` | |
| `goods_id` | `762135` | |
| `page_num` | `1` | |
| `page_size` | `10` | |
| `sort_by` | `price.asc`, `paintwear.asc` | |
| `min_paintwear` | `0.00` | Lọc float |
| `max_paintwear` | `0.07` | Lọc float |
| `paintseed` | `554` | Lọc pattern |

---

### `GET /api/market/goods/buy_order`

Dùng để lấy buy order / bid hiện tại.

| Param | Ví dụ | Ghi chú |
|---|---|---|
| `game` | `csgo` | |
| `goods_id` | `762135` | |
| `page_num` | `1` | |
| `page_size` | `10` | |

---

### `GET /api/market/goods/bill_order`

Dùng để lấy lịch sử giao dịch gần nhất. Crawl nhẹ, không spam.

| Param | Ví dụ | Ghi chú |
|---|---|---|
| `game` | `csgo` | |
| `goods_id` | `33882` | |
| `page_num` | `1` | |
| `page_size` | `10` | |

Response fields: `price`, `transact_time`, `type`, `paintwear`.

---

## 3. Crawl Flow

```
Step 1 — Catalog
  GET /api/market/goods
  → lưu: goods_id, market_hash_name, category, sell_min_price, buy_max_price

Step 2 — Sell orders (các item quan tâm)
  GET /api/market/goods/sell_order
  → lưu: giá bán thấp nhất, float, phase/fade, listing count

Step 3 — Buy orders
  GET /api/market/goods/buy_order
  → lưu: bid cao nhất, bid volume

Step 4 — Bill orders (crawl nhẹ)
  GET /api/market/goods/bill_order
  → lưu: lịch sử sale gần nhất

Step 5 — Analytics
  spread    = ask − bid
  liquidity = số listing + số sale gần đây
  trend     = giá hiện tại vs trung bình 7d/30d
```

---

## 4. Database Schema

```sql
-- Catalog
goods (
  id, buff_goods_id, market_hash_name, category,
  icon_url, steam_price_cny, created_at, updated_at
)

-- Snapshots bán
sell_order_snapshots (
  id, buff_goods_id, price_cny, paintwear, paintseed,
  phase_or_fade, asset_id_hash, crawled_at
)

-- Snapshots mua
buy_order_snapshots (
  id, buff_goods_id, price_cny, quantity, crawled_at
)

-- Lịch sử giao dịch
bill_orders (
  id, buff_goods_id, price_cny, paintwear,
  transact_time, order_type, crawled_at
)

-- Audit crawl
crawl_runs (
  id, source, endpoint, status, item_count,
  error_message, started_at, finished_at
)
```

---

## 5. Project Structure (Python/FastAPI)

```
app/
├── api/
│   ├── goods.py          # xem item
│   ├── prices.py         # xem snapshot giá
│   └── analytics.py      # spread / trend
├── crawlers/
│   ├── buff_client.py    # HTTP wrapper
│   ├── goods_crawler.py
│   ├── sell_order_crawler.py
│   ├── buy_order_crawler.py
│   └── bill_order_crawler.py
├── jobs/
│   ├── scheduler.py      # APScheduler / Celery Beat
│   └── tasks.py
├── models/
│   ├── goods.py
│   ├── price_snapshot.py
│   └── crawl_run.py
└── services/
    ├── price_analyzer.py
    └── alert_service.py
```

---

## 6. Crawl Schedule

| Job | Tần suất |
|---|---|
| Catalog `/goods` | 1 lần/ngày |
| Top item sell/buy order | 5–15 phút/lần |
| Item ít quan tâm | 1–6 giờ/lần |
| Bill order | 30–60 phút/lần |
| Rebuild analytics | Sau mỗi crawl batch |

---

## 7. Giới hạn & Rủi ro

**Không làm:**
- Bypass anti-bot hoặc rotate proxy để né block
- Dùng session/cookie của người khác
- Tự động buy/cancel/sell
- Lưu Steam API key hoặc cookie thô trong database
- Spam request toàn bộ goods_id liên tục

> Một số repo cộng đồng (buff2steam) cảnh báo tài khoản bị ban khi crawl quá nhanh. Crawl chậm, cache mạnh, log lỗi rõ ràng.

---

## 8. Alternatives

| Hướng | Mô tả |
|---|---|
| Tự crawl nhẹ | Dùng 5 endpoint ở trên, giới hạn item cần theo dõi |
| Third-party API | cs2.sh hoặc Apify BUFF163 scraper |
| Hybrid | Third-party cho toàn thị trường; tự crawl BUFF cho item cụ thể |

# Buff163 (buff.163.com) — Phân tích kỹ thuật cho việc Crawl & Arbitrage Trading

> **Đối tượng**: Newbie với platform skin trading
> **Mục tiêu**: Crawl data realtime → phát hiện cơ hội arbitrage → tự động hoá thành web app/tool có thể tích hợp AI
> **Cảnh báo**: Tài liệu này phục vụ research kỹ thuật. Buff163 có ToS rõ ràng cấm bot/scraping. Đọc kỹ phần **Risks** ở cuối.

---

## 1. Tổng quan Buff163

**Buff163** (网易BUFF) là marketplace của **NetEase**, là sàn giao dịch skin/item lớn nhất thế giới về **volume thực tế** cho các game của Valve:

- **CS2 (Counter-Strike 2)** — chiếm ~85% volume
- **Dota 2** — items, sets, couriers
- **TF2, Rust, PUBG** — volume thấp hơn nhiều

### Vì sao Buff163 quan trọng với arbitrage?

| Yếu tố | Buff163 | Steam Market | Skinport/CSFloat/DMarket |
|---|---|---|---|
| Phí seller | ~2.5% | 15% (10% Steam + 5% game) | 5–12% |
| Withdraw cash | Có (CNY → AliPay/WeChat) | **Không** (chỉ Steam Wallet) | Có (USD/EUR) |
| Liquidity | Cao nhất | Cao | Trung bình |
| Giá thực tế | Thường thấp nhất | Cao nhất | Trung bình |

→ **Cơ chế arbitrage cơ bản**: Mua trên Buff (giá CNY rẻ) → list lên Steam Market hoặc Skinport (giá USD cao) → ăn spread sau khi trừ phí + tỷ giá + Steam trade hold (7 ngày).

### Flow nghiệp vụ chính

```
User Buyer ──┐
             ├─► Buff163 (escrow) ──► Steam Trade Bot ──► User Buyer's Steam Inventory
User Seller ─┘         │
                       └─► CNY balance ──► AliPay/WeChat withdraw
```

Buff không tự giữ item. Họ dùng **bot Steam accounts** làm trung gian: seller deposit item lên bot, buyer trả tiền, bot trade item ra cho buyer. Đây là điểm quan trọng vì nó tạo ra **delay** (thường 1–10 phút) giữa lúc click mua và lúc nhận item — ảnh hưởng tới chiến lược sniping.

---

## 2. Cấu trúc trang web & các đối tượng dữ liệu

### 2.1 URL chính

| URL | Mục đích |
|---|---|
| `buff.163.com/market/csgo` | Listing items CS2 |
| `buff.163.com/goods/{goods_id}` | Chi tiết 1 item (tất cả sell orders) |
| `buff.163.com/market/buying?game=csgo` | Buy orders của user |
| `buff.163.com/api/...` | API endpoints (xem mục 3) |

### 2.2 Object model

Có 4 entity cốt lõi cần hiểu:

**`goods`** = một loại skin (ví dụ: AK-47 | Redline (Field-Tested))
- Mỗi `goods` có 1 `goods_id` (integer, ổn định)
- Có `market_hash_name` (chuỗi y hệt Steam dùng) → đây là **PRIMARY KEY** để cross-reference với Steam và các sàn khác
- Có `steam_price`, `steam_price_cny` để Buff tự tính spread

**`sell_order`** = một lệnh bán cụ thể của 1 user
- Mỗi sell_order là 1 instance vật lý của skin (có float, paint seed, stickers cụ thể)
- Có `id`, `price`, `asset_info` (chứa float, paintseed, stickers, screenshot)
- Có `created_at`, `updated_at` — quan trọng để detect giá vừa update

**`buy_order`** = lệnh mua treo sẵn (giống bid)
- Quyết định `buy_max_price` của 1 goods

**`asset_info`** = metadata vật lý của skin
```json
{
  "paintwear": "0.16234567",      // Float value (0.0–1.0)
  "paintseed": 661,                // Pattern seed
  "info": {
    "stickers": [
      {"name": "iBUYPOWER (Holo) | Katowice 2014", "wear": 0.0}
    ]
  }
}
```

→ **Nghiệp vụ quan trọng**: 2 skin cùng `goods_id` có thể chênh giá **100×** vì float + sticker. Crawl chỉ `goods` price là **chưa đủ** cho arbitrage thật, phải crawl tới level `sell_order`.

### 2.3 Hệ thống tag/filter

Trên trang listing có hàng trăm filter (rarity, exterior, weapon, sticker, có/không StatTrak, knife type...). Tất cả map về query params như `tag_ids=x,y,z` hoặc `category_group=knife`. Nên crawl `/api/market/category` 1 lần để có dictionary, sau đó dùng tag_ids là cách query mạnh nhất.

---

## 3. API endpoints (reverse-engineered)

Buff163 là SPA, frontend gọi internal JSON API. Đây là các endpoint quan trọng:

### 3.1 Listing & search

```
GET /api/market/goods
    ?game=csgo
    &page_num=1
    &page_size=80          (max 80, server-enforced)
    &sort_by=price.asc     (price.desc, created.desc, transacted_num.desc, ...)
    &min_price=10
    &max_price=100
    &category_group=knife
    &tag_ids=...
    &search=ak-47
```

Response:
```json
{
  "code": "OK",
  "data": {
    "items": [
      {
        "id": 33453,
        "name": "AK-47 | Redline (Field-Tested)",
        "market_hash_name": "AK-47 | Redline (Field-Tested)",
        "sell_min_price": "12.34",
        "sell_num": 4567,
        "buy_max_price": "11.50",
        "buy_num": 234,
        "steam_price": "5.67",          // USD
        "steam_price_cny": "40.50",     // CNY equivalent
        "goods_info": { "info": { "tags": {...} } }
      }
    ],
    "total_count": 12345,
    "total_page": 155
  }
}
```

→ **Đây là endpoint xương sống cho việc scan toàn market**. Có thể quét toàn bộ ~50.000 goods CS2 bằng pagination.

### 3.2 Sell orders của 1 item

```
GET /api/market/goods/sell_order
    ?game=csgo
    &goods_id=33453
    &page_num=1
    &sort_by=default        (price.asc cũng dùng được)
    &allow_tradable_cooldown=1
```

Response chứa array `items[]` với mỗi sell order kèm `asset_info` đầy đủ (float, sticker, screenshot URL). **Đây là layer quan trọng nhất cho sniping**.

### 3.3 Buy orders

```
GET /api/market/goods/buy_order?game=csgo&goods_id=33453
```

### 3.4 Preview trước khi mua (kiểm tra giá còn không)

```
GET /api/market/sell_order/preview
    ?sell_orders={sell_order_id}
    &game=csgo
```

### 3.5 Bid/Buy execute

```
POST /api/market/sell_order/buy
   body: sell_orders, price, ...  (cần CSRF token + valid session)
```

### 3.6 Categories & tags

```
GET /api/market/category?game=csgo
GET /api/market/itemset?game=csgo
```

→ Crawl 1 lần, cache local.

### 3.7 Price history (cực giá trị cho ML)

```
GET /api/market/goods/price_history/buff
    ?game=csgo
    &goods_id=33453
    &days=30        (7, 30, 90)
    &currency=CNY
```

```
GET /api/market/goods/bill_order
    ?game=csgo
    &goods_id=33453   // recent transactions
```

→ Dữ liệu này **vàng** cho training time-series model.

### 3.8 Steam price comparison

```
GET /api/market/steam_price_history?game=csgo&market_hash_name=...
```

---

## 4. Authentication & Session

### 4.1 Cách Buff xác thực

Buff dùng **NetEase Pass (urs.163.com)** — login qua:
- Email + password
- Steam OpenID (link account)
- Mobile OTP (Trung Quốc)

Sau khi login, các cookie quan trọng trong domain `.buff.163.com`:

| Cookie | Vai trò |
|---|---|
| `session` | Session ID chính (server-side) |
| `csrf_token` | Anti-CSRF, gửi trong header `X-CSRFToken` cho POST |
| `Device-Id` | Fingerprint device, **bắt buộc** từ ~2023 |
| `client_type` | `web` |
| `Locale-Supported` | `en` / `zh-Hans` |
| `game` | game đang xem |

Header thường được check:
- `User-Agent` (phải hợp lý, không phải python-requests/...)
- `Referer` (phải là buff.163.com)
- `X-Requested-With: XMLHttpRequest` (hoặc tương đương)

### 4.2 Read vs Write

- **Read endpoints (GET listing, sell_order, price_history)**: Đa số có thể gọi **không cần login**, nhưng rate limit thấp hơn nhiều và dễ bị captcha.
- **Write endpoints (mua, bán, withdraw, message)**: **Bắt buộc** session hợp lệ + CSRF + device verification (đôi khi cả SMS OTP với Trung Quốc).

→ **Kiến nghị**: Login bằng browser thật 1 lần, export cookie ra (hoặc dùng Playwright giữ session), sau đó dùng cookie cho API requests. Đây là pattern phổ biến nhất.

---

## 5. Anti-bot mechanisms

Buff163 đầu tư mạnh vào anti-bot. Cụ thể:

### 5.1 Rate limiting

- Anonymous: ~30 req/min cho `/api/market/goods`, dễ bị 429
- Logged-in: ~100–200 req/min, nhưng burst nhanh sẽ trigger captcha
- Per-endpoint khác nhau: `sell_order` strict hơn `goods`

### 5.2 Captcha

- Khi nghi ngờ, Buff trigger **NetEase Yidun Captcha** (滑块/slider hoặc text)
- Captcha trả về flag → request bị block tới khi solve
- Solver: 2Captcha, AntiCaptcha, Capmonster đều support Yidun (~$2–3/1000 captcha)

### 5.3 IP-based

- IP ngoài Trung Quốc bị throttle nặng hơn
- IP datacenter (AWS, GCP, Azure) bị flag rất nhanh
- IP Trung Quốc (Aliyun, Tencent Cloud) hoạt động tốt hơn nhưng có rủi ro pháp lý

### 5.4 Device fingerprinting

- `Device-Id` cookie + canvas fingerprint + WebGL + audio fingerprint
- Nếu fingerprint không khớp với session đã login → force re-verify

### 5.5 Behavioral

- Pattern request quá đều → flag (ví dụ: chính xác mỗi 1.0s)
- Không có request tới static assets (image, CSS) → flag
- Mouse movement / scroll events nếu dùng full browser → check qua telemetry

### 5.6 Cloudflare-like layer

Buff dùng riêng NetEase WAF, không phải Cloudflare. Nó check JA3 fingerprint của TLS handshake — `python-requests` dùng OpenSSL fingerprint cố định, dễ bị flag. Cần dùng **`curl_cffi`** (impersonate Chrome TLS fingerprint) hoặc Playwright thật.

---

## 6. Các approach crawl — so sánh

### Approach A: Pure HTTP với cookie từ browser

**Tech**: `httpx` / `aiohttp` / `curl_cffi` + cookie jar export từ Chrome.

| Ưu | Nhược |
|---|---|
| Nhanh nhất (không boot browser) | Cookie hết hạn ~7–14 ngày phải refresh |
| Tốn ít resource (chạy được trên VPS rẻ) | Dễ bị fingerprint nếu không có `curl_cffi` |
| Concurrency cao với async | Không xử lý được captcha tự động |

**Khi nào dùng**: Crawl listing đơn giản, volume vừa phải (vài chục nghìn req/ngày).

### Approach B: Browser automation (Playwright/undetected-chromedriver)

| Ưu | Nhược |
|---|---|
| Vượt được hầu hết fingerprint check | Chậm (1 page = vài giây) |
| Tự động giữ session | Tốn RAM/CPU (1GB/instance) |
| Có thể solve captcha bằng human-in-the-loop | Khó scale |

**Khi nào dùng**: Login flow, mua thực tế, hoặc khi Approach A bị block.

### Approach C: Hybrid (RECOMMENDED)

```
┌──────────────────────┐
│ Playwright instance  │  ← Login + giữ session warm + refresh cookie định kỳ
│ (1 instance/account) │
└──────────┬───────────┘
           │ cookie + headers
           ▼
┌──────────────────────┐
│ httpx async pool     │  ← Crawl heavy (1000s req/min)
│ + curl_cffi          │
│ + proxy rotation     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Captcha detector     │  ── if 403/captcha → escalate to Playwright + 2Captcha
└──────────────────────┘
```

Đây là pattern production các trading bot trên thị trường đang dùng (Pricempire, BitSkins-watcher, etc.).

### Approach D: Reverse engineer mobile app

Buff163 có app Android/iOS dùng cùng API nhưng có **app-only signature** (`X-CA-Signature` hoặc tương tự). Khi bypass được sẽ có rate limit cao hơn web. Khó hơn nhưng giá trị cao.

→ **Khuyến nghị cho beginner**: Bắt đầu với **Approach C**, scope nhỏ (chỉ track 100–500 items đầu tiên), sau đó scale.

### Proxy strategy

- **Residential proxies Trung Quốc** (luminati/brightdata Asia plan): tỷ lệ pass cao nhất nhưng đắt ($5–15/GB)
- **Mobile proxies**: cực kỳ trust nhưng đắt
- **Datacenter rotating proxies**: rẻ nhưng dễ bị block, chỉ dùng cho read endpoints
- **Số lượng**: Tối thiểu 10–20 IP rotating cho production crawl

---

## 7. Chiến lược arbitrage — đi từ data tới profit

### 7.1 Các loại spread thường có

**A. Buff → Steam Market**
- Mua Buff với CNY, list Steam giá USD
- Spread điển hình 15–40% **nhưng**:
  - Phí Steam 15%
  - Bị giam Steam Wallet (không withdraw được)
  - Trade hold 7 ngày
- → Phù hợp khi muốn nạp Steam balance để mua game/items khác

**B. Buff → Skinport/CSFloat/DMarket** (cash arbitrage thật)
- Mua Buff (CNY) → trade lên Skinport (EUR/USD)
- Spread 5–25% sau phí
- Withdraw thật được tiền
- **Đây là target chính cho việc kiếm tiền thật**

**C. Buff internal — Float/Sticker arbitrage**
- Same `goods_id`, khác float/sticker → giá khác xa
- Sticker rare (Katowice 2014, especially iBUYPOWER) có premium 100×–1000×
- Float thấp bất thường (0.00x với Field-Tested condition) → tier cao hơn về cảm quan
- Pattern hiếm (Case Hardened Blue Gem #387, Crimson Web pattern...) → 10×–100× normal

**D. Buff buy_order vs sell_order**
- Khi `buy_max_price > sell_min_price - fee` → mua sell order, list buy order, ăn spread ngay
- Hiếm khi xảy ra (market efficient), nhưng khi xảy ra thì free money

### 7.2 Công thức tính lợi nhuận chính xác

```
profit_usd = (sell_price_target * (1 - fee_target)) / fx_target
           - (buy_price_buff * (1 + fee_buff)) / fx_buff
           - withdraw_fee
           - opportunity_cost(days_held)

ROI = profit_usd / cost_usd
```

Ví dụ Buff → Skinport:
```
Buff:     100 CNY × 1.025 (phí + tip) = 102.5 CNY
          = 102.5 / 7.2 (CNY/USD)     = $14.24 cost

Skinport: $18.00 listing
          × (1 - 0.12 phí Skinport)    = $15.84 nhận về

Profit = $15.84 - $14.24 = $1.60 (11.2% ROI)
Sau khi trừ trade hold 7 ngày + risk → cần ROI ≥ 15% để worth it
```

### 7.3 Thresholds thực tế

| Strategy | Min ROI | Min volume/tháng | Capital cần |
|---|---|---|---|
| Buff→Steam | 8% | Không quan trọng (Steam hold) | $200+ |
| Buff→Skinport | 12% | 30+ giao dịch | $1000+ |
| Float sniping | 30% | 5–10 deals | $500+ |
| Sticker arb | 20% | 10–20 deals | $2000+ |

### 7.4 Tỷ giá CNY/USD/VND — risk

CNY biến động ~3–5%/quý. Nên hedge bằng cách convert nhanh hoặc giữ multi-currency. Đối với scale nhỏ (<$10k turnover/tháng) thì có thể bỏ qua.

---

## 8. Architecture đề xuất cho tool

### 8.1 High-level architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│  Dashboard | Opportunities | Portfolio | Manual Trade UI    │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST + WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                  API Gateway (FastAPI)                       │
└──────────────────────┬──────────────────────────────────────┘
        ┌──────────────┼──────────────┬──────────────┐
        ▼              ▼              ▼              ▼
   ┌─────────┐   ┌──────────┐   ┌─────────┐   ┌──────────┐
   │ Crawler │   │ Arbitrage│   │ Trading │   │ ML/AI    │
   │ workers │   │ engine   │   │ executor│   │ service  │
   └────┬────┘   └────┬─────┘   └────┬────┘   └────┬─────┘
        │             │              │              │
        └─────────────┼──────────────┴──────────────┘
                      ▼
        ┌──────────────────────────────────┐
        │ PostgreSQL + TimescaleDB         │  ← time-series cho price
        │ Redis (cache + pub/sub realtime) │
        │ S3/MinIO (screenshot, sticker)   │
        └──────────────────────────────────┘
```

### 8.2 Crawler workers — chiến lược tiered

```
Tier 1 (high freq, mỗi 30s)  → Top 200 items theo volume + watchlist user
Tier 2 (medium, mỗi 5 phút)  → Top 5000 items
Tier 3 (low, mỗi 30 phút)    → Toàn bộ market (~50k items)
Tier 4 (on-demand)           → sell_order detail khi có signal từ Tier 1
```

→ Tránh "dumb crawl" toàn bộ mọi 30s — sẽ bị ban ngay.

### 8.3 Database schema cốt lõi

```sql
-- Catalog (dim)
CREATE TABLE goods (
  goods_id        BIGINT PRIMARY KEY,
  market_hash_name TEXT UNIQUE,
  game            TEXT,
  category        TEXT,
  rarity          TEXT,
  metadata        JSONB
);

-- Time-series (hypertable TimescaleDB)
CREATE TABLE price_snapshot (
  ts              TIMESTAMPTZ NOT NULL,
  goods_id        BIGINT,
  source          TEXT,            -- 'buff', 'steam', 'skinport', ...
  sell_min        NUMERIC,
  buy_max         NUMERIC,
  sell_count      INTEGER,
  currency        TEXT
);
SELECT create_hypertable('price_snapshot', 'ts');

-- Sell order snapshots (cho float/sticker arb)
CREATE TABLE sell_order_snapshot (
  sell_order_id   TEXT PRIMARY KEY,
  goods_id        BIGINT,
  price           NUMERIC,
  paintwear       NUMERIC,
  paintseed       INTEGER,
  stickers        JSONB,
  screenshot_url  TEXT,
  first_seen      TIMESTAMPTZ,
  last_seen       TIMESTAMPTZ,
  sold_at         TIMESTAMPTZ      -- NULL nếu vẫn còn
);

-- Opportunities detected
CREATE TABLE opportunity (
  id              BIGSERIAL PRIMARY KEY,
  detected_at     TIMESTAMPTZ,
  buy_source      TEXT,
  sell_target     TEXT,
  goods_id        BIGINT,
  expected_roi    NUMERIC,
  confidence      NUMERIC,         -- từ ML model
  status          TEXT,            -- detected/executed/expired
  payload         JSONB
);
```

### 8.4 Realtime layer

- **Redis pub/sub** cho event "price_updated", "opportunity_detected"
- **WebSocket** từ FastAPI push xuống dashboard
- **Celery beat** schedule crawl tier
- **Dramatiq** hoặc **Arq** cho async task queue (nhẹ hơn Celery)

### 8.5 Tech stack final

| Layer | Choice | Vì sao |
|---|---|---|
| Backend | **Python 3.12 + FastAPI** | Ecosystem ML mạnh, async tốt |
| Crawler | **httpx + curl_cffi + Playwright** | Đa dạng tier |
| Queue | **Arq** (Redis-based) | Đơn giản hơn Celery |
| DB | **PostgreSQL 16 + TimescaleDB** | Time-series + relational 1 nơi |
| Cache | **Redis 7** | Pub/sub + cache + queue |
| Frontend | **Next.js 14 + shadcn/ui + TanStack Query** | DX tốt, realtime dễ |
| Charting | **Lightweight Charts (TradingView)** | Free, fast |
| Deploy | **Docker Compose** đầu, **k8s** sau | |
| Proxy | **Bright Data residential pool** | Đắt nhưng pass rate cao |
| Captcha | **2Captcha API** | Cheap, có Yidun support |
| Monitor | **Grafana + Prometheus + Loki** | Standard OSS stack |

---

## 9. AI/ML applications

Đây là phần thực sự tạo edge so với các tool có sẵn (Pricempire, csgofloat, ...).

### 9.1 Price prediction (time-series forecasting)

**Mục tiêu**: Dự đoán giá item trong N ngày → quyết định "hold để bán giá tốt hơn" hay "flip ngay".

- **Baseline**: ARIMA, Prophet — chạy nhanh, dùng làm benchmark
- **ML**: XGBoost với feature engineering (volume, MA7, MA30, RSI, volatility, sticker premium)
- **DL**: LSTM hoặc Temporal Fusion Transformer cho top items có nhiều data

→ Lưu ý: skin market không stationary, có nhiều shock event (Major tournament, case mới release, update game). Phải có feature event-aware.

### 9.2 Anomaly detection (mispricing detection)

**Mục tiêu**: Tự động detect sell order treo giá lệch market (newbie list quá rẻ, hoặc fat-finger).

- **Isolation Forest** trên feature `(price, float, sticker_value, time_since_listed)`
- **Robust z-score** so với median của 100 sell order gần nhất cùng goods
- Khi z-score < -2.5 → opportunity, push notification ngay

→ Đây là **cách kiếm tiền nhanh nhất**, vì sniping mispricing ROI cao và không cần predict tương lai.

### 9.3 Sticker/Pattern valuation

**Mục tiêu**: Định giá chính xác value của sticker combo + pattern.

- Crawl historical sales của items có sticker tương tự
- Train regression model: `value = f(base_price, sticker_combo, sticker_wear, pattern_seed)`
- Đối với pattern hiếm (Case Hardened Blue Gem, Doppler Phase, ...): cần dataset từ csgofloat/pricempire
- **Computer vision**: Phân tích screenshot để verify sticker placement (sticker bị scratch ảnh hưởng giá nhiều)

### 9.4 NLP cho sentiment

- Crawl reddit r/csgomarketforum, r/GlobalOffensiveTrade
- Discord sticker-trading channels
- Detect trend: "X case sắp release" → giá item liên quan biến động

### 9.5 Reinforcement Learning cho execution

**Mục tiêu**: Khi có signal mua, RL agent quyết định:
- Mua ngay hay đợi giá thấp hơn 1%?
- List bán giá nào để fill nhanh nhất với profit max?

→ Advanced, để giai đoạn 3.

### 9.6 Computer Vision

- Verify screenshot khớp với metadata (chống scam)
- Detect rare pattern từ screenshot (vd: blue gem percentage)
- OCR float value từ screenshot khi data không có

---

## 10. Risks — đọc kỹ trước khi build

### 10.1 Technical risks

- **Account ban**: Buff có thể ban tài khoản nếu detect bot. Mất balance trong account.
  - Mitigation: Phân tách "scrape account" và "trade account". Trade thủ công initial.
- **Steam ban**: Steam có thể flag account "trade boosting". Risk thấp với arbitrage thường.
- **Trade hold 7 ngày**: Capital bị giam, không react được khi giá biến động ngược.
- **Liquidity risk**: Item rare khó bán, có thể giam hàng tháng.

### 10.2 Legal/Compliance

- **Buff163 ToS** cấm rõ scraping, automation, bulk operations. Không có precedent kiện cá nhân nhưng có quyền ban + tịch thu balance.
- **VN regulation**: Trading skin chưa có khung pháp lý rõ. Income từ arbitrage cần khai thuế (TNCN).
- **Trung Quốc**: Buff là công ty TQ, payment qua AliPay → cần tài khoản TQ (đa số dùng "号商" — middleman service).
- **Rút tiền về VN**: Thường qua P2P USDT hoặc dịch vụ chuyển khoản TQ-VN.

### 10.3 Market risks

- **CS2 economy crash**: Valve có thể release update làm devalue toàn market (đã xảy ra 2023 với CS2 release)
- **Currency risk**: CNY weak so với USD → profit margin co lại
- **Competition**: Có hàng ngàn bot khác đang scan. Edge của bạn là (a) tốc độ, (b) ML model, (c) niche items không ai cover

### 10.4 Operational risks

- Captcha solve fail → bỏ lỡ opportunity
- Proxy down → crawl die
- Bug trong arbitrage logic → mua nhầm giá cao bán giá thấp (đã có nhiều case lost $$$ vì bug 1 dòng code)

→ **Khuyến nghị tuyệt đối**: Trong giai đoạn đầu, **bot chỉ detect và notify**, mua bán **manual confirm**. Chỉ tự động execute khi đã chạy ổn định ≥ 3 tháng và có kill-switch.

---

## 11. Roadmap MVP → Production

### Phase 1: Discovery (1–2 tuần)
- Đăng ký Buff account, mua bán thủ công 5–10 deal để hiểu flow
- Setup môi trường dev: Python + Postgres + Redis Docker
- Viết script crawl `/api/market/goods` đơn giản, lưu vào DB
- Verify được rate limit thực tế, captcha trigger threshold

### Phase 2: MVP crawler (2–3 tuần)
- Tier 3 crawler (full scan mỗi 30 phút) chạy ổn định 1 tuần không bị ban
- Schema time-series hoạt động, có dashboard Grafana xem giá history
- Tích hợp Steam Market price (qua API public hoặc 3rd party như Steamapis.com)
- Compute basic spread Buff vs Steam, output CSV daily

### Phase 3: Arbitrage detection (3–4 tuần)
- Tích hợp Skinport API (có official API)
- Anomaly detection cơ bản (z-score)
- Web dashboard Next.js: list top opportunities, click vào xem detail
- Telegram bot push notification

### Phase 4: Float/Sticker layer (4–6 tuần)
- Crawl tới level sell_order
- Sticker valuation database
- Float arbitrage detection

### Phase 5: ML & Auto-execute (8+ tuần)
- Price prediction model
- RL execution
- Auto-buy với strict guardrail (max $X/giao dịch, max $Y/ngày)
- Multi-account management

### Phase 6: Scale
- Move sang k8s
- Multi-game (Dota 2, Rust)
- Cross-platform (Skinport ↔ CSFloat ↔ DMarket)

---

## 12. Tài nguyên tham khảo

**Open source projects để học (đọc code, không clone production)**:
- `buff163-py` — Python wrapper không chính thức (search GitHub)
- `csfloat-api` — API CSFloat
- `Pricempire API docs` — aggregator pricing
- `node-globaloffensive` / `node-steam-user` — Steam trade automation

**Communities**:
- Reddit: r/csgomarketforum, r/csgotrading
- Discord: Pricempire, BuffMarket community

**Data sources hỗ trợ**:
- `csfloat.com` — float inspect API (free, có rate limit)
- `steamapis.com` — Steam price aggregator (paid)
- `pricempire.com` — cross-platform aggregator (paid, có free tier)
- `csgostash.com` — metadata items (scrape được)

**Đọc thêm về anti-bot**:
- `curl_cffi` docs (TLS impersonation)
- `playwright-stealth` plugin
- "Web scraping with TLS fingerprint" articles

---

## TL;DR

1. Buff163 là sàn skin lớn nhất, có **JSON API rõ ràng** dễ reverse-engineer nhưng **anti-bot mạnh**.
2. Phân biệt 4 entity: `goods` / `sell_order` / `buy_order` / `asset_info`. Float + sticker là chìa khoá arbitrage cao cấp.
3. Approach tốt nhất: **Hybrid Playwright (session) + httpx async + curl_cffi + residential proxy + 2Captcha fallback**.
4. **Đừng auto-buy ngay**. Detect → notify → manual confirm trong 3 tháng đầu.
5. Tech stack: **Python + FastAPI + PostgreSQL+TimescaleDB + Redis + Next.js**.
6. AI value: **Anomaly detection (mispricing sniping)** = ROI cao nhất, code dễ nhất. Price prediction để giai đoạn sau.
7. Risk lớn nhất: **bug logic** mất tiền + **account ban** mất balance. Guardrail nghiêm ngặt từ ngày 1.
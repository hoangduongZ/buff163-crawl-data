# Phân tích chuyên sâu về buff.163.com

---

## Tóm tắt điều hành

BUFF là marketplace giao dịch skin game do **NetEase** vận hành, nhắm tới người dùng trên nền tảng **Steam**, hỗ trợ các game như **Counter-Strike 2** và **Dota 2**.

Mô tả chính thức nhấn mạnh các tính năng: fast trade, giao hàng inventory-to-inventory, lọc theo sticker/thuộc tính, market trends, ảnh HD, 3D inspect, community, hỗ trợ 24/7 và skin rental — cho thấy đây là một nền tảng P2P đầy đủ, có lớp tài khoản, thanh toán và vận hành giao dịch rõ ràng.

### Kiến trúc kỹ thuật tổng quan

Site hoạt động theo mô hình **HTML shell + JS + XHR**:

- Trang item redirect từ `/goods/{id}` → `/s/goods.html?game=...&goods_id=...`
- Dữ liệu được tải động từ các JSON endpoint như `/api/market/goods/info` và `/api/market/goods/sell_order`
- Bundle tĩnh quan sát được: `style.min.css`, `lib.min.js`, `app.min.js`, `marcket.js`
- Frontend dùng thư viện legacy: Zepto, FastClick, ClipboardJS, client-side templating
- Header server: `nginx/1.13.5`, `X-Trace-ID`, `ntes-trace-id`, `x-envoy-upstream-service-time`
- Cookie quan sát được: `client_id`, `Device-Id`, `csrf_token`

> **Không có tài liệu API công khai chính thức.** Các endpoint được trace từ tab Network của trình duyệt.

### Khuyến nghị kiến trúc tổng thể

**Hybrid architecture** là lựa chọn tốt nhất cho production:

- **Browser thật / headless browser** → chỉ dùng để bootstrap session đăng nhập và xử lý challenge
- **JSON polling** → toàn bộ pipeline đọc dữ liệu thị trường, có jitter, cache-busting, xác nhận hai bước

> Hiện **không có bằng chứng WebSocket hay SSE** trong các trace quan sát được — tối ưu cho polling thông minh thay vì kênh push.

---

## Sản phẩm, mô hình kinh doanh và luồng người dùng

BUFF kiếm tiền từ hai lớp:

1. **Marketplace core** — kết nối người bán/người mua, tìm kiếm, so sánh, theo dõi xu hướng, giao hàng inventory-to-inventory
2. **Dịch vụ gia tăng** — gói **BUFF Plus** (in-app purchase), rental, phân loại nâng cao, market trends, ảnh HD, 3D inspect, community

App privacy disclosure xác nhận hệ thống xử lý: payment info, financial info, phone number, name, user ID, device ID — phù hợp với một nền tảng có ví/số dư/giao dịch thực.

> **Biểu phí hiện tại chưa xác minh được từ first-party source.** Nguồn thứ cấp mâu thuẫn: có nguồn nói seller fee ~2.5%, buyer fee 0%; có nguồn nói 2.5% cho cả hai phía. Hãy coi phí là **biến cấu hình cần kiểm chứng lại** thay vì hard-code.

### Luồng người dùng và hàm ý triển khai

| Luồng | Bề mặt web | Hàm ý triển khai |
|---|---|---|
| Duyệt thị trường | `/market/csgo#tab=selling&page_num=1` + `/api/market/goods` | Crawl bằng JSON trước, không parse DOM khi không cần |
| Tìm kiếm/lọc | Query params: `page_num`, `page_size`, `use_suggestion`, `min_price`, `max_price`, `category`, `sort_by`; có `Locale-Supported=en` | Chuẩn hóa filter dạng object; kiểm tra edge cases theo locale/game |
| Xem item | `/goods/{id}` → `/s/goods.html?...`; XHR gọi `/api/market/goods/info` | Item page là shell mỏng, detail ở JSON |
| Xem bên bán | `/api/market/goods/sell_order` | Lưu snapshot ask book theo thời gian |
| Xem bên mua | `/api/market/goods/buy_order` | Lưu snapshot bid book theo thời gian |
| Lịch sử khớp lệnh | `/api/market/goods/bill_order` | Cần auth — tách collector này khỏi collector công khai |
| Đăng nhập/tài khoản | Login UI có thể trong `iframe`; có lỗi SMS và "too many login failures" | Browser automation phải xử lý iframe và fallback thủ công |
| Ví/giao dịch | Có lớp payment/financial data; endpoint ví chưa lộ trong trace | Cần network trace riêng trên tài khoản của bạn |

> **Read flow** có thể xây ổn định bằng JSON endpoints. **Write flow** cần browser session thật và lớp phê duyệt từ con người.

---

## Kiến trúc site và chỉ dấu kỹ thuật

### Cơ chế render dữ liệu

BUFF **không render dữ liệu item bằng HTML server-side**. Trace một item page TF2 cho thấy chuỗi:

```
/goods/798088  →  /s/goods.html?game=tf2&goods_id=798088
    ↓ XHR
/api/market/goods/info?game=tf2&goods_id=798088
/api/market/goods/sell_order?game=tf2&goods_id=798088&page_num=1&page_size=20
```

HTML chính chỉ là **vỏ bọc** — toàn bộ dữ liệu giá và depth nằm ở JSON layer.

### Bundle và global variables

```
style.min.css  |  lib.min.js  |  app.min.js  |  marcket.js?20220706
```

Global variables trên `window`: `Zepto`, `$`, `template`, `FastClick`, `ClipboardJS`, `i18n`, `I18N`, `Popup`, `BUFFAPP`, `_zid`, `launchData`

→ Frontend kiểu legacy/minified custom, dùng thư viện nhỏ và client-side templating, **không phải SPA React/Vue/Angular**.

### Hạ tầng

- **2023**: `nginx/1.13.5` + IP AWS Dublin (trang chính); media qua `g.fp.ps.netease.com` và `market.fp.ps.netease.com`
- **2025**: Domain phân giải sang NetEase-network ở Hàng Châu (`buff-cn.ntes53.netease.com`)

> Site có thể dùng fronting theo vùng hoặc CDN. **Không nên khóa logic giám sát vào một IP/ASN cố định.**

### Sơ đồ kiến trúc quan sát được

```
Trình duyệt
    │
    ├── buff.163.com (HTML shell)
    │       ├── /css/style.min.css
    │       ├── /js/lib.min.js
    │       ├── /js/app.min.js
    │       └── /js/marcket.js
    │               ├── XHR → /api/market/goods/info
    │               └── XHR → /api/market/goods/sell_order
    │
    ├── g.fp.ps.netease.com   (media)
    └── market.fp.ps.netease.com (media)

Cookie jar: client_id | Device-Id | csrf_token
```

---

## API công khai, dữ liệu động và xác thực

### Bảng endpoint

| Endpoint | Công dụng | Tham số nổi bật | Auth |
|---|---|---|---|
| `/api/market/goods` | Danh sách item / browse / search | `game`, `page_num`, `page_size`, `use_suggestion`, `min_price`, `max_price`, `category`, `sort_by` | Biến thiên |
| `/api/market/goods/info` | Chi tiết item | `game`, `goods_id` | Có vẻ công khai |
| `/api/market/goods/sell_order` | Sổ lệnh bán / ask depth | `game`, `goods_id`, `page_num`, `page_size`, `_` | Có thể public |
| `/api/market/goods/buy_order` | Sổ lệnh mua / bid depth | `game`, `goods_id`, `page_num`, `_` | Biến thiên |
| `/api/market/goods/bill_order` | Lịch sử khớp lệnh | `game`, `goods_id` | **Bắt buộc** |
| `/api/market/goods/price_history/buff` | Lịch sử giá | `game`, `goods_id`, `currency`, `days`, `buff_price_type`, `_` | Chưa xác minh |

### Response shape mẫu

**Market list** (`/api/market/goods`):

```json
{
  "code": "OK",
  "data": {
    "items": [
      {
        "id": 35803,
        "name": "AK-47 | ...",
        "market_hash_name": "AK-47 | ...",
        "quick_price": "29.89",
        "sell_min_price": "29.89",
        "buy_max_price": "28.50",
        "sell_num": 321,
        "buy_num": 45,
        "transacted_num": 912,
        "goods_info": {
          "icon_url": "https://...",
          "steam_price": "33.21",
          "steam_price_cny": "240.00",
          "info": {
            "tags": {
              "rarity": {},
              "quality": {},
              "type": {},
              "weapon": {},
              "exterior": {}
            }
          }
        }
      }
    ]
  }
}
```

**Buy order** (`/api/market/goods/buy_order`):

```json
{
  "data": {
    "items": [
      { "price": "1.2" },
      { "price": "1.1" }
    ]
  }
}
```

**Bill order khi chưa đăng nhập** (`/api/market/goods/bill_order`):

```json
{
  "code": "Login Required",
  "error": "请先登录",
  "extra": null
}
```

### Freshness và cache-busting

Public examples thêm tham số `_={epoch_ms}` vào `buy_order`/`sell_order`. Tuy vậy, có báo cáo `sell_order` trả dữ liệu chậm tới ~5 phút khi request qua proxy dù đã thêm timestamp.

> `_` là **gợi ý freshness**, không phải SLA. Pipeline giao dịch **phải đọc lại lần cuối trước khi hành động**.

### Cookie jar hợp lệ

| Nguồn | Cookies |
|---|---|
| Item page công khai | `client_id`, `Device-Id`, `csrf_token` |
| Public examples | `Locale-Supported=en`, `game=csgo`, `session`, `csrf_token`, `Device-Id` |
| Wrapper README | Thêm: `NTES_YD_SESS`, `S_INFO`, `P_INFO`, `remember_me` |

> Session hợp lệ không chỉ là một cookie `session` — đó là cả **cookie jar ràng buộc locale, device và CSRF state**.

---

## Chống bot, rào cản vận hành và ràng buộc pháp lý

### Tín hiệu chống bot quan sát được

- Cookie `Device-Id` và host `g.fp.ps.netease.com`, `market.fp.ps.netease.com` → **dấu hiệu fingerprinting/telemetry**
- Login trong iframe
- Lỗi "too many login failures" (ghi nhận trong App Store review)
- Cảnh báo cộng đồng: request quá dày có thể dẫn tới **ban tài khoản**

> Trong trace hiện có, **không có bằng chứng rõ ràng BUFF front door dùng Cloudflare**. Rủi ro thực tế hơn là throttle theo thiết bị/phiên, stale cache, iframe login, SMS friction và account-level abuse controls.

### Tình trạng pháp lý

**ToS hiện hành, robots.txt và privacy policy body chưa xác minh được** từ first-party source trong pass này. Mọi automation nên được coi là **rủi ro pháp lý/tuân thủ chưa làm rõ**, không phải quyền mặc định.

### Bảng so sánh phương án crawl

| Phương án | Khi nên dùng | Ưu điểm | Nhược điểm | Đánh giá |
|---|---|---|---|---|
| Direct API polling | Read-heavy watchlists, market snapshots | Nhanh, rẻ, dễ chuẩn hóa | Session hết hạn; freshness không tuyệt đối | ✅ **Ưu tiên số một** |
| Headless browser | Bootstrap login, iframe, semi-auto write | Bám hành vi user thật | Tốn tài nguyên, dễ vỡ khi UI đổi | ✅ **Chỉ dùng khi cần** |
| Hybrid | Session bootstrap bằng browser + data bằng API polling | Cân bằng tốt nhất | Phức tạp hơn | ✅ **Khuyến nghị production** |
| WebSocket client | Khi trace phát hiện WS thật | Latency tốt | Chưa có bằng chứng WS | ⏸ **Chưa nên đầu tư** |
| SSE client | Khi trace phát hiện SSE | Triển khai gọn | Chưa có bằng chứng SSE | ⏸ **Chưa nên đầu tư** |
| Proxy / rotating IPs | Chỉ cho tải hợp lệ đã review pháp lý | Tách tải | Rủi ro compliance cao | ❌ **Không khuyến nghị** |

---

## Kiến trúc ứng dụng tự động hóa, mô hình dữ liệu và tích hợp AI

### Schema database gợi ý

| Bảng | Cột chính | Mục đích |
|---|---|---|
| `items` | `item_id`, `game`, `name`, `market_hash_name`, `tags_json`, `icon_url`, `steam_price`, `steam_price_cny`, `updated_at` | Hồ sơ chuẩn hóa của item |
| `market_snapshots` | `snapshot_id`, `item_id`, `observed_at`, `quick_price`, `sell_min_price`, `buy_max_price`, `sell_num`, `buy_num`, `transacted_num`, `recent_sold_count`, `raw_json` | Snapshot top-level theo thời gian |
| `sell_orders` | `snapshot_id`, `item_id`, `observed_at`, `price`, `quantity`, `paintwear_nullable`, `paintseed_nullable`, `cooldown_nullable`, `attrs_json` | Ask side depth / listing details |
| `buy_orders` | `snapshot_id`, `item_id`, `observed_at`, `price`, `quantity`, `attrs_json` | Bid side depth |
| `sales_history` | `trade_row_id`, `item_id`, `sold_at`, `price`, `quantity`, `attrs_json` | Lịch sử khớp lệnh để tính fair value |
| `account_events` | `event_id`, `event_type`, `ts`, `item_id_nullable`, `amount_cny_nullable`, `status`, `request_trace_id`, `details_json` | Audit trail cho mọi thao tác |
| `model_scores` | `score_id`, `item_id`, `ts`, `fair_value`, `anomaly_score`, `liquidity_score`, `edge_net`, `features_json`, `model_version` | Lưu inference và backtest trace |

> Thiết kế theo hướng **event-sourced snapshots** thay vì "một bảng giá hiện tại" — tín hiệu giao dịch nằm ở biến động theo thời gian.

### Luồng kiến trúc hệ thống

```
Browser bootstrap (login / iframe / manual challenge)
    │
    ▼
Cookie vault
    │
    ▼
API pollers (watchlists + snapshots)
    │
    ▼
Raw event queue → Normalizer → PostgreSQL / Timescale
                                        │
                                        ▼
                              Feature views → AI / Signal engine
                                                    │
                                                    ▼
                                            Risk engine
                                                    │
                              ┌─────────────────────┤
                              ▼                     ▼
                         Alert only        Operator approval
                                                    │
                                                    ▼
                              Browser execution worker → Execution ledger
```

### Chiến lược trading theo 3 lớp

**Lớp 1 — Stat-arb read-only** (dễ nhất, bắt đầu ở đây)

Phát hiện listing rẻ bất thường so với fair value nội bộ từ price history, top-of-book, recent sold count và trend ngắn hạn. Chưa cần auto-buy — chỉ alert và human review. Phù hợp cho **anomaly detection**.

**Lớp 2 — Microstructure strategy**

Dùng bid/ask imbalance, tốc độ cạn top ask, spread giữa `sell_min_price` và `buy_max_price`, cùng listing attributes (paintwear, sticker combinations). Công thức quyết định:

```
edge_net = fair_value_exit - entry_cost - fees - fx_cost - slippage - settlement_risk
```

**Lớp 3 — Cross-market strategy**

BUFF là price reference chuẩn trong cộng đồng skin trading. Lợi thế không nằm ở microseconds mà ở **lọc đúng item có thanh khoản + xác nhận nhanh trước execution**. Nếu chưa có write endpoint hợp lệ, dừng ở alerting hoặc browser-assisted execution.

### Phân công tích hợp AI

- **Price prediction** — ước lượng fair value / ngưỡng exit cho từng item và biến thể
- **Anomaly detection** — tìm listing rẻ bất thường, data corruption, stale snapshot, spoof-like depth
- **Repricing bot** — nếu có write flow hợp lệ, đề xuất giá mục tiêu (không auto-submit)
- **Computer vision** (tùy chọn) — nếu có ảnh HD/inspect assets trong luồng hợp lệ, trích đặc trưng sticker/wear vị trí

---

## Kế hoạch triển khai

### Roadmap

| Mốc | Deliverable | Effort |
|---|---|---|
| Khung pháp lý + baseline trace | Xác minh ToS/robots, chụp network trace (browse / detail / orderbook / wallet) | Thấp |
| Session bootstrap + read crawler | Cookie vault, API clients cho goods/info/sell_order/buy_order, retry/backoff/jitter | Trung bình |
| Chuẩn hóa dữ liệu + lưu trữ | DB schema, raw JSON archive, dedupe, timestamping, materialized views | Trung bình |
| Watchlists + cảnh báo | Hot-item selectors, freshness SLA, alert trên spread/anomaly/volume shock | Trung bình |
| Browser fallback | Login iframe handling, manual challenge flow, DOM monitors, screenshot audit | Trung bình |
| Strategy engine + backtest | Fair-value model, anomaly model, cost/slippage engine, PnL simulator | Cao |
| Pilot semi-auto execution | Human approval queue, browser-assisted submit, audit ledger, kill-switch | Cao |
| Hardening production | Metrics, tracing, on-call alerts, secret rotation, budget guardrails | Trung bình |

### Ước tính chi phí (minh họa)

| Quy mô | Thành phần | Ước tính/tháng |
|---|---|---|
| Lab | 1 API worker + 1 Postgres nhỏ + dashboard | ~vài chục USD |
| Pilot | 2 API workers + 1 browser worker + managed DB + alerting | ~thấp đến vài trăm USD |
| Production có dự phòng | Queue + 4–10 workers + 1–2 browser workers + HA DB + object storage + tracing | ~từ vài trăm USD trở lên |

### Code mẫu — Session reuse cho read flow

```python
import requests

def build_session(cookie_dict: dict) -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://buff.163.com/market/csgo#tab=selling&page_num=1",
        "Accept": "application/json, text/plain, */*",
    })
    for k, v in cookie_dict.items():
        s.cookies.set(k, v, domain="buff.163.com")
    return s

session = build_session({
    "session": "...",
    "csrf_token": "...",
    "Device-Id": "...",
    "Locale-Supported": "en",
    "game": "csgo",
})

resp = session.get(
    "https://buff.163.com/api/market/goods",
    params={"game": "csgo", "page_num": 1, "use_suggestion": 0},
    timeout=15,
)
resp.raise_for_status()
items = resp.json().get("data", {}).get("items", [])
```

### Code mẫu — Fetch order book

```python
import time

def fetch_orderbook(session, goods_id: int, game: str = "csgo", page_size: int = 20):
    now_ms = int(time.time() * 1000)

    asks = session.get(
        "https://buff.163.com/api/market/goods/sell_order",
        params={
            "game": game, "goods_id": goods_id,
            "page_num": 1, "page_size": page_size, "_": now_ms,
        },
        timeout=15,
    ).json()

    bids = session.get(
        "https://buff.163.com/api/market/goods/buy_order",
        params={
            "game": game, "goods_id": goods_id,
            "page_num": 1, "_": now_ms,
        },
        timeout=15,
    ).json()

    return {
        "ts_ms": now_ms,
        "asks": asks.get("data", {}).get("items", []),
        "bids": bids.get("data", {}).get("items", []),
    }
```

### Pseudocode — Browser execution (write flow)

```python
# PSEUDOCODE ONLY — write endpoint chưa được xác minh
def submit_buy_via_browser(page, goods_id: int, max_entry_price: float):
    page.goto(f"https://buff.163.com/goods/{goods_id}?from=market#tab=selling")

    latest_price = read_lowest_listing_price(page)
    if latest_price is None:
        return {"status": "error", "reason": "price_not_found"}

    if latest_price > max_entry_price:
        return {"status": "skip", "reason": "price_moved"}

    click_buy_button(page)
    tick_required_confirmations(page)

    if challenge_detected(page):
        notify_operator("manual challenge required")
        page.pause()  # human solves in owned session

    click_final_confirm(page)
    return {"status": "submitted", "result": read_submission_result(page)}
```

### Pseudocode — Challenge handler

```python
# PSEUDOCODE ONLY
def handle_challenge(page):
    if challenge_detected(page):
        record_account_event("manual_challenge_required")
        send_alert("Please solve the verification challenge in the browser.")
        page.pause()  # human-in-the-loop, không bypass
```

---

## Rủi ro vận hành và cách giảm thiểu

| Rủi ro | Vì sao đáng ngại | Giảm thiểu |
|---|---|---|
| ToS/robots chưa xác minh | Bot hợp lệ về kỹ thuật nhưng rủi ro tuân thủ | Xác minh first-party terms trước production; giữ mode alert/semi-auto |
| Session leak / cookie theft | Cookie jar = khóa tài khoản | Mã hóa secrets, chỉ nạp runtime, không ghi log cookie, rotate định kỳ |
| Login throttling / lockout | Public evidence về "too many login failures" | Đăng nhập ít lần, tái sử dụng session, tách bootstrap khỏi read workers |
| Dữ liệu stale | sell_order bị trễ nhiều phút (public report) | Re-read trước decision, xác nhận 2 bước, đánh dấu freshness SLA |
| DOM drift | Browser automation vỡ khi UI đổi | Giữ browser chỉ cho phần cần thiết; mọi read flow đi JSON |
| Model false positives | Giá rẻ chưa chắc mua được hoặc thoát được | Dùng risk engine, min liquidity, max slippage, cooldown filter |
| Settlement risk | Giao dịch inventory-to-inventory có độ trễ và bất thường | Chỉ semi-auto giai đoạn đầu; giữ audit ledger và manual override |
| Account ban / abuse flag | Poll quá dày hoặc hành vi bất thường | Watchlist, jitter, backoff, không flood, không stealth-evasion |

---

## Câu hỏi mở và giới hạn của pass nghiên cứu này

Có bốn giới hạn quan trọng cần xử lý trong giai đoạn discovery nội bộ:

**1. Không replay trực tiếp được request tới BUFF** — Kết luận kỹ thuật dựa trên tổ hợp App Store listing chính thức, archived network trace, tài liệu wrapper không chính thức và public network examples. Độ tự tin cao với read surface, thấp hơn nhiều với write surface.

**2. ToS, robots.txt và privacy policy body chưa xác minh được** — Phần legal/contractual được đánh dấu là **unspecified**. Quyền crawl/auto-trading hiện hành chưa có căn cứ first-party.

**3. Không có bằng chứng WebSocket/SSE trong trace** — Không chứng minh triệt để site không dùng chúng. Nếu sau này trace phát hiện WS ở màn wallet/notifications/live-trade, kiến trúc collector cần bổ sung.

**4. Biểu phí và wallet endpoints vẫn là vùng mờ** — Nguồn bên ngoài mâu thuẫn; wallet flow không lộ trong trace công khai.

### Bước tiếp theo được khuyến nghị

Trước khi viết bất kỳ chiến lược tự động nào, hãy tự tạo một **Network Trace Workbook** trên tài khoản của bạn, bao gồm:

- Browse market
- Item detail
- Buy flow / sell flow
- Wallet / balance / deposit / withdraw
- History
- Challenge / captcha
- Error states

Sau khi có workbook đó, bạn sẽ biết rõ ranh giới nào đọc thẳng bằng API, ranh giới nào phải bám browser, và ranh giới nào tốt nhất nên để con người duyệt.
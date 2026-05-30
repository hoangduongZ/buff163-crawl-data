# Buff163 Sniper Tool — Feature Spec & Architecture

> **User**: 1 người (bạn)
> **Goal**: Phát hiện sell order giá thấp bất thường trên Buff → notify trong giây → click mua trước người khác
> **Platform**: Macbook M1 Pro (16GB RAM, 8/10 core)
> **Triết lý**: Thực dụng, đơn giản, làm xong dùng được — không enterprise, không over-engineer

---

## 1. Hiểu đúng bài toán — đây là Sniping, không phải Analytics

| Sniping Tool (cần làm) | Analytics Tool (đã làm trước) |
|---|---|
| Theo dõi watchlist 50-200 item bạn quan tâm | Scan toàn market 50k+ items |
| Tần suất check: 5-30 giây/item | 10-30 phút/cycle |
| Latency từ "phát hiện" → "notify" < 5 giây | Tổng hợp report cuối ngày |
| Action: bấm mua ngay (manual hoặc auto) | Action: đọc dashboard, ra quyết định chậm |
| Quét đến level **sell_order** (float, sticker cụ thể) | Đến level **goods** (giá min của loại) đủ rồi |
| Anti-bot evasion là sống còn | Tolerance cao hơn |

→ Tài liệu này design **chỉ** cho sniping. Analytics có thể chạy song song nhưng tách biệt.

---

## 2. Tính năng cần có — phân theo 3 priority

### 🔴 P0 — MUST HAVE (MVP, làm trước)

#### F1. Watchlist management
Bạn chỉ định **danh sách item cần theo dõi**, lưu trong file YAML đơn giản:

```yaml
# watchlist.yaml
items:
  - goods_id: 33453
    name: "AK-47 | Redline (FT)"
    max_buy_price_cny: 90.0           # giá tối đa chấp nhận
    min_float: null                    # filter optional
    max_float: 0.20
    require_no_stickers: false
    notes: "wait for drop dưới 90"

  - goods_id: 776543
    name: "AWP | Asiimov (BS)"
    max_buy_price_cny: 250.0
    notes: "spread vs Skinport ~30%"
```

Lý do dùng YAML không phải JSON: comment được, edit thoải mái, không quote nhiều.

**Workflow**: bạn duyệt buff.163.com, copy goods_id từ URL, paste vào yaml, đặt max price. Tool tự động lo phần còn lại.

#### F2. Tiered polling — không scan ngu

Không thể scan 200 items mỗi 5 giây — Buff sẽ ban. Phải tier:

```
Hot tier (top 20 items quan tâm nhất):  poll mỗi 10-15 giây
Warm tier (50 items kế tiếp):           poll mỗi 60 giây
Cold tier (rest):                       poll mỗi 5 phút
```

**Logic auto-promote**: item nào vừa đổi giá → tự động nhảy lên Hot tier 1 giờ tiếp theo. Item Hot tier không đổi giá 30 phút → demote xuống Warm.

→ Đây là điểm khác biệt lớn nhất giữa "tool nghiệp dư" và "tool dùng được".

#### F3. Sell order level monitoring

Không chỉ check `sell_min_price` (số tổng). Phải gọi `/api/market/goods/sell_order` để **lấy danh sách sell orders thật**, vì:

- Cùng 1 goods, có sell order $90 (newbie list rẻ) và $120 (giá thị trường)
- Bạn cần `sell_order_id` để mua chính xác cây đó
- Phải đọc float, sticker, paintseed để verify trước khi alert

#### F4. Smart alerting — không spam

Alert thoả MỌI điều kiện:
- Giá ≤ `max_buy_price_cny` đã set
- Float trong range cho phép
- KHÔNG đã alert sell_order_id này rồi (deduplicate)
- Item còn `state == 1` (chưa bị mua)
- KHÔNG có `tradable_cooldown_text` (trừ khi bạn cho phép)

**Critical**: dedupe theo `sell_order_id`, không phải theo goods_id. Cùng 1 goods có thể có 5 sell orders rẻ cùng lúc → cần alert hết 5 cái, mỗi cái 1 lần.

#### F5. macOS native notification

Trên M1 dùng `osascript` hoặc `pync` để bắn notification system:

```
🚨 Buff Snipe — AK Redline FT
   85 CNY (target: 90) — float 0.16
   [Click để mở browser]
```

Click vào notification → mở thẳng `https://buff.163.com/goods/33453?...&sell_order_id=xxx`.

#### F6. Audio alert (optional, nhưng khuyến nghị)

Notification dễ miss. Thêm beep system khi có alert tier cao (giá cực rẻ, vd ≤ 70% max_buy_price). M1 dùng `afplay /System/Library/Sounds/Glass.aiff` hoặc tương tự.

#### F7. Persistence — không bỏ lỡ alert khi máy tắt

Lưu state trên disk:
- `state.json` — last_seen_price của từng goods (để diff)
- `alerts_seen.json` — set sell_order_id đã alert (tránh spam khi restart)
- `alerts_history.jsonl` — log hết alert (đêm xem lại)

#### F8. Retry với exponential backoff + circuit breaker

Khi Buff trả 429/403/captcha → tự động:
- Retry 3 lần với delay 5s, 15s, 45s
- Sau 3 fail → pause 5 phút, không retry
- Notification cho bạn biết "tool đang bị throttle, paused"

#### F9. CLI đơn giản

```bash
sniper start              # chạy daemon
sniper start --watchlist ak.yaml
sniper status             # xem đang track gì, last poll khi nào
sniper recent             # 10 alert gần nhất
sniper add 33453 --max 90 # thêm item nhanh
sniper test               # smoke test 1 item, không loop
```

---

### 🟡 P1 — SHOULD HAVE (làm sau khi P0 ổn 1-2 tuần)

#### F10. Telegram notification — quan trọng khi không ngồi máy

Notification macOS chỉ làm việc khi máy không sleep. Telegram bot push lên phone:
- Setup: tạo bot qua @BotFather, lấy token, ~10 phút
- Có nút "Open in Buff" inline để bấm 1 phát mở browser/app
- Free, reliable hơn email

#### F11. Multi-channel notification routing

```yaml
notifications:
  default:
    - macos
    - log
  high_priority:        # khi giá ≤ 70% max
    - macos
    - audio
    - telegram
  critical:             # khi giá ≤ 50% max (rare deal)
    - macos
    - audio
    - telegram
    - sms             # qua Twilio nếu có
```

#### F12. Statistical anomaly detection

Thay vì chỉ check giá < threshold, tính **z-score** trên giá 100 sell orders gần nhất cùng goods. Khi z-score < -2.5 → alert "underpriced" kể cả không hit threshold.

Catch case: bạn set threshold 90, nhưng giá thị trường vừa tăng lên 130 → có cây 100 cũng là deal mà threshold không bắt.

#### F13. Steam price comparison

Trong alert hiển thị luôn:
```
Buff:    85 CNY  (~$11.80)
Steam:   $14.20 (~$12.07 sau phí 15%)
Spread:  +2.3% — meh deal
```

→ Giúp ra quyết định nhanh hơn, không cần mở tab khác check.

#### F14. Float/Sticker filter chi tiết

Trong watchlist:
```yaml
- goods_id: 33453
  max_buy_price_cny: 90.0
  filters:
    max_float: 0.18
    min_float: 0.16          # hunting low-float
    require_stickers:
      - "Katowice 2014"      # sticker rare
    blacklist_paintseed: [661]  # avoid common pattern
    require_paintseed: [387]    # blue gem #387
```

#### F15. Auto-snooze khi không có signal

Item Cold tier 3 ngày không có alert → tự động giảm priority + warn bạn "có muốn bỏ track không?". Tránh watchlist phình to vô dụng.

#### F16. Web dashboard (Streamlit)

Streamlit = Python lib viết dashboard 50 dòng có UI. Lý tưởng cho 1 user, không cần Next.js:

```
http://localhost:8501

[ Status: Running, last poll 4s ago ]
[ Watchlist: 47 items, 3 alerts last hour ]

Recent Alerts table
Watchlist editor (chỉnh inline, save trực tiếp file YAML)
Price history chart (Lightweight Charts hoặc plotly)
```

Streamlit auto-reload khi đổi code, dev cực nhanh.

---

### 🟢 P2 — NICE TO HAVE (sau 1+ tháng dùng)

#### F17. Auto-buy với guardrails (RỦI RO CAO)

Cho phép tool tự click mua khi:
- Giá ≤ X% max_buy_price (vd ≤ 60%)
- Float trong sweet spot (vd 0.15-0.18)
- Tổng spend hôm nay < $Y (kill switch)
- Account có đủ balance
- Không phải first-time alert (dedupe khi reload)

**WARNING**: Auto-buy cần cookie session valid + CSRF token + có thể trigger captcha → fail rate cao. KHÔNG khuyên làm trước 3 tháng.

#### F18. Pricempire/CSFloat cross-check

Trước khi alert, query API bên thứ 3 để check giá trên Skinport, CSFloat, DMarket. Tính ROI Buff→Sell platform thực sự, không chỉ Steam.

#### F19. ML-based anomaly detection

Thay z-score đơn giản:
- Isolation Forest trên feature `(price, float, sticker_premium, time_of_day, day_of_week)`
- Train hàng ngày trên data 30 ngày gần nhất
- Score "rarity" của mỗi sell order → ưu tiên alert

→ Đáng làm khi đã có 3 tháng dữ liệu.

#### F20. Multi-account session pool

Nếu 1 account/cookie bị throttle → switch sang account khác. Cần 3-5 Buff accounts (rủi ro ToS).

---

## 3. Architecture đề xuất

### 3.1 Tổng thể — single-process, async, file-based persistence

```
┌─────────────────────────────────────────────────────────┐
│                    sniper (Python process)              │
│                                                         │
│  ┌──────────────┐    ┌──────────────┐                 │
│  │ Watchlist    │───►│ Scheduler    │  tier-aware     │
│  │ Loader (YAML)│    │ (asyncio)    │  polling        │
│  └──────────────┘    └──────┬───────┘                 │
│                             │                          │
│                             ▼                          │
│                   ┌──────────────────┐                 │
│                   │ HTTP Client      │ curl_cffi      │
│                   │ + retry/backoff  │ + cookie pool  │
│                   └──────┬───────────┘                 │
│                          │                             │
│                          ▼                             │
│                   ┌──────────────────┐                 │
│                   │ Order Diff Engine│                 │
│                   │ (detect new low) │                 │
│                   └──────┬───────────┘                 │
│                          │                             │
│                          ▼                             │
│                   ┌──────────────────┐                 │
│                   │ Alert Filter     │ check criteria  │
│                   │ + Deduplicator   │                 │
│                   └──────┬───────────┘                 │
│                          │                             │
│                          ▼                             │
│             ┌────────────┴────────────┐               │
│             ▼            ▼            ▼               │
│         macOS        Telegram      JSONL              │
│         notify       (P1)          log                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │ Streamlit UI │ tách process, đọc    │
                  │ (P1)         │ shared file          │
                  └──────────────┘
```

**Quyết định**:
- **Single process** với asyncio — không Celery/Redis. Vì sao: M1 Pro 16GB thừa sức, 1 user, 200 item; thêm broker phức tạp không lợi gì
- **File-based persistence** — JSON/YAML/JSONL. Không Postgres/SQLite vì size data nhỏ, file system M1 NVMe nhanh hơn DB ở scale này
- **Streamlit dashboard** chạy tách process, đọc cùng file → hot reload khi watchlist đổi

### 3.2 Project structure

```
buff_sniper/
├── pyproject.toml              # dependencies (modern thay requirements.txt)
├── README.md
├── config/
│   ├── watchlist.yaml          # bạn edit cái này nhiều nhất
│   ├── settings.yaml           # tier intervals, thresholds, notification config
│   └── cookie.txt              # cookie từ browser (gitignored)
├── data/
│   ├── state.json              # current state mỗi item
│   ├── alerts_seen.json        # dedupe set
│   ├── alerts_history.jsonl    # log alerts
│   └── snapshots/              # raw snapshots (debug)
├── src/
│   ├── __init__.py
│   ├── main.py                 # entry point CLI
│   ├── config.py               # load YAML config
│   ├── watchlist.py            # watchlist + tier logic
│   ├── client.py               # curl_cffi wrapper, retry
│   ├── poller.py               # main polling loop (asyncio)
│   ├── differ.py               # detect price changes / new orders
│   ├── filters.py              # alert criteria checks
│   ├── notifiers/
│   │   ├── __init__.py
│   │   ├── base.py             # interface
│   │   ├── macos.py            # osascript
│   │   ├── audio.py            # afplay
│   │   ├── telegram.py         # python-telegram-bot
│   │   └── log.py              # JSONL writer
│   └── dashboard.py            # streamlit (chạy: streamlit run dashboard.py)
├── tests/
│   ├── test_differ.py
│   ├── test_filters.py
│   └── test_watchlist.py
└── scripts/
    ├── add_item.py             # quick CLI: thêm item vào watchlist
    └── export_alerts.py        # export alerts CSV
```

→ Không cần "đầy đủ tất cả file" ngay. MVP chỉ cần `main.py` + `client.py` + `differ.py` + `notifiers/macos.py`. File khác thêm dần khi đau.

### 3.3 Data flow chi tiết — 1 cycle polling

```
1. Scheduler tick → "tới giờ poll item X (tier Hot)"
2. Client: GET /api/market/goods/sell_order?goods_id=X&page=1&sort=price.asc
   - Header: cookie từ pool, Chrome impersonate
   - Timeout 20s, retry 3 lần
3. Parse response → list 20 sell_orders sort theo giá tăng
4. Differ:
   - Load previous state[X] = {top_3_orders: [...], min_price: 87.50}
   - Compare với current top 3
   - Detect: order_id mới nào xuất hiện trong top, hoặc giá min giảm
5. Filter (cho mỗi order mới phát hiện):
   - price ≤ watchlist[X].max_buy_price?
   - float trong range?
   - sticker requirements OK?
   - sell_order_id chưa từng alert?
   - state == 1 (active)?
6. Notify (qua các channels theo priority):
   - Build message với context (giá, float, URL deep-link)
   - Send macOS notification
   - Append to alerts_history.jsonl
   - Mark sell_order_id vào alerts_seen
7. Update state[X] = current top 3
8. Schedule next poll cho X (tăng frequency nếu vừa có alert)
```

**Latency target**: từ lúc Buff API trả response đến notification trên màn hình **< 500ms**. Step 4-7 toàn local, không network.

### 3.4 Concurrency model

```python
# Pseudocode
async def main():
    watchlist = load_watchlist()
    queue = PriorityQueue()
    for item in watchlist:
        queue.put((next_poll_time(item), item))
    
    semaphore = asyncio.Semaphore(3)   # max 3 concurrent HTTP calls
    
    while running:
        scheduled_time, item = await queue.get()
        if scheduled_time > now():
            await asyncio.sleep(scheduled_time - now())
        
        asyncio.create_task(process_item(item, semaphore))
        # re-schedule
        queue.put((now() + interval(item), item))
```

`Semaphore(3)` quan trọng: max 3 request đồng thời. Quá nhiều → trigger anti-bot. Đây là "rate limit local" trước cả khi Buff rate limit.

---

## 4. UX design — gì hiển thị cho bạn

### 4.1 Notification format (macOS)

```
🎯 BUFF SNIPE [HOT]
AK-47 | Redline (FT)
85.00 CNY (target: 90 / -5.6%)
Float: 0.1623  •  No stickers
[Open] [Snooze 1h] [Remove from watch]
```

Click → mở browser tới `https://buff.163.com/goods/33453?...&sell_order_id=20260426...`.

### 4.2 Telegram message format

```
🎯 BUFF SNIPE — AK Redline (FT)
━━━━━━━━━━━━━━━━━━━━
💰 Price: 85.00 CNY (~$11.80)
🎯 Target: 90 CNY (-5.6%)
📊 Steam: $14.20 (+20.3%)
🔍 Float: 0.1623
🏷️ Stickers: None
⏱️ Listed: 2 phút trước

[ 🛒 Open in Buff ]
```

Inline button → deep link.

### 4.3 Streamlit dashboard layout

```
┌─────────────────────────────────────────────┐
│ Status: 🟢 Running  •  Last poll: 3s ago    │
│ Active items: 47  •  Alerts last 24h: 12   │
└─────────────────────────────────────────────┘

┌────────── Watchlist ──────────┐ ┌── Recent Alerts ──┐
│ ☑ AK Redline FT  90 CNY  Hot │ │ 🎯 AK Redline 85  │
│ ☑ AWP Asiimov   250 CNY  Hot │ │    2 min ago      │
│ ☑ Karambit Doppler  ...      │ │ 🎯 AWP Asiimov 230│
│ [+ Add]                       │ │    18 min ago     │
└───────────────────────────────┘ └───────────────────┘

┌── Price History (selected: AK Redline FT) ──┐
│ [Lightweight Charts]                          │
│  100 ┤    ╱╲                                  │
│   90 ┤───╯  ╲___╱╲      ← target line         │
│   85 ┤            ╲___                        │
│      └─────────────────────                   │
│      24h ago              now                 │
└───────────────────────────────────────────────┘
```

→ Streamlit có sẵn component cho mọi thứ trên, viết trong 200 dòng.

---

## 5. Đặc thù tối ưu cho M1 Pro

M1 Pro có lợi thế cụ thể tận dụng được:

### 5.1 Native ARM Python — fast startup
- Cài Python qua Homebrew sẽ tự là arm64
- Verify: `python3 -c "import platform; print(platform.machine())"` → `arm64`
- `curl_cffi` có wheel ARM build sẵn từ v0.7+, không cần compile từ source

### 5.2 Background process với `launchd` (= cron của macOS)

Thay vì để terminal mở chạy daemon, dùng `launchd`:

```xml
<!-- ~/Library/LaunchAgents/com.you.buffsniper.plist -->
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.you.buffsniper</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/venv/bin/python</string>
        <string>/path/to/sniper/main.py</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>     <!-- restart nếu crash -->
    <key>StandardOutPath</key>
    <string>/tmp/buffsniper.log</string>
</dict>
</plist>
```

Activate: `launchctl load ~/Library/LaunchAgents/com.you.buffsniper.plist`.

→ Tool tự chạy khi mở máy, tự restart khi crash, không cần terminal.

### 5.3 macOS notification permission

Lần đầu chạy `osascript -e 'display notification ...'` → System sẽ hỏi cấp quyền. Approve trong System Settings > Notifications. **Quan trọng**: terminal app (iTerm2/Terminal) phải có quyền notification, không phải Python.

### 5.4 Power management — đừng để máy sleep mất alerts

Khi để tool chạy lâu:
- `caffeinate -i python main.py start` — prevent system idle sleep
- Hoặc System Settings > Battery > Prevent automatic sleeping

### 5.5 Resource budget thực tế trên M1 Pro 16GB

Tool này (200 items, polling 24/7) sẽ dùng:
- RAM: ~80-150MB (Python + curl_cffi + state)
- CPU: <1% average, peak 3-5% khi notify
- Network: ~10-30MB/giờ
- Disk: ~50MB/tháng (logs + snapshots với prune)

→ Hoàn toàn negligible trên M1 Pro. Có thể chạy song song với mọi development work.

---

## 6. Tech stack final

| Layer | Choice | Lý do |
|---|---|---|
| Language | Python 3.12 (arm64) | TLS bypass, ML-ready, dev tốc độ |
| HTTP | `curl_cffi` 0.7+ | TLS fingerprint impersonation |
| Async | `asyncio` (stdlib) | Không cần thêm framework |
| Config | `pyyaml` | Human-friendly hơn JSON |
| Validation | `pydantic` v2 | Type-safe config loading |
| CLI | `typer` | FastAPI-style CLI, đẹp hơn argparse |
| Logging | `loguru` | Đơn giản hơn logging stdlib 10x |
| macOS notif | `pync` hoặc `osascript` subprocess | Native |
| Telegram | `python-telegram-bot` | Standard |
| Dashboard | `streamlit` | 200 dòng có UI hoàn chỉnh |
| Charts | `plotly` (đi cùng streamlit) | Interactive |
| Process mgmt | `launchd` (macOS native) | Không cần Docker/systemd |
| Test | `pytest` | Standard |
| Format/lint | `ruff` | Cực nhanh, replace black+flake8+isort |

**Không dùng**:
- ~~Redis~~ — overkill cho 1 user
- ~~PostgreSQL/SQLite~~ — file JSON đủ, đơn giản hơn
- ~~Celery/RQ~~ — asyncio đủ
- ~~Docker~~ — chạy local M1, không cần containerize
- ~~FastAPI~~ — chưa cần REST API, Streamlit đủ
- ~~Selenium/Playwright~~ — chỉ dùng nếu curl_cffi fail (fallback later)

---

## 7. Dependency list (`pyproject.toml`)

```toml
[project]
name = "buff-sniper"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "curl_cffi>=0.7.0",
    "pyyaml>=6.0",
    "pydantic>=2.5",
    "typer>=0.9",
    "loguru>=0.7",
    "pync>=2.0",                  # macOS notification
    "python-telegram-bot>=20.7",  # P1
    "streamlit>=1.30",            # P1
    "plotly>=5.18",               # P1
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-asyncio>=0.23",
    "ruff>=0.1.9",
]

[project.scripts]
sniper = "buff_sniper.main:app"
```

Cài: `pip install -e .` (editable mode, sửa code không cần re-install).

---

## 8. Implementation roadmap — thực tế

### Tuần 1: MVP polling
- [ ] Setup project structure + pyproject.toml + venv
- [ ] `client.py`: curl_cffi wrapper + retry, gọi được sell_order endpoint
- [ ] `watchlist.py`: load YAML
- [ ] `differ.py`: so sánh top 3 sell orders, detect order mới
- [ ] `main.py`: CLI `sniper start`, vòng lặp đơn giản 60s/item
- [ ] Test với 5-10 items thật
- [ ] **Acceptance**: Khi có sell order mới giá < threshold, tool log ra console

### Tuần 2: Notification + reliability
- [ ] `notifiers/macos.py`: native notification với deep-link
- [ ] `notifiers/log.py`: JSONL writer
- [ ] `notifiers/audio.py`: afplay
- [ ] State persistence: lưu/load `state.json`
- [ ] Dedupe logic: `alerts_seen.json`
- [ ] Tier-aware scheduling
- [ ] launchd setup
- [ ] **Acceptance**: Tool tự chạy 24/7, notification pop khi có deal

### Tuần 3-4: Quality of life
- [ ] Telegram notifier
- [ ] Streamlit dashboard cơ bản
- [ ] CLI `sniper add/status/recent`
- [ ] Filter chi tiết (float, sticker)
- [ ] Steam price comparison trong notification

### Tháng 2+: Advanced
- [ ] Z-score anomaly detection
- [ ] Skinport API integration (cho ROI thực)
- [ ] ML model
- [ ] (very late) Auto-buy với strict guardrails

---

## 9. Risks & mitigations

### 9.1 Account ban
- **Risk**: Buff detect bot, ban account, mất balance
- **Mitigation**: 
  - Conservative polling (Hot tier 15s, không 5s)
  - Random jitter ±20% trong interval (đừng poll đúng giây)
  - Dùng cookie từ browser thật, không headless
  - Account dùng cho sniper KHÁC account hold balance lớn

### 9.2 Captcha / rate limit
- **Risk**: Bị block giữa giờ deal hot
- **Mitigation**:
  - Circuit breaker: 3 lỗi liên tiếp → pause 5 phút
  - Notification riêng "tool đang throttled" để bạn biết check manual
  - Backup cookie thứ 2 để swap

### 9.3 False positive
- **Risk**: Alert spam khi giá thị trường giảm chung, không phải mispricing
- **Mitigation**:
  - Threshold absolute (`max_buy_price`) thay vì chỉ relative
  - Z-score confirm: alert chỉ khi z < -2 so với 100 sell orders gần nhất

### 9.4 Lỡ deal
- **Risk**: Item rẻ chỉ tồn tại 30s, 60s polling miss
- **Mitigation**: 
  - Hot tier 10-15s cho top items
  - Telegram để nhận alert khi rời máy
  - Auto-buy (P2, sau khi tool ổn)

### 9.5 macOS sleep
- **Risk**: Máy sleep → tool dừng poll
- **Mitigation**: `caffeinate` khi run, hoặc hostname ra cloud VPS sau

---

## 10. Anti-pattern phải tránh

❌ **Polling cùng tần suất cho mọi item** — sẽ ban hoặc miss deal
✅ Tier-aware

❌ **Lưu state trong memory only** — restart mất hết
✅ Persist sau mỗi cycle

❌ **Notify mọi thay đổi giá** — spam, tê liệt
✅ Filter strict + dedupe

❌ **1 cookie cho mọi request** không jitter — bị flag nhanh
✅ Random delay, multiple cookies, conservative interval

❌ **Database ngay từ đầu** — over-engineer
✅ File JSON/YAML cho 1 user, di chuyển sang DB chỉ khi đau

❌ **Build dashboard trước polling** — vô ích nếu data sai
✅ MVP polling + console log trước, UI sau

❌ **Auto-buy ngay** — mất tiền do bug
✅ Manual click 3 tháng đầu, build trust với tool

❌ **Watchlist 500 items** — không sniper được, chỉ analytics
✅ Top 30-50 items thực sự muốn mua

---

## 11. Success metrics — sau 1 tháng dùng

Đo bằng số liệu thật:

| Metric | Target |
|---|---|
| Số alert/ngày | 5-15 (không quá ít, không spam) |
| Tỷ lệ alert → click mở Buff | >50% (alert relevant) |
| Tỷ lệ click → mua thật | >20% (deal đủ tốt) |
| Latency từ list → notify | <30s (Hot tier) |
| Uptime | >95% |
| False positive rate | <30% |
| Số deal "tiếc" (giá tốt mà miss) | <5/tuần |

→ Nếu sau 1 tháng metric tệ → tune thresholds, đổi tier strategy, **không** rewrite tool.

---

## TL;DR

**Nhu cầu thực**: Sniping tool, không analytics. Top 30-50 item, polling 15s-5min tier-aware, notify trong giây, run 24/7 trên M1 Pro.

**MVP 1 tuần**: watchlist YAML + curl_cffi client + sell_order polling + diff + macOS notify + state persistence. ~500 dòng Python.

**Stack tối giản**: Python + curl_cffi + asyncio + YAML files + Streamlit (P1) + launchd. Không Docker/Redis/Postgres/FastAPI. M1 Pro overkill cho workload này.

**Không làm sớm**: Auto-buy, ML, multi-account, web app phức tạp. Wait until tool ổn 1+ tháng.

**KPI thành công**: 1 deal/tuần kiếm về > thời gian build tool. Nếu < threshold đó → bỏ, không sunk cost.
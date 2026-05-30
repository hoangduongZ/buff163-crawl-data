# Buff163 Sniper Tool — Tech Stack & Best Practices

> **Mục tiêu**: Sniping tool theo dõi 50-200 CS2 skin trên Buff163, phát hiện sell order giá thấp bất thường, notify trong vài giây, có giao diện quản lý watchlist và xem lịch sử alert.

---

## 1. Tổng quan stack

```
┌─────────────────────────────────────────────────────────┐
│  Python 3.12 (arm64, Homebrew)                          │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  CLI        │  │  Core Engine │  │  Dashboard    │  │
│  │  typer      │  │  asyncio     │  │  Streamlit    │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                         │                               │
│                   ┌─────▼──────┐                        │
│                   │ curl_cffi  │  HTTP + TLS bypass      │
│                   └─────┬──────┘                        │
│                         │                               │
│              ┌──────────▼──────────┐                    │
│              │   File persistence  │                    │
│              │  YAML / JSON / JSONL│                    │
│              └─────────────────────┘                    │
└─────────────────────────────────────────────────────────┘
         │                    │
    macOS notify          Telegram bot
    (osascript)         (python-telegram-bot)
```

---

## 2. Stack chi tiết theo layer

### 2.1 Runtime

| Công nghệ | Version | Mục đích |
|---|---|---|
| **Python** | 3.12, arm64 | Runtime chính. ARM native trên M1 Pro, fast startup |
| **uv** hoặc venv | latest | Quản lý virtual environment. `uv` nhanh hơn pip 10-100x |
| **pyproject.toml** | PEP 517 | Quản lý dependency thay `requirements.txt` |

> **Tại sao 3.12**: asyncio cải thiện, `tomllib` built-in, type hints tốt hơn. Tránh 3.13 vì ecosystem chưa kịp.

---

### 2.2 HTTP & Anti-bot

| Công nghệ | Version | Mục đích |
|---|---|---|
| **curl_cffi** | ≥ 0.7 | HTTP client chính. Impersonate Chrome TLS fingerprint — quan trọng nhất để không bị Buff block |
| **asyncio** (stdlib) | built-in | Async I/O, chạy nhiều request đồng thời có controlled concurrency |

> **Tại sao curl_cffi thay requests/httpx**: Buff163 dùng Cloudflare + JA3/JA4 TLS fingerprint detection. `requests` và `httpx` bị detect là bot. `curl_cffi` impersonate TLS handshake của Chrome thật → bypass được.

```python
# Pattern chuẩn
from curl_cffi.requests import AsyncSession

async with AsyncSession(impersonate="chrome120") as session:
    resp = await session.get(url, headers=headers, cookies=cookies)
```

---

### 2.3 Concurrency & Scheduling

| Công nghệ | Mục đích |
|---|---|
| **asyncio** (stdlib) | Event loop chính, không cần thêm framework |
| **asyncio.Semaphore** | Giới hạn max 3 concurrent HTTP requests — tránh trigger anti-bot |
| **asyncio.PriorityQueue** | Tier-aware scheduling: Hot/Warm/Cold poll ở tần suất khác nhau |

> **Không dùng**: Celery, RQ, Redis, threading. Với 1 user + 200 items, asyncio đủ và đơn giản hơn nhiều.

```python
# Rate control
semaphore = asyncio.Semaphore(3)  # max 3 request đồng thời

# Tier polling
# Hot:  poll mỗi 10-15s (top 20 items quan tâm nhất)
# Warm: poll mỗi 60s   (50 items kế tiếp)
# Cold: poll mỗi 5min  (còn lại)
```

---

### 2.4 Config & Validation

| Công nghệ | Version | Mục đích |
|---|---|---|
| **pyyaml** | ≥ 6.0 | Parse watchlist.yaml và settings.yaml |
| **pydantic** | v2 | Validate config khi load — catch lỗi sớm, type-safe |

> **Tại sao YAML thay JSON**: Comment được, edit thoải mái, không cần quote nhiều. Watchlist là file bạn edit thủ công nhiều nhất.

```yaml
# watchlist.yaml
items:
  - goods_id: 33453
    name: "AK-47 | Redline (FT)"
    max_buy_price_cny: 90.0  # giá tối đa chấp nhận
    max_float: 0.20
```

---

### 2.5 CLI

| Công nghệ | Version | Mục đích |
|---|---|---|
| **typer** | ≥ 0.9 | CLI framework. Khai báo bằng type hint, tự gen `--help` đẹp |

> **Tại sao typer thay argparse**: Ít boilerplate hơn 5-10x, auto-complete, colored output built-in.

```bash
sniper start              # chạy daemon
sniper status             # xem trạng thái hiện tại
sniper recent             # 10 alert gần nhất
sniper add 33453 --max 90 # thêm item vào watchlist
sniper test               # test 1 item, không loop
```

---

### 2.6 Logging

| Công nghệ | Version | Mục đích |
|---|---|---|
| **loguru** | ≥ 0.7 | Application log ra console + file |

> **Tại sao loguru thay logging stdlib**: Setup 1 dòng thay vì 10 dòng config. Colored output, rotation, exception tracing đẹp hơn nhiều.

```python
from loguru import logger
logger.add("logs/sniper.log", rotation="10 MB")
logger.info("Alert: AK Redline 85 CNY")
```

---

### 2.7 Persistence (File-based, không DB)

| File | Format | Mục đích |
|---|---|---|
| `watchlist.yaml` | YAML | Danh sách item cần theo dõi — bạn edit thủ công |
| `settings.yaml` | YAML | Config tier interval, thresholds, notification |
| `state.json` | JSON | Last-seen price của từng item, so sánh để detect thay đổi |
| `alerts_seen.json` | JSON | Set sell_order_id đã alert — tránh spam khi restart |
| `alerts_history.jsonl` | JSONL | Log toàn bộ alert history, đọc lại được |
| `cookie.txt` | plain text | Cookie session từ browser (gitignored) |

> **Tại sao không SQLite/Postgres**: Data size nhỏ (<50MB/tháng với prune), 1 user, file JSON/YAML đơn giản hơn, debug bằng `cat` được, M1 NVMe đủ nhanh.

---

### 2.8 Notification

| Công nghệ | Mục đích | Priority |
|---|---|---|
| **osascript** (subprocess) | macOS native notification — không cần thư viện | P0 |
| **afplay** (subprocess) | Audio beep khi có deal đặc biệt (built-in macOS) | P0 |
| **python-telegram-bot** ≥ 20.7 | Push lên phone khi rời máy | P1 |

> **Tại sao Telegram thay email**: Realtime, có inline button "Open in Buff", free, mobile-friendly hơn nhiều.

---

### 2.9 Dashboard (Giao diện)

| Công nghệ | Version | Mục đích |
|---|---|---|
| **Streamlit** | ≥ 1.30 | Web dashboard — watchlist editor, alert history, status |
| **plotly** | ≥ 5.18 | Price history chart (đi kèm Streamlit) |

> **Tại sao Streamlit**: Viết 200 dòng Python thuần có UI hoàn chỉnh. Auto-reload khi đổi code. 1 user không cần auth. Dev nhanh nhất trong các option Python.

> **Giới hạn**: Không realtime tốt bằng WebSocket. Dùng `st.rerun()` + sleep 2s để refresh — chấp nhận được vì notification thật sự đã qua macOS/Telegram, UI chỉ để xem lịch sử và manage watchlist.

```
http://localhost:8501

[ Status: 🟢 Running  •  Last poll: 3s ago ]
[ Active: 47 items  •  Alerts last 24h: 12 ]

┌─── Watchlist ───────────────┐ ┌── Recent Alerts ──┐
│ AK Redline FT   90 CNY  Hot │ │ 🎯 AK Redline 85  │
│ AWP Asiimov    250 CNY  Hot │ │    2 min ago      │
│ [+ Add item]                │ │ 🎯 AWP Asiimov 230│
└─────────────────────────────┘ └───────────────────┘

┌── Price History ────────────────────────────────┐
│ [plotly chart]                                   │
│  100 ┤    ╱╲                                     │
│   90 ┤───╯  ╲___╱╲   ← target line              │
│   85 ┤            ╲___                           │
└─────────────────────────────────────────────────┘
```

---

### 2.10 Testing & Code Quality

| Công nghệ | Mục đích |
|---|---|
| **pytest** | Unit test cho differ, filter, watchlist logic |
| **pytest-asyncio** | Test async functions |
| **ruff** | Linter + formatter — thay thế black + flake8 + isort, cực nhanh |

---

### 2.11 Process Management (macOS)

| Công nghệ | Mục đích |
|---|---|
| **launchd** (macOS native) | Chạy daemon khi boot, tự restart nếu crash |
| **caffeinate** (macOS native) | Prevent máy sleep khi tool đang chạy |

> **Tại sao không Docker/systemd**: Chạy local trên M1, không cần containerize. launchd là native macOS, zero overhead.

```xml
<!-- ~/Library/LaunchAgents/com.you.buffsniper.plist -->
<key>KeepAlive</key><true/>   <!-- tự restart nếu crash -->
<key>RunAtLoad</key><true/>   <!-- chạy khi mở máy -->
```

---

## 3. Những gì KHÔNG dùng và tại sao

| Bỏ qua | Lý do |
|---|---|
| ~~Redis~~ | Overkill cho 1 user, file JSON đủ |
| ~~PostgreSQL / SQLite~~ | Data nhỏ, file JSON đơn giản hơn, không cần query phức tạp |
| ~~Celery / RQ~~ | asyncio đủ, không cần message broker |
| ~~Docker~~ | Chạy local M1, thêm complexity không có lợi gì |
| ~~FastAPI~~ | Chưa cần REST API, Streamlit đủ cho 1 user |
| ~~Selenium / Playwright~~ | Nặng, chậm — chỉ dùng nếu curl_cffi fail (fallback P2) |
| ~~requests / httpx~~ | Bị Buff detect TLS fingerprint, dùng curl_cffi |
| ~~threading~~ | asyncio kiểm soát concurrency tốt hơn, không race condition |
| ~~React / Next.js~~ | Overkill cho dashboard 1 user |

---

## 4. pyproject.toml

```toml
[project]
name = "buff-sniper"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "curl_cffi>=0.7.0",        # HTTP + TLS bypass
    "pyyaml>=6.0",             # config parsing
    "pydantic>=2.5",           # config validation
    "typer>=0.9",              # CLI
    "loguru>=0.7",             # logging
    "python-telegram-bot>=20.7",  # P1: Telegram notify
    "streamlit>=1.30",         # P1: dashboard
    "plotly>=5.18",            # P1: charts
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

---

## 5. Thứ tự build — đừng làm ngược

```
Tuần 1: Core polling
  curl_cffi client → watchlist YAML → polling loop → diff engine → console log
  ✓ Acceptance: phát hiện được deal, log ra terminal

Tuần 2: Notify + Reliability
  macOS notification → JSONL log → state persistence → dedupe → tier scheduling → launchd
  ✓ Acceptance: tool chạy 24/7, pop notification khi có deal

Tuần 3-4: Quality of Life
  Telegram bot → Streamlit dashboard → CLI commands → float/sticker filter

Tháng 2+: Advanced
  Z-score anomaly → Steam price comparison → ML model
  (very late) Auto-buy với strict guardrails
```

> **Quy tắc**: Build dashboard SAU khi polling ổn. UI vô nghĩa nếu data không đúng.

---

## 6. TL;DR — 1 trang

| Layer | Chọn | Không chọn |
|---|---|---|
| Language | Python 3.12 arm64 | Go, Node, Java |
| HTTP | curl_cffi | requests, httpx |
| Async | asyncio (stdlib) | Celery, threading |
| Config | pyyaml + pydantic | JSON, dotenv |
| CLI | typer | argparse, click |
| Log | loguru | logging stdlib |
| Persistence | File JSON/YAML | SQLite, Postgres, Redis |
| Notify (local) | osascript + afplay | pync (thêm dep không cần) |
| Notify (remote) | python-telegram-bot | Email, Slack |
| Dashboard | Streamlit + plotly | React, Next.js, FastAPI |
| Process | launchd + caffeinate | Docker, systemd |
| Test | pytest + ruff | unittest |

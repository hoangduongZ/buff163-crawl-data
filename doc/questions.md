# 5W1H — Bản chất tool Buff163 Sniper

## WHO — Ai?

**1 người** (bạn) ngồi Macbook M1 Pro. Không phải team, không phải startup. Toàn bộ stack thiết kế quanh assumption đó — file JSON thay DB, launchd thay k8s, Streamlit thay Next.js.

---

## WHAT — Là cái gì?

**Buff163 Sniper Tool** — một daemon Python chạy ngầm 24/7, liên tục poll API Buff163 để phát hiện CS2 skin bị bán rẻ bất thường trong watchlist, rồi bắn notification tới màn hình/phone trong vài giây để bạn click mua tay trước người khác.

Nó **không phải** analytics tool (scan toàn market, report), không phải auto-buyer (ít nhất trong 3 tháng đầu).

---

## WHERE — Ở đâu?

- **Data source**: Buff163 API (`/api/market/goods/sell_order`) — không cần scrape HTML, có JSON API thuần.
- **Chạy**: Macbook M1 Pro local, background qua `launchd`. Notification hiện trên màn hình macOS + Telegram phone.
- **Mua**: Bạn click tay trên browser Buff.

---

## WHEN — Khi nào?

- **Trigger**: Mỗi 10–15 giây với hot items, mỗi 5 phút với cold items (tiered polling).
- **Alert khi**: Có sell order mới xuất hiện trong top, giá ≤ threshold bạn set, float/sticker pass filter, chưa từng alert order đó.
- **MVP**: Tuần 1 (~500 dòng Python).

---

## WHY — Tại sao?

**Cơ chế kiếm tiền**: Người bán newbie/vội list skin thấp hơn giá thị trường → bạn mua nhanh → bán lại Skinport/Steam cao hơn → ăn spread 10–30%.

Edge của bạn là **tốc độ** (bot detect trước mắt người), không phải thông tin.

---

## HOW — Như thế nào?

```
YAML watchlist
  → asyncio scheduler (tiered: 15s / 60s / 5min)
  → curl_cffi HTTP (TLS fingerprint Chrome, tránh bị detect)
  → sell_order API
  → diff engine (so sánh top-3 sell order với snapshot lần trước)
  → filter (giá ≤ threshold, float range, dedupe by sell_order_id)
  → osascript notification + deep-link URL mở thẳng item Buff
```

Stack: Python 3.12 + curl_cffi + asyncio + YAML/JSON files. Không Docker/Redis/Postgres.

---

## Đánh giá thực dụng

### Điểm mạnh thật sự

| Quyết định | Tại sao đúng |
|---|---|
| Tiered polling | Poll đều = bị ban hoặc tốn quota vô nghĩa |
| Dedupe theo `sell_order_id` (không phải `goods_id`) | Đúng level granularity — 1 goods có thể có 5 deal cùng lúc |
| File JSON thay DB | Đúng cho 1 user, không phải lười — overhead DB không lợi gì ở scale này |
| `curl_cffi` cho TLS fingerprint | Non-negotiable — `requests` bị detect ngay qua JA3 fingerprint |
| Không auto-buy trong 3 tháng | Bug 1 dòng code = mất tiền thật |

### Rủi ro bị underestimate trong tài liệu

**1. Cookie expiry là pain point lớn nhất — tài liệu nói qua loa.**
Cookie Buff hết hạn ~7–14 ngày. Nếu chết lúc 3 giờ sáng → tool dừng → mất deal. Cần alert sớm trước khi expire, không đợi 403.

**2. Hot tier 15s vẫn có thể quá chậm với high-value items.**
Knife rare $2000+ bị snipe trong 5–10 giây. Best case của tool: 15s poll + xử lý + bạn click = ~20–25s. Mid-range items ($50–200) thực tế hơn nhiều.

**3. Z-score anomaly đang xếp P1 — nên là P0.5.**
Threshold cứng (`max_buy_price_cny`) miss deal khi giá thị trường biến động. Thị trường tăng 30% sau 2 tuần → threshold cũ không còn phản ánh thực tế. Z-score nên làm sớm hơn tài liệu đề xuất.

**4. Buff không có official API → ToS & stability risk.**
Buff đã update anti-bot layer nhiều lần. Tool có thể chết hoàn toàn qua đêm, không có SLA.

**5. "Mua Buff → bán Skinport" có hidden friction.**
Trade hold 7 ngày + Skinport fee 12% + tỷ giá CNY/USD. Với item <$50, margin thực sau tất cả các bước rất mỏng.

---

## Kết luận

| Câu hỏi | Trả lời |
|---|---|
| Có làm được không? | Có — phần kỹ thuật tương đối thẳng |
| MVP 1 tuần có realistic không? | Có, nếu biết Python async + đã có cookie Buff |
| Kiếm được tiền không? | Phụ thuộc niche — mid-range $50–200 thực tế nhất |
| Rủi ro lớn nhất | Cookie chết lúc không hay + Buff update anti-bot |
| Thiếu gì quan trọng | Alert cookie sắp expire + z-score nên ưu tiên sớm hơn |

So sánh giá với chỗ nào?

**Mục đích**: Dễ tính score tự động

Gợi ý: So sánh `sell_min_price` (Buff CNY) với:
1. `goods_info.steam_price_cny` — có sẵn trong response `/api/market/goods`, tính được Buff/Steam ratio ngay.
2. **Skinport API** (có official API, free tier) — giá EUR/USD, đây là target bán thực tế nhất.
3. **Pricempire API** (paid, có free tier) — aggregator nhiều sàn, tiết kiệm công tích hợp từng cái.

Công thức score đơn giản:

```
buff_steam_ratio = sell_min_price_cny / steam_price_cny   # < 0.75 là interesting
skinport_roi     = (skinport_price_usd * 0.88) / (buff_price_cny / 7.2) - 1  # 0.88 = trừ 12% fee
```

Score tổng hợp = weighted average hai chỉ số trên, lọc theo `sell_num` (thanh khoản).

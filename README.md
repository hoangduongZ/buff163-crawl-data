# Buff163 CS2 Sniper

Nghiên cứu và kiểm thử Buff163 API phục vụ xây dựng tool phát hiện skin CS2 bị rao bán rẻ bất thường.

> **Trạng thái:** Nghiên cứu API — chưa build tool  
> **Platform:** macOS M1 Pro

---

## Kết quả kiểm thử API (2026-06-21)

| Endpoint | Không cookie | Có cookie |
|---|---|---|
| `/api/market/goods` | Login Required | ✅ OK — 33.876 items |
| `/api/market/goods/info` | ✅ OK | ✅ OK |
| `/api/market/goods/sell_order` | Login Required | Steam Binding Required |
| `/api/market/goods/buy_order` | ✅ OK | ✅ OK |
| `/api/market/goods/price_history` | — | Steam Binding Required |
| `/api/market/goods/bill_order` | — | Steam Binding Required |
| `/api/market/category` | Path Not Found | Path Not Found |
| `/api/market/steam_price_history` | Path Not Found | Path Not Found |

**Blocker hiện tại:** `/sell_order` cần tài khoản Buff đã liên kết Steam.

---

## Phát hiện quan trọng

- `/goods` và `/sell_order` thực tế cần auth — doc cũ ghi nhầm là public
- `/category`, `/itemset`, `/steam_price_history` đã bị xóa khỏi Buff163
- Path đúng cho lịch sử giá: `/api/market/goods/price_history` (không có suffix `/buff`)
- CS2 goods_id bắt đầu từ ~40.000 (dưới đó là Dota2)
- Gọi `/price_history` thường xuyên → cộng đồng ghi nhận bị khóa tài khoản

---

## Tech đã xác nhận

- `curl_cffi` với `impersonate="chrome124"` — bypass Buff TLS fingerprint detection
- Cookie tối thiểu cần: `session` + `csrf_token` + `Device-Id`

---

## Thư mục

```
doc/
  tool-spec/        kiến trúc và endpoint spec
  analysis/         research notes từ cộng đồng (GitHub, Reddit, Zhihu)
  business-logic/   chiến lược trading

endpoint-evidences/
  ep0X_*.py         script kiểm thử từng endpoint
  evidence/         raw JSON response từ Buff (gitignored)
```

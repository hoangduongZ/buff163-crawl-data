# BUFF163 API Research Notes cho CS2 Skin Data

> Ngày tổng hợp: 2026-06-20  
> Mục tiêu: ghi chú nghiên cứu các endpoint BUFF163 phục vụ app theo dõi giá CS2 skin, catalog item, buy order, sell order và lịch sử giá.  
> Phạm vi an toàn: chỉ phục vụ phân tích dữ liệu thị trường bằng tài khoản/dữ liệu hợp lệ của chính bạn. Không dùng để bypass anti-bot, chiếm session, dùng cookie người khác, tự động mua/bán hoặc né cơ chế bảo vệ của BUFF163.

---

## 1. Kết luận nhanh

BUFF163 không có public API miễn phí, ổn định và đầy đủ cho cộng đồng quốc tế.

Phần lớn endpoint đang được cộng đồng sử dụng là endpoint nội bộ của web/app, thường yêu cầu cookie đăng nhập. Một số endpoint đọc dữ liệu cơ bản có thể hoạt động ẩn danh, nhưng các endpoint quan trọng như danh sách market item và sell order thường trả về `"Login Required"` nếu không có cookie.

Kết luận thực dụng:

- Có thể dùng `/api/market/goods/info` để lấy thông tin chi tiết một item theo `goods_id`.
- Có thể dùng `/api/market/goods/buy_order` để lấy buy order của một item.
- Muốn lấy catalog từ `/api/market/goods` thường cần cookie đăng nhập.
- Muốn lấy sell order từ `/api/market/goods/sell_order` thường cần cookie đăng nhập.
- Endpoint `/api/market/category`, `/api/market/itemset`, `/api/market/steam_price_history` hiện có khả năng đã chết hoặc không đúng path.
- Endpoint lịch sử giá đúng được cộng đồng ghi nhận là `/api/market/goods/price_history`, nhưng rủi ro bị khóa tài khoản cao nếu gọi thường xuyên.
- Nếu mục tiêu là app cá nhân ổn định, nên ưu tiên crawl nhẹ, cache mạnh, hoặc dùng dataset/API trung gian.

---

## 2. Kết quả kiểm thử endpoint ẩn danh

| Endpoint | HTTP | Buff code | Kết luận |
|---|---:|---|---|
| `/api/market/goods` | 200 | Login Required | Cần auth |
| `/api/market/goods/info` | 200 | OK | Có thể dùng ẩn danh |
| `/api/market/goods/sell_order` | 200 | Login Required | Cần auth |
| `/api/market/goods/buy_order` | 200 | OK | Có thể dùng ẩn danh |
| `/api/market/category` | 200 | Path Not Found | Có thể đã chết |
| `/api/market/itemset` | 200 | Path Not Found | Có thể đã chết |
| `/api/market/steam_price_history` | 200 | Path Not Found | Sai path / đã chết |

---

## 3. Cookie và xác thực

### 3.1. Cookie quan trọng

Các repo cộng đồng thường yêu cầu lấy cookie sau khi đăng nhập BUFF163 bằng trình duyệt.

Những cookie thường xuất hiện:

```text
Device-Id
session
csrf_token
remember_me
NTES_YD_SESS
S_INFO
P_INFO
Locale-Supported
game
```

Trong đó, các hướng dẫn cộng đồng thường nhấn mạnh 3 giá trị quan trọng:

```text
Device-Id
session
csrf_token
```

Một số bài cũ cho rằng chỉ cần `session` là đủ cho endpoint `/goods`, nhưng các tool mới hơn thường yêu cầu thêm `Device-Id` và `csrf_token`.

### 3.2. Cách lấy cookie hợp lệ

Quy trình hợp lệ thường là:

1. Đăng nhập tài khoản của chính bạn tại `https://buff.163.com`.
2. Mở DevTools bằng F12.
3. Vào tab Network.
4. Refresh trang.
5. Tìm request API hoặc response có `Set-Cookie`.
6. Copy các giá trị cookie cần thiết.
7. Lưu vào file cấu hình cục bộ, ví dụ `.env` hoặc `config.json`.

Không nên chia sẻ cookie, session, Steam token hoặc API key cho người khác.

### 3.3. Session dài hạn

Không tìm thấy cách public, ổn định, an toàn để tạo session cookie dài hạn mà không cần đăng nhập lại.

BUFF163 có thể:

- hết hạn session;
- invalid session;
- yêu cầu đăng nhập lại;
- khóa session nếu phát hiện hành vi tự động hóa;
- giới hạn theo thiết bị, IP hoặc hành vi.

---

## 4. Endpoint chính

## 4.1. Goods catalog

```http
GET https://buff.163.com/api/market/goods
```

### Mục đích

Lấy danh sách item trên market. Đây là endpoint quan trọng nhất để xây catalog nội bộ.

### Params thường gặp

```text
game=csgo
page_num=1
page_size=80
category=weapon_ak47
sort_by=price.asc
sort_by=price.desc
sort_by=sell_num.desc
min_price=100
max_price=200
```

### Ví dụ

```text
https://buff.163.com/api/market/goods?game=csgo&page_num=1&page_size=80&category=weapon_ak47&sort_by=price.desc&min_price=100&max_price=200
```

### Output thường có

```text
items[]
total_count
total_page
page_num
```

Mỗi item thường có:

```text
id
name
market_hash_name
sell_reference_price
steam_price_cny
buy_num
sell_num
steam_market_url
goods_info
```

### Ghi chú

- Nếu không có cookie, endpoint này có thể trả `"Login Required"`.
- Nếu không truyền `category`, kết quả có thể gồm cả sticker, case, graffiti và nhiều item không phải weapon skin.
- `page_size` thường được cộng đồng dùng tối đa khoảng 80.

---

## 4.2. Goods info

```http
GET https://buff.163.com/api/market/goods/info
```

### Mục đích

Lấy thông tin chi tiết của một item theo `goods_id`.

### Params

```text
game=csgo
goods_id=44000
```

### Ví dụ

```text
https://buff.163.com/api/market/goods/info?game=csgo&goods_id=44000
```

### Trạng thái

Theo kiểm thử của bạn, endpoint này trả `"OK"` kể cả khi không có cookie.

### Dùng để làm gì

- Lấy tên item.
- Lấy ảnh.
- Lấy metadata.
- Kiểm tra một `goods_id` có tồn tại hay không.
- Bổ sung thông tin khi đã có danh sách id từ dataset khác.

---

## 4.3. Sell order

```http
GET https://buff.163.com/api/market/goods/sell_order
```

### Mục đích

Lấy danh sách lệnh bán hiện tại của một item.

### Params thường gặp

```text
game=csgo
goods_id=44000
page_num=1
page_size=10
sort_by=price.asc
sort_by=paintwear.asc
min_paintwear=0.00
max_paintwear=0.07
paintseed=554
```

### Ví dụ sort theo float

```text
https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=44060&sort_by=paintwear.asc
```

### Ví dụ lọc pattern seed

```text
https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id=44060&sort_by=paintwear.asc&paintseed=554
```

### Trạng thái

Theo kiểm thử của bạn, endpoint này trả `"Login Required"` khi không có cookie.

### Ghi chú

Đây là endpoint rất quan trọng cho sniping vì nó cho biết ask price thấp nhất, float, paint seed và các listing đang bán.

---

## 4.4. Buy order

```http
GET https://buff.163.com/api/market/goods/buy_order
```

### Mục đích

Lấy danh sách lệnh mua hiện tại của một item.

### Params

```text
game=csgo
goods_id=44000
page_num=1
page_size=10
```

### Ví dụ

```text
https://buff.163.com/api/market/goods/buy_order?game=csgo&goods_id=44000&page_num=1&page_size=10
```

### Trạng thái

Theo kiểm thử của bạn, endpoint này trả `"OK"` kể cả khi không có cookie.

### Dùng để làm gì

- Lấy bid cao nhất.
- Tính spread giữa ask và bid.
- Đánh giá thanh khoản phía cầu.
- Phục vụ alert khi ask thấp bất thường so với bid.

---

## 4.5. Goods price history

```http
GET https://buff.163.com/api/market/goods/price_history
```

### Mục đích

Lấy lịch sử giá của item.

### Params

```text
game=csgo
goods_id=34790
currency=CNY
days=7
```

### Ví dụ

```text
https://buff.163.com/api/market/goods/price_history?game=csgo&goods_id=34790&currency=CNY&days=7
```

### Output được cộng đồng mô tả

Có mảng `price_history`. Mỗi phần tử thường chứa:

```text
timestamp
price
volume / count
```

### Cảnh báo quan trọng

Endpoint này bị cộng đồng đánh giá là rủi ro cao. Có ghi nhận tài khoản bị khóa khi gọi quá thường xuyên, kể cả khi delay nhiều giây.

Không nên dùng endpoint này cho crawler liên tục. Nếu cần lịch sử giá, cân nhắc:

- dùng Steam Market history trực tiếp;
- dùng dataset cộng đồng;
- dùng third-party API;
- tự lưu snapshot hằng ngày từ dữ liệu hiện tại thay vì gọi history liên tục.

---

## 5. Endpoint sai hoặc đã chết

Các endpoint sau hiện trả về `"Path Not Found"` trong kiểm thử của bạn:

```text
/api/market/category
/api/market/itemset
/api/market/steam_price_history
```

Nhận định:

- BUFF163 không cần endpoint category riêng cho luồng market phổ biến.
- Danh mục được truyền qua param `category` trong `/api/market/goods`.
- `steam_price_history` không phải path hiện tại được cộng đồng ghi nhận.
- Path lịch sử giá được ghi nhận là `/api/market/goods/price_history`.

---

## 6. Category và tags

Không tìm thấy endpoint category công khai hiện tại.

Cách thực tế để lọc danh mục là dùng param `category` trong endpoint `/api/market/goods`.

Ví dụ category:

```text
weapon_ak47
weapon_awp
weapon_m4a1
weapon_m4a1_silencer
weapon_deagle
weapon_glock
weapon_usp_silencer
knife
sticker
container
```

Tên category có thể thay đổi theo frontend BUFF163. Cách chắc chắn nhất là:

1. Mở trang market bằng trình duyệt đã đăng nhập.
2. Chọn filter/category trên UI.
3. Quan sát request `/api/market/goods` trong tab Network.
4. Lấy giá trị query param thực tế.

---

## 7. Xây catalog goods_id

### 7.1. Có thể brute-force goods_id không?

Không nên.

Lý do:

- `goods_id` không liên tục.
- Có nhiều khoảng trống.
- ID có thể xen giữa item cũ và mới.
- Brute-force gây request rất lớn.
- Dễ bị chặn hoặc khóa session.

### 7.2. Cách nên làm

Có 3 hướng an toàn hơn:

#### Hướng A: Duyệt `/goods` theo category

```text
for category in categories:
    for page_num in range(1, total_page + 1):
        call /api/market/goods
        save items[].id
```

#### Hướng B: Dùng dataset cộng đồng

Có repo cộng đồng như `ModestSerhat/cs2-marketplace-ids`, lưu nhiều ID liên quan đến CS2 item trên BUFF163 và Youpin898.

#### Hướng C: Hybrid

- Dùng dataset cộng đồng làm seed.
- Với mỗi id, gọi `/goods/info` để verify.
- Sau đó chỉ crawl sell/buy order cho danh sách item quan tâm.

### 7.3. Không có range goods_id đáng tin cậy

`goods_id=44000` là một item dao CS:GO/CS2, nhưng không thể suy ra khoảng ID hợp lệ chỉ từ giá trị này.

---

## 8. Rate limit và chống bot

BUFF163 không công bố rate limit chính thức cho các endpoint nội bộ.

Các ghi nhận cộng đồng:

- Support từng trả lời theo hướng “hãy hành xử như người thật”.
- Có người bị khóa tài khoản sau khoảng 10 phút khi chạy scraper random mỗi 5–10 giây/request.
- Endpoint `goods/price_history` bị đánh giá rủi ro hơn endpoint `/goods`.
- Dịch vụ cs2.sh mô tả BUFF163 chủ động chặn automated collection, invalid session và block IP.

### 8.1. Không nên làm

```text
Không spam request.
Không gọi history liên tục.
Không crawl full market trong một batch lớn.
Không dùng cookie người khác.
Không lưu raw Steam session token nếu không thật sự cần.
Không tự động buy/sell/cancel khi chưa kiểm soát rủi ro.
Không cố bypass anti-bot hoặc né cơ chế bảo vệ.
```

### 8.2. Cách crawl nhẹ hơn

```text
Catalog /goods: 1 lần/ngày
Goods info: chỉ gọi khi cần verify item mới
Buy order: 5–30 phút/lần cho item quan tâm
Sell order: 5–30 phút/lần cho item quan tâm
Price history: hạn chế tối đa; ưu tiên tự lưu snapshot
```

---

## 9. API chính thức và third-party API

### 9.1. API chính thức BUFF163

Có ghi nhận cuối năm 2025 rằng BUFF163 phát hành BUFF API 1.0.0 dạng trả phí:

```text
Developer: ¥300/tháng
Enterprise: ¥1000/tháng
OpenAPI 3.0
```

Tuy nhiên khả năng tiếp cận có thể bị giới hạn theo tài khoản Trung Quốc hoặc điều kiện nội bộ.

### 9.2. Third-party API

Một số dịch vụ cung cấp dữ liệu BUFF163 đã crawl sẵn:

```text
cs2.sh
steamwebapi
csgoskins.gg
pricempire
skinpock
```

Dùng third-party API sẽ an toàn và ổn định hơn nếu bạn chỉ cần dữ liệu giá, spread, history, volume.

---

## 10. Thiết kế app đề xuất

## 10.1. Mục tiêu app

App nên được thiết kế như một hệ thống market snapshot, không phải full scraper.

Mục tiêu chính:

```text
Theo dõi ask price
Theo dõi bid price
Tính spread
Tính biến động giá
Phát hiện item lệch giá
Lưu lịch sử snapshot nội bộ
```

## 10.2. Kiến trúc FastAPI gợi ý

```text
app/
  api/
    goods.py
    prices.py
    analytics.py

  crawlers/
    buff_client.py
    goods_crawler.py
    buy_order_crawler.py
    sell_order_crawler.py
    info_crawler.py

  jobs/
    scheduler.py
    tasks.py

  models/
    goods.py
    sell_order_snapshot.py
    buy_order_snapshot.py
    crawl_run.py

  services/
    price_analyzer.py
    alert_service.py
```

## 10.3. Database schema gợi ý

### goods

```sql
id
buff_goods_id
market_hash_name
name
category
icon_url
steam_price_cny
created_at
updated_at
```

### sell_order_snapshots

```sql
id
buff_goods_id
price_cny
paintwear
paintseed
asset_id_hash
seller_hash
crawled_at
```

### buy_order_snapshots

```sql
id
buff_goods_id
price_cny
quantity
crawled_at
```

### price_signals

```sql
id
buff_goods_id
ask_price
bid_price
spread
spread_percent
liquidity_score
signal_type
created_at
```

### crawl_runs

```sql
id
source
endpoint
status
item_count
error_message
started_at
finished_at
```

---

## 11. Công thức phân tích giá

### Spread

```text
spread = ask_price - bid_price
spread_percent = spread / ask_price * 100
```

### Mid price

```text
mid_price = (ask_price + bid_price) / 2
```

### Liquidity score

```text
liquidity_score = sell_order_count + buy_order_count + recent_sales_count
```

### Sniping signal đơn giản

```text
if ask_price < average_7d_price * 0.9
and spread_percent < threshold
and liquidity_score > minimum:
    signal = "possible_snipe"
```

---

## 12. Chiến lược MVP

### Phase 1: Không cần cookie

Dùng endpoint public:

```text
/goods/info
/buy_order
```

Mục tiêu:

- verify goods_id;
- lấy bid;
- build watchlist từ dataset cộng đồng;
- chưa crawl sell order.

### Phase 2: Có cookie chính chủ

Dùng thêm:

```text
/goods
/sell_order
```

Mục tiêu:

- tạo catalog;
- lấy ask;
- tính spread;
- lưu snapshot.

### Phase 3: Analytics

Tự lưu lịch sử giá thay vì gọi `price_history` liên tục.

```text
Mỗi lần crawl sell/buy order
→ lưu snapshot
→ tự tính trend 1h / 24h / 7d
```

### Phase 4: Alert

Gửi alert khi:

```text
ask giảm mạnh
spread thấp
bid tăng
item có volume cao
giá thấp hơn median snapshot
```

---

## 13. Nguồn tham khảo

### GitHub

- `markzhdan/buff163-unofficial-api`  
  https://github.com/markzhdan/buff163-unofficial-api

- `perrebser/buff163Prices`  
  https://github.com/perrebser/buff163Prices

- `pato-1441/tocsvBuff163`  
  https://github.com/pato-1441/tocsvBuff163

- `sometastycake/bufflogin`  
  https://github.com/sometastycake/bufflogin

- `ModestSerhat/cs2-marketplace-ids`  
  https://github.com/ModestSerhat/cs2-marketplace-ids

- `atalantus/buff-price-history-archive`  
  https://github.com/atalantus/buff-price-history-archive

### Reddit

- Buff163 có API không?  
  https://www.reddit.com/r/csgomarketforum/comments/1bx36zv/does_buff163_have_a_api_q/

- Buff API conditions / rate limit  
  https://www.reddit.com/r/Csgotrading/comments/118ywe7/buff163com_api_conditions_q/

- Steam Session Token Usage / buff163 update rules  
  https://www.reddit.com/r/csgomarketforum/comments/1bxmwtg/q_steam_session_token_usage_buff163_update_rules/

- Automatically updating Buff163 investment Spreadsheet  
  https://old.reddit.com/r/csgomarketforum/comments/ny7r6i/d_automatically_updating_buff163_investment/

### Blog / community

- Zhihu crawler note về BUFF163  
  https://zhuanlan.zhihu.com/p/182880739

- cs2.sh BUFF API  
  https://cs2.sh/buff-api

- SteamWebAPI BUFF API article  
  https://www.steamwebapi.com/blog/cs2-buff-api-real-time-buff163-prices-history-for-cs2-items

### X / Twitter

- Ghi nhận BUFF API 1.0.0 trả phí  
  https://x.com/olafkswg/status/1993357766912586157

---

## 14. Checklist khi triển khai

```text
[ ] Không dùng cookie của người khác
[ ] Không lưu cookie dạng plain text trong repo
[ ] Không commit .env
[ ] Có rate limit nội bộ
[ ] Có retry với backoff
[ ] Có cache
[ ] Có log crawl_run
[ ] Có cơ chế stop khi nhận Login Required nhiều lần
[ ] Có cơ chế stop khi nhận Path Not Found
[ ] Không gọi price_history liên tục
[ ] Không tự động mua/bán trong MVP
[ ] Tự lưu snapshot để build history riêng
```

---

## 15. Tóm tắt cuối

BUFF163 có thể dùng làm nguồn dữ liệu giá CS2 nhưng không nên crawl như một public API bình thường.

Cách làm bền hơn:

1. Dùng dataset cộng đồng để có danh sách `goods_id`.
2. Dùng `/goods/info` và `/buy_order` không cookie để verify.
3. Dùng cookie chính chủ nếu cần `/goods` và `/sell_order`.
4. Tự lưu snapshot để xây price history riêng.
5. Tránh endpoint `goods/price_history` nếu không thật sự cần.
6. Không bypass anti-bot.
7. Cân nhắc third-party API nếu cần dữ liệu production ổn định.

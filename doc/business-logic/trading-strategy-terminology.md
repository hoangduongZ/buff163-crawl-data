## Giải thích thuật ngữ

### Thuật ngữ thị trường

| Thuật ngữ | Giải thích |
|---|---|
| **Buff163** | Sàn giao dịch skin CS2/CSGO lớn nhất Trung Quốc. Giá thường rẻ hơn Steam 20–40%. |
| **Steam Market** | Chợ skin chính thức của Valve (hãng làm CS2). Giá thường cao hơn Buff. |
| **CSFloat / Skinport** | Các sàn giao dịch skin quốc tế khác, thường dùng để bán sang người mua Tây. |
| **Flip** | Mua rẻ ở một chỗ, bán đắt hơn ở chỗ khác để kiếm lời. |
| **Arbitrage** | Lợi dụng chênh lệch giá giữa hai sàn/thị trường để kiếm lời không rủi ro. |
| **Listing** | Một vật phẩm cụ thể đang được đăng bán trên sàn. |
| **Spread** | Khoảng cách giữa giá bán thấp nhất và giá mua cao nhất. Spread càng hẹp → thị trường càng thanh khoản tốt. |
| **Thanh khoản** | Khả năng mua/bán nhanh mà không ảnh hưởng nhiều đến giá. Item thanh khoản cao = dễ thoát hàng. |
| **Thoát hàng** | Bán được item ra, thu tiền về. |
| **Volume** | Số lượng giao dịch thực sự diễn ra trong một khoảng thời gian. |
| **Phí giao dịch** | Buff thu 2.5% trên mỗi giao dịch bán thành công. Người mua không mất phí. |

### Thuật ngữ giá

| Thuật ngữ | Giải thích |
|---|---|
| **sell_min_price** | Giá bán thấp nhất hiện có trên Buff — tức là giá bạn phải trả nếu muốn mua ngay. |
| **buy_max_price** | Giá cao nhất mà ai đó đang đặt lệnh mua (bid). Bán ngay vào đây sẽ thoát hàng nhanh nhất. |
| **steam_price_cny** | Giá item tương đương trên Steam Market, quy đổi sang CNY (nhân dân tệ). |
| **quick_price** | Giá "bán nhanh" — thấp hơn sell_min_price một chút, dùng khi muốn bán ngay lập tức. |
| **Ratio (Buff/Steam ratio)** | Tỉ lệ `giá Buff / giá Steam`. Ví dụ ratio = 0.65 nghĩa là Buff rẻ hơn Steam 35%. Ratio càng thấp → cơ hội kiếm lời càng cao. |
| **CNY** | Nhân dân tệ (¥) — đơn vị tiền tệ trên Buff163. ~3,400 VNĐ/CNY (tham khảo). |
| **Margin** | Phần lợi nhuận còn lại sau khi trừ phí và giá mua. |
| **Downtrend** | Xu hướng giá đang giảm dần theo thời gian. |

### Thuật ngữ về skin CS2

| Thuật ngữ | Giải thích |
|---|---|
| **Skin** | Vật phẩm trang trí vũ khí trong CS2, không ảnh hưởng gameplay, chỉ thay đổi ngoại hình. |
| **Float (paintwear)** | Chỉ số mài mòn của skin, từ 0.00 (mới nhất) đến 1.00 (cũ nhất). Float càng thấp → skin càng đẹp → giá càng cao. |
| **Exterior (tình trạng)** | Phân loại skin theo float: Factory New (FN) → Minimal Wear (MW) → Field-Tested (FT) → Well Worn (WW) → Battle-Scarred (BS). |
| **Sticker** | Nhãn dán trên skin. Một số sticker từ giải đấu cũ (ví dụ Katowice 2014) có giá trị rất cao, có thể làm tăng giá skin nhiều lần. |
| **StatTrak™ (ST)** | Biến thể đặc biệt của skin, có bộ đếm số kill. Giá cao hơn skin thường cùng loại. |
| **Souvenir** | Biến thể kỷ niệm từ giải đấu CS2 lớn. Thường có sticker của các team thi đấu, giá cao hoặc rất thấp tùy item. |
| **Knife / Glove** | Loại vật phẩm cao cấp nhất, giá thường từ vài triệu đến hàng chục triệu VNĐ. |
| **Covert / Classified / Restricted / Mil-Spec** | Cấp độ hiếm của skin, từ cao xuống thấp. Covert (đỏ) hiếm nhất. |
| **goods_id** | ID định danh một loại skin trên Buff. Mọi listing cùng goods_id là cùng loại skin nhưng khác float/sticker. |
| **market_hash_name** | Tên chuẩn của item dùng để tra cứu trên Steam Market. |

### Thuật ngữ kỹ thuật

| Thuật ngữ | Giải thích |
|---|---|
| **API** | Giao diện lập trình — cách máy tính lấy dữ liệu từ server của Buff một cách tự động thay vì dùng trình duyệt. |
| **Crawl** | Tự động gọi API để thu thập dữ liệu hàng loạt. |
| **Snapshot** | Ảnh chụp dữ liệu tại một thời điểm cụ thể. |
| **Candidate** | Item được lọc ra là có tiềm năng mua tốt, chờ xác nhận thêm. |
| **Sniping** | Tìm và mua nhanh item bị định giá sai (thấp hơn giá trị thực) trước người khác. |
| **Float sniping** | Mua skin có float đặc biệt tốt nhưng đang bị bán sai giá. |
| **Sticker sniping** | Mua skin có sticker quý nhưng người bán không biết/không tính vào giá. |
| **Trade hold / Cooldown** | Thời gian khóa không giao dịch được sau khi mua — thường 7 ngày nếu dùng Steam Guard mobile. |
| **Bid** | Lệnh mua — giá cao nhất người mua sẵn sàng trả (= buy_max_price). |
| **Ask** | Lệnh bán — giá thấp nhất người bán chấp nhận (= sell_min_price). |
| **Scoring model** | Công thức tính điểm để so sánh và xếp hạng các item theo mức độ hấp dẫn. |
| **Auth / Session** | Thông tin đăng nhập — cần thiết để gọi một số API yêu cầu xác thực. |

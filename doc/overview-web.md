# buff.163.com – Tổng hợp dữ liệu (chuẩn theo trang hiện tại)

> Ghi chú: Nội dung dưới đây **chỉ** dùng thông tin xuất hiện trực tiếp trong HTML/DOM trang chủ buff.163.com tại thời điểm quét, không suy diễn thêm.

---

## 1. Điều hướng & khu vực chính

### 1.1. Menu điều hướng trên

- Home → `https://buff.163.com/?game=csgo`  
- Market → `https://buff.163.com/market/csgo`  
- News → `https://buff.163.com/news/`  
- Custom Inspection 3D → `https://buff.163.com/market/custom_inspect?game=csgo`  
- Login/Register → `#` (link placeholder, mở UI đăng nhập/đăng ký)

Trang mặc định đang là game **CS2**, nhưng tham số URL và nhiều link vẫn dùng `game=csgo` (di sản đặt tên).

---

## 2. Khối nội dung “CS2”

Ngay dưới phần điều hướng là khối giới thiệu:

- Tiêu đề: **CS2**  
- Subsection: “Users' choice – The most popular skins”  
- Subsection: “BUFF App – Much more powerful and handy”

Có nút:

- **View market** → `https://buff.163.com/market/csgo#tab=top-bookmarked`

---

## 3. Khối “Popular” (Phổ biến)

Tiêu đề: **Popular**

Có 2 tab:

- CS2  
- DOTA2  

Dưới tab CS2, trang hiện tại hiển thị **10 dòng skin**, mỗi dòng có cấu trúc:

- Một text “Float: …” (khi có float).  
- Tên skin (link tới trang hàng hóa).  
- Giá in CNY, dạng: `¥ <số>` (có in đậm).  
- Tình trạng (Factory New / Field-Tested / Well-Worn / Minimal Wear).  
- Một số dòng có:
  - Ký hiệu `★` (sao).  
  - Một số tag (P2, T3).  
  - Một số với số phía sau (dạng 183, 289, 216, 499, 894, 134, 606, 497) – xuất hiện sau dòng tình trạng, có thể là số bookmark hoặc chỉ số khác (trang không giải thích, nên chỉ ghi lại nguyên văn).

### 3.1. Danh sách chi tiết (dữ liệu đúng như HTML)

1. Float: `0.03798766806721687`  
   - Tên: `AK-47 | Bloodsport (Factory New)`  
   - Link: `https://buff.163.com/goods/33868`  
   - Giá: `¥ 3100`  
   - Tình trạng: `Factory New`  
   - Số: `183`

2. Float: `0.2971876859664917`  
   - Tên: `★ Specialist Gloves | Cloud Chaser (Field-Tested)`  
   - Link: `https://buff.163.com/goods/1134284`  
   - Giá: `¥ 4800`  
   - Tình trạng: `Field-Tested`  
   - Ký hiệu: `★`  
   - Số: `289`

3. Float: `0.03422997519373894`  
   - Tên: `★ M9 Bayonet | Gamma Doppler (Factory New)`  
   - Link: `https://buff.163.com/goods/43104`  
   - Giá: `¥ 13000`  
   - Tình trạng: `Factory New`  
   - Ký hiệu: `★`  
   - Tag: `P2`

4. Float: `0.4206851124763489`  
   - Tên: `AK-47 | Case Hardened (Well-Worn)`  
   - Link: `https://buff.163.com/goods/33884`  
   - Giá: `¥ 3188`  
   - Tình trạng: `Well-Worn`  
   - Tag: `T3`

5. Float: `0.16837194561958313`  
   - Tên: `★ Sport Gloves | Ultra Violent (Field-Tested)`  
   - Link: `https://buff.163.com/goods/1134285`  
   - Giá: `¥ 13499`  
   - Tình trạng: `Field-Tested`  
   - Ký hiệu: `★`  
   - Số: `216`

6. Float: `0.15268518030643463`  
   - Tên: `★ Sport Gloves | Vice (Field-Tested)`  
   - Link: `https://buff.163.com/goods/45582`  
   - Giá: `¥ 8000`  
   - Tình trạng: `Field-Tested`  
   - Ký hiệu: `★`  
   - Số: `499`

7. Float: `0.030218925327062607`  
   - Tên: `★ Karambit | Marble Fade (Factory New)`  
   - Link: `https://buff.163.com/goods/43017`  
   - Giá: `¥ 8000`  
   - Tình trạng: `Factory New`  
   - Ký hiệu: `★`  
   - Số: `894`

8. Float: `0.129705548286438`  
   - Tên: `AK-47 | Crane Flight (Minimal Wear)`  
   - Link: `https://buff.163.com/goods/1134183`  
   - Giá: `¥ 400`  
   - Tình trạng: `Minimal Wear`  
   - Số: `134`

9. Float: `0.26744163036346436`  
   - Tên: `AK-47 | Aphrodite (Field-Tested)`  
   - Link: `https://buff.163.com/goods/1133038`  
   - Giá: `¥ 138`  
   - Tình trạng: `Field-Tested`  
   - Số: `606`

10. Float: `0.18875037133693695`  
    - Tên: `AK-47 | Blue Laminate (Field-Tested)`  
    - Link: `https://buff.163.com/goods/33873`  
    - Giá: `¥ 2050`  
    - Tình trạng: `Field-Tested`  
    - Số: `497`

Cuối khối có link:

- `View market` → `https://buff.163.com/market/csgo#tab=selling`

---

## 4. Khối “Latest” (Mới nhất)

Tiêu đề: **Latest**

Có 2 tab:

- CS2  
- DOTA2  

Dưới tab CS2, đang hiển thị 10 mục, mỗi mục:

- Một link tên item.  
- Lặp lại tên dưới dạng heading `###`.  
- Giá CNY, format có xuống dòng giữa phần nguyên và phần thập phân (vd: `¥ 24` xuống dòng `.64`).

### 4.1. Danh sách chi tiết

1.  
   - Tên: `Sticker | VINI (Gold) | Shanghai 2024`  
   - Link: `https://buff.163.com/goods/1114778` (cả ở dòng trên và heading)  
   - Giá: `¥ 24.64` (hiển thị dạng:
     - `¥ 24`
     - `.64` ở dòng kế tiếp)

2.  
   - Tên: `R8 Revolver | Nitro (Minimal Wear)`  
   - Link: `https://buff.163.com/goods/762056` (cả 2 vị trí)  
   - Giá: `¥ 1.61` (hiển thị `¥ 1` và `.61` xuống dòng)

3.  
   - Tên: `★ Sport Gloves | Omega (Field-Tested)`  
   - Link: `https://buff.163.com/goods/45509`  
   - Giá: `¥ 1650`

4.  
   - Tên: `SG 553 | Basket Halftone (Factory New)`  
   - Link: `https://buff.163.com/goods/1116001`  
   - Giá: `¥ 1.37` (hiển thị `¥ 1` và `.37`)

5.  
   - Tên: `Five-SeveN | Fairy Tale (Field-Tested)`  
   - Link: `https://buff.163.com/goods/835605`  
   - Giá: `¥ 185`

6.  
   - Tên: `StatTrak™ Tec-9 | Flash Out (Factory New)`  
   - Link: `https://buff.163.com/goods/773760`  
   - Giá: `¥ 11.83` (hiển thị `¥ 11` và `.83`)

7.  
   - Tên: `StatTrak™ MP9 | Airlock (Minimal Wear)`  
   - Link: `https://buff.163.com/goods/39047`  
   - Giá: `¥ 107.25` (hiển thị `¥ 107` và `.25`)

8.  
   - Tên: `StatTrak™ AK-47 | Cartel (Field-Tested)`  
   - Link: `https://buff.163.com/goods/38167`  
   - Giá: `¥ 314`

9.  
   - Tên: `MP9 | Ruby Poison Dart (Minimal Wear)`  
   - Link: `https://buff.163.com/goods/35685`  
   - Giá: `¥ 14.6` (hiển thị `¥ 14` và `.6`)

10.  
    - Tên: `StatTrak™ M4A4 | Choppa (Minimal Wear)`  
    - Link: `https://buff.163.com/goods/1115586`  
    - Giá: `¥ 6.66` (hiển thị `¥ 6` và `.66`)

Cuối khối:

- `View market` → `https://buff.163.com/market/csgo#tab=buying`

---

## 5. Khối “Buy Orders” (Lệnh mua)

Tiêu đề: **Buy Orders**

Có 2 tab:

- CS2  
- DOTA2  

Dưới tab CS2, đang hiển thị 10 hàng, mỗi hàng:

- Tên item (link).  
- Lặp lại tên trong `###`.  
- Giá CNY.

### 5.1. Danh sách chi tiết

1.  
   - Tên: `StatTrak™ AK-47 | Fire Serpent (Factory New)`  
   - Link: `https://buff.163.com/goods/44362#tab=buying` (cả 2 vị trí)  
   - Giá: `¥ 27080`

2.  
   - Tên: `M249 | Nebula Crusader (Factory New)`  
   - Link: `https://buff.163.com/goods/35141#tab=buying`  
   - Giá: `¥ 68`

3.  
   - Tên: `MAC-10 | Toybox (Field-Tested)`  
   - Link: `https://buff.163.com/goods/871539#tab=buying`  
   - Giá: `¥ 104`

4.  
   - Tên: `Desert Eagle | Cobalt Disruption (Factory New)`  
   - Link: `https://buff.163.com/goods/34396#tab=buying`  
   - Giá: `¥ 805`

5.  
   - Tên: `StatTrak™ AWP | Capillary (Battle-Scarred)`  
   - Link: `https://buff.163.com/goods/779280#tab=buying`  
   - Giá: `¥ 10.9` (hiển thị `¥ 10` và `.9`)

6.  
   - Tên: `★ Gut Knife | Urban Masked (Field-Tested)`  
   - Link: `https://buff.163.com/goods/42871#tab=buying`  
   - Giá: `¥ 356`

7.  
   - Tên: `M4A4 | 龍王 (Dragon King) (Field-Tested)`  
   - Link: `https://buff.163.com/goods/35354#tab=buying`  
   - Giá: `¥ 98`

8.  
   - Tên: `Glock-18 | Mirror Mosaic (Battle-Scarred)`  
   - Link: `https://buff.163.com/goods/1120052#tab=buying`  
   - Giá: `¥ 28`

9.  
   - Tên: `Dual Berettas | Switch Board (Field-Tested)`  
   - Link: `https://buff.163.com/goods/835409#tab=buying`  
   - Giá: `¥ 19.1` (hiển thị `¥ 19` và `.1`)

10.  
    - Tên: `AWP | Crakow! (Field-Tested)`  
    - Link: `https://buff.163.com/goods/968298#tab=buying`  
    - Giá: `¥ 232`

---

## 6. Khu vực “Account settings”

Tiêu đề: **Account settings**

Các link con:

- `Steam Settings` → `https://buff.163.com/help#N_steam_setting_new`  
- `Developer API` → `https://buff.163.com/developer/documentation`

---

## 7. Khu vực “Wallet Issues”

Tiêu đề: **Wallet Issues**

Các link con:

- `Charging standards` → `https://buff.163.com/help#N_fees_new`  
- `Illegal account publicity` → `https://buff.163.com/help#N_trade_mismatch_illegal`  
- `Guide on Using Alipay for Purchases as a Foreigner` → `https://buff.163.com/help#N_alipay_guide`

---

## 8. Khu vực “FAQ”

Tiêu đề: **FAQ**

Các link con:

- `Buyers FAQ` → `https://buff.163.com/help#N_newbie_faq_buy`  
- `Sellers FAQ` → `https://buff.163.com/help#N_newbie_faq_Seller`  
- `Unable to trade` → `https://buff.163.com/help#N_newbie_faq_Unabletotrade`  
- `Other FAQ` → `https://buff.163.com/help#N_newbie_faq_Other`

---

## 9. Khu vực “Convenient payment”

Tiêu đề: **Convenient payment**

Danh sách phương thức (text):

- Alipay  
- Bank card payments  
- WeChat payment

---

## 10. Khu vực “BUFF APP”

Tiêu đề: **BUFF APP**

Có link “App” ở footer (xem mục 11) trỏ đến trang app riêng.

---

## 11. Footer & thông tin pháp lý

- Text: `网易公司版权所有 ©1997-2026`  
- Link chính sách riêng tư: `网易BUFF隐私政策及儿童个人信息保护规则` → `https://buff.163.com/static/help/privacy_policy.html`  
- Thông tin ICP: `ICP备案：粤B2-20090191-18` → `https://beian.miit.gov.cn/`

Các link tiện ích khác trong footer:

- `App` → `https://buff.163.com/app/`  
- `Favorites` → `https://buff.163.com/user-center/bookmark/sell_order?game=csgo&from=nav`  
- `Official Account` → `#`  
- `Weibo` → `#`  
- `Help` → `https://buff.163.com/help`  
- `Feedback` → `https://buff.163.com/user-center/feedback/`

---
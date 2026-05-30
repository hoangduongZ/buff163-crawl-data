# Buff163 API — `GET /api/market/goods`

Tài liệu tổng hợp tham số request và các field response, dựa trên
`fetch_goods.py` và `data/goods_20260427_180558.json`.

---

## 1. Request Parameters

| Tham số | Kiểu | Bắt buộc | Mô tả |
|---|---|---|---|
| `game` | string | ✅ | Game cần lấy dữ liệu. Giá trị: `"csgo"` hoặc `"dota2"` |
| `page_num` | int | | Trang hiện tại (1-indexed). Mặc định: `1` |
| `page_size` | int | | Số item mỗi trang. Tối đa ~80. Mặc định: `20` |
| `category` | string | | Lọc theo loại vũ khí cụ thể. Ví dụ: `weapon_ak47`, `weapon_awp`, `knife`, `glove` |
| `category_group` | string | | Nhóm category cấp cao hơn |
| `min_price` | number | | Giá sàn tính bằng CNY |
| `max_price` | number | | Giá trần tính bằng CNY |
| `exterior` | string | | Tình trạng bề ngoài item. Xem bảng giá trị bên dưới |
| `quality` | string | | Chất lượng item. Xem bảng giá trị bên dưới |
| `rarity` | string | | Độ hiếm item. Xem bảng giá trị bên dưới |
| `sort_by` | string | | Cách sắp xếp kết quả. Xem bảng giá trị bên dưới |

### Giá trị hợp lệ

**`exterior` — Tình trạng skin**

| Giá trị | Hiển thị |
|---|---|
| `factory_new` | Factory New |
| `minimal_wear` | Minimal Wear |
| `field_tested` | Field-Tested |
| `well_worn` | Well Worn |
| `battle_scarred` | Battle-Scarred |

**`quality` — Chất lượng**

| Giá trị | Hiển thị | Ghi chú |
|---|---|---|
| `normal` | Normal | Item thường |
| `strange` | StatTrak™ | Đếm số kill |
| `tournament` | Souvenir | Item kỷ niệm giải đấu |

**`rarity` — Độ hiếm**

| Giá trị | Hiển thị CS2 |
|---|---|
| `ancient_weapon` | Covert |
| `legendary_weapon` | Classified |
| `mythical_weapon` | Restricted |
| `rare_weapon` | Mil-Spec Grade |

**`sort_by` — Sắp xếp**

| Giá trị | Ý nghĩa |
|---|---|
| `price.asc` | Giá tăng dần |
| `price.desc` | Giá giảm dần |
| `sell_num.desc` | Số lượng bán nhiều nhất |

---

## 2. Response Structure

```
{
  "code": "OK",
  "data": { ... },
  "msg": null
}
```

### 2.1 Root fields

| Field | Kiểu | Mô tả |
|---|---|---|
| `code` | string | Trạng thái API. `"OK"` = thành công |
| `data` | object | Dữ liệu chính |
| `msg` | string\|null | Thông báo lỗi nếu có |

### 2.2 `data` — Phân trang

| Field | Kiểu | Mô tả |
|---|---|---|
| `page_num` | int | Trang hiện tại |
| `page_size` | int | Số item trên trang này |
| `total_page` | int | Tổng số trang |
| `total_count` | int | Tổng số item toàn bộ thị trường |
| `items` | array | Danh sách item (xem mục 2.3) |

> **Ví dụ thực tế:** `page_num=1`, `total_page=1605`, `total_count=32083`

### 2.3 `items[]` — Thông tin từng item

#### Định danh & tên

| Field | Kiểu | Mô tả |
|---|---|---|
| `id` | int | ID item trên Buff163 (goods_id) |
| `appid` | int | Steam App ID. CS2/CSGO = `730` |
| `game` | string | Tên game (`"csgo"`) |
| `name` | string | Tên đầy đủ, bao gồm exterior. Ví dụ: `"AWP | Worm God (Field-Tested)"` |
| `market_hash_name` | string | Tên chuẩn trên Steam Market (dùng để gọi API Steam) |
| `short_name` | string | Tên rút gọn, không có exterior. Ví dụ: `"AWP | Worm God"` |
| `description` | string\|null | Mô tả item (thường `null`) |

#### Giá cả (đơn vị: CNY)

| Field | Kiểu | Mô tả |
|---|---|---|
| `sell_min_price` | string | Giá bán thấp nhất hiện tại trên Buff (người bán thấp nhất) |
| `sell_reference_price` | string | Giá tham chiếu bán — thường bằng `sell_min_price`, dùng để hiển thị |
| `buy_max_price` | string | Giá mua cao nhất hiện tại (người mua trả cao nhất) |
| `quick_price` | string | Giá "quick sell" — thấp hơn `sell_min_price` một chút, dùng để bán nhanh |
| `market_min_price` | string | Giá sàn thị trường (thường `"0"`) |

#### Số lượng giao dịch

| Field | Kiểu | Mô tả |
|---|---|---|
| `sell_num` | int | Số lượng listing đang bán |
| `buy_num` | int | Số lượng lệnh mua đang chờ |
| `transacted_num` | int | Số giao dịch đã hoàn thành (trong kỳ hiện tại, thường `0`) |

#### Đấu giá & pre-sell

| Field | Kiểu | Mô tả |
|---|---|---|
| `auction_num` | int | Số lượng đang đấu giá |
| `pre_sell_num` | int | Số lượng đang pre-sell (bán trước) |
| `pre_sell_min_price` | string | Giá pre-sell thấp nhất. `"0"` nếu không có |

#### Cho thuê (Rent)

| Field | Kiểu | Mô tả |
|---|---|---|
| `rent_num` | int | Số lượng đang cho thuê |
| `rent_unit_reference_price` | string | Giá thuê tham chiếu mỗi ngày (CNY) |
| `min_rent_unit_price` | string | Giá thuê thấp nhất mỗi ngày. `"0"` nếu không có |
| `min_security_price` | string | Đặt cọc tối thiểu khi thuê. `"0"` nếu không có |

#### Tính năng & flags

| Field | Kiểu | Mô tả |
|---|---|---|
| `can_bargain` | bool | Có thể trả giá (bargain) hay không |
| `can_search_by_tournament` | bool | `true` nếu là Souvenir item — có thể lọc theo giải đấu |
| `is_charm` | bool | `true` nếu là keychain/charm |
| `keychain_color_img` | string\|null | URL ảnh màu keychain (nếu là charm) |
| `has_buff_price_history` | bool | Có dữ liệu lịch sử giá trên Buff hay không |
| `bookmarked` | bool | Người dùng đã bookmark item này chưa (yêu cầu auth) |
| `highlight_reel_text` | string | Text nổi bật (thường rỗng `""`) |

#### Link

| Field | Kiểu | Mô tả |
|---|---|---|
| `steam_market_url` | string | URL trang Steam Market của item |

---

### 2.4 `goods_info` — Chi tiết item

| Field | Kiểu | Mô tả |
|---|---|---|
| `icon_url` | string | URL ảnh icon (định dạng WebP, đã tối ưu) |
| `original_icon_url` | string | URL ảnh gốc (chất lượng cao hơn) |
| `steam_price` | string | Giá trên Steam Market tính bằng **USD** |
| `steam_price_cny` | string | Giá trên Steam Market tính bằng **CNY** |
| `item_id` | null | ID nội bộ (thường `null`) |
| `info` | object | Thông tin chi tiết tags |

### 2.5 `goods_info.info.tags` — Tags phân loại

Mỗi tag gồm các field: `id` (int), `category` (string), `internal_name` (string), `localized_name` (string).

| Tag key | Ý nghĩa | Ví dụ `internal_name` |
|---|---|---|
| `exterior` | Tình trạng bề ngoài | `wearcategory0` → FN, `wearcategory1` → MW, `wearcategory2` → FT, `wearcategory3` → WW, `wearcategory4` → BS |
| `quality` | Chất lượng | `normal`, `strange` (StatTrak), `unusual` (★ Knife/Glove), `tournament` (Souvenir) |
| `rarity` | Độ hiếm | `ancient_weapon` (Covert), `legendary_weapon` (Classified), `mythical_weapon` (Restricted), `rare_weapon` (Mil-Spec), `common_weapon` (Consumer), `common` (Base Grade), `ancient` (Extraordinary — Gloves) |
| `type` | Loại item | `csgo_type_rifle`, `csgo_type_pistol`, `csgo_type_smg`, `csgo_type_knife`, `type_hands` (Gloves), `csgo_type_weaponcase`, v.v. |
| `weapon` | Tên vũ khí cụ thể | `weapon_ak47`, `weapon_awp`, `weapon_knife_m9_bayonet`, v.v. |
| `category` | Category lọc (trùng với weapon cho skin) | `weapon_ak47`, `weapon_awp`, v.v. |

> **Lưu ý:** Item không có exterior (như case, keychain) sẽ thiếu tag `exterior` và `weapon`.

---

## 3. Ví dụ thực tế

### Item cao cấp: Knife
```json
{
  "id": 43114,
  "name": "★ M9 Bayonet | Night (Field-Tested)",
  "sell_min_price": "2349",
  "buy_max_price": "2240",
  "sell_num": 98,
  "goods_info": {
    "steam_price": "562.31",
    "steam_price_cny": "3844.12"
  }
}
```
→ Buff/Steam ratio: `2349 / 3844.12 ≈ 0.61` (Buff rẻ hơn ~39%)

### Item phổ thông: Case
```json
{
  "id": 1119940,
  "name": "Sealed Genesis Terminal",
  "sell_min_price": "1.29",
  "buy_max_price": "1.3",
  "sell_num": 14632,
  "pre_sell_num": 92
}
```

---

## 4. Ghi chú

- Tất cả giá trị giá (`sell_min_price`, `buy_max_price`, v.v.) đều là **string** dù là số.
- `steam_price` là USD, `steam_price_cny` là CNY — hai field riêng biệt.
- `transacted_num` thường bằng `0` trong snapshot; cần gọi API riêng để lấy volume giao dịch thực.
- Cần `cookie.txt` hợp lệ để tránh bị block hoặc nhận data không đầy đủ.
- `bookmarked` luôn `false` nếu request không có auth cookie.

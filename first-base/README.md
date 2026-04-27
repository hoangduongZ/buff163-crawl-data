# First Base — Buff163 Fetch Goods

Fetch danh sách goods từ Buff163 API và lưu ra file JSON.

---

## Yêu cầu

- Python 3.8+
- Thư viện `curl_cffi`

---

## Cài đặt

```bash
pip install curl_cffi
```

---

## Chạy

```bash
cd first-base
python3 fetch_goods.py
```

### Output mẫu

```
[warn] cookie.txt not found — request sẽ không có auth, có thể bị block
[fetch] GET https://buff.163.com/api/market/goods
[ok]    API code=OK, nhận 20 items
[save]  /path/to/first-base/data/goods_20260427_180558.json

--- Preview ---
  [43114] ★ M9 Bayonet | Night (Field-Tested) — sell_min: 2349 CNY
  [35078] Glock-18 | Weasel (Field-Tested) — sell_min: 7.96 CNY
  ...
```

---

## Cấu trúc thư mục

```
first-base/
├── fetch_goods.py          # script chính
├── cookie.txt              # (tuỳ chọn) cookie từ browser để auth
└── data/
    └── goods_YYYYMMDD_HHMMSS.json   # file output, tự động đặt tên theo timestamp
```

---

## Dùng cookie (nếu bị block)

1. Mở `buff.163.com` trên Chrome, đăng nhập
2. Mở DevTools (`F12`) → tab **Network** → click bất kỳ request nào tới `buff.163.com`
3. Trong phần **Request Headers**, copy toàn bộ giá trị của dòng `cookie:`
4. Tạo file `first-base/cookie.txt`, paste vào, lưu lại
5. Chạy lại `python3 fetch_goods.py` — lần này sẽ dùng cookie

---

## API đang gọi

```
GET https://buff.163.com/api/market/goods?game=csgo&page_num=1&page_size=20
```

| Param | Giá trị | Ý nghĩa |
|---|---|---|
| `game` | `csgo` | Game CS2/CSGO |
| `page_num` | `1` | Trang đầu |
| `page_size` | `20` | 20 items mỗi trang |

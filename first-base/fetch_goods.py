"""
Bước 1: Fetch danh sách goods từ Buff163 API và lưu ra file JSON.

Endpoint: GET https://buff.163.com/api/market/goods

Tham số hỗ trợ:
  game            string   "csgo" | "dota2"                         (bắt buộc)
  page_num        int      1-indexed                                 (default: 1)
  page_size       int      tối đa ~80                                (default: 20)
  category        string   "weapon_ak47", "weapon_awp", "knife", …
  category_group  string   nhóm category cao hơn
  min_price       number   giá sàn CNY
  max_price       number   giá trần CNY
  exterior        string   "factory_new" | "minimal_wear" |
                           "field_tested" | "well_worn" | "battle_scarred"
  quality         string   "normal" | "strange" (StatTrak) | "tournament" (Souvenir)
  rarity          string   "ancient_weapon" (Covert) | "legendary_weapon" (Classified) |
                           "mythical_weapon" (Restricted) | "rare_weapon" (Mil-Spec)
  sort_by         string   "price.asc" | "price.desc" | "sell_num.desc"
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import curl_cffi.requests as requests

OUTPUT_DIR = Path(__file__).parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

API_URL = "https://buff.163.com/api/market/goods"

# Chỉnh các tham số tại đây trước khi chạy
PARAMS = {
    "game": "csgo",
    "page_num": 1,
    "page_size": 80,
    # --- Lọc ---
    # "category": "weapon_ak47",   # vd: weapon_awp, knife, glove
    # "category_group": "",
    # "min_price": 100,
    # "max_price": 500,
    # "exterior": "factory_new",   # factory_new | minimal_wear | field_tested | well_worn | battle_scarred
    # "quality": "strange",        # normal | strange | tournament
    # "rarity": "ancient_weapon",  # ancient_weapon | legendary_weapon | mythical_weapon | rare_weapon
    # --- Sắp xếp ---
    # "sort_by": "price.asc",      # price.asc | price.desc | sell_num.desc
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://buff.163.com/market/",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(cookie: Optional[str] = None) -> dict:
    headers = HEADERS.copy()
    if cookie:
        headers["Cookie"] = cookie

    response = requests.get(
        API_URL,
        params=PARAMS,
        headers=headers,
        impersonate="chrome124",
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def save(data: dict) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = OUTPUT_DIR / f"goods_{timestamp}.json"
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return out_file


def main():
    cookie_file = Path(__file__).parent / "cookie.txt"
    cookie = cookie_file.read_text().strip() if cookie_file.exists() else None

    if not cookie:
        print("[warn] cookie.txt not found — request sẽ không có auth, có thể bị block")

    print(f"[fetch] GET {API_URL}")
    print(f"[params] {PARAMS}")
    try:
        data = fetch(cookie)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(1)

    code = data.get("code")
    if code != "OK":
        print(f"[error] API trả code={code!r}: {data.get('error', '')}", file=sys.stderr)
        sys.exit(1)

    d = data.get("data", {})
    items = d.get("items", [])
    print(
        f"[ok]    API code=OK, trang {d.get('page_num')}/{d.get('total_page')} "
        f"— {len(items)} items (tổng {d.get('total_count')})"
    )

    out = save(data)
    print(f"[save]  {out}")

    print("\n--- Preview ---")
    for item in items[:5]:
        name = item.get("name", "?")
        price = item.get("sell_min_price", "?")
        goods_id = item.get("id", "?")
        print(f"  [{goods_id}] {name} — sell_min: {price} CNY")


if __name__ == "__main__":
    main()

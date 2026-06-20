"""
Endpoint #3 — GET /api/market/goods/sell_order
Documented as Public. Lists sell orders for a specific item.
Key source for float/sticker sniping.
"""
from _common import call, load_cookie, save_evidence, print_result

URL = "https://buff.163.com/api/market/goods/sell_order"
PARAMS = {
    "game": "csgo",
    "goods_id": 44000,
    "page_num": 1,
    "sort_by": "price.asc",
    "allow_tradable_cooldown": 1,
}

def run():
    cookie = load_cookie()
    status, latency, data, error, raw = call(URL, PARAMS, cookie=cookie)
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/goods/sell_order",
        "params": PARAMS,
        "auth_used": bool(cookie),
        "status_code": status,
        "latency_ms": latency,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        total = data.get("data", {}).get("total_count", "?")
        print(f"code: {data.get('code')}  |  total sell orders: {total}")

    save_evidence("evidence/ep03_sell_order.evidence.json", evidence)

if __name__ == "__main__":
    run()

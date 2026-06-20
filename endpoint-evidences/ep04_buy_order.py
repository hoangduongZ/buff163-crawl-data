"""
Endpoint #4 — GET /api/market/goods/buy_order
Documented as Public. Lists buy orders for a specific item.
"""
from _common import call, load_cookie, save_evidence, print_result

URL = "https://buff.163.com/api/market/goods/buy_order"
PARAMS = {"game": "csgo", "goods_id": 44000, "page_num": 1}

def run():
    cookie = load_cookie()
    status, latency, data, error, raw = call(URL, PARAMS, cookie=cookie)
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/goods/buy_order",
        "params": PARAMS,
        "auth_used": bool(cookie),
        "status_code": status,
        "latency_ms": latency,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        total = data.get("data", {}).get("total_count", "?")
        print(f"code: {data.get('code')}  |  total buy orders: {total}")

    save_evidence("evidence/ep04_buy_order.evidence.json", evidence)

if __name__ == "__main__":
    run()

"""
Endpoint #8 — GET /api/market/goods/price_history/buff
AUTH REQUIRED. Buff163 price history for an item.

Setup: BUFF_COOKIE env var or cookie.txt in this directory.
"""
import sys
from _common import call, load_cookie, save_evidence, print_result

URL = "https://buff.163.com/api/market/goods/price_history"
PARAMS = {"game": "csgo", "goods_id": 44000, "days": 30, "currency": "CNY"}

def run():
    cookie = load_cookie()
    if not cookie:
        print("ERROR: No cookie. Set BUFF_COOKIE env var or create cookie.txt")
        sys.exit(1)

    status, latency, data, error, raw = call(URL, PARAMS, cookie=cookie)
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/goods/price_history/buff",
        "params": PARAMS,
        "auth_used": True,
        "status_code": status,
        "latency_ms": latency,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        total = len(data.get("data", {}).get("price_history", []))
        print(f"code: {data.get('code')}  |  price_history entries: {total}")

    save_evidence("evidence/ep08_price_history.evidence.json", evidence)

if __name__ == "__main__":
    run()

"""
Endpoint #9 — GET /api/market/goods/bill_order
AUTH REQUIRED. Recent transaction history for an item.

Setup: BUFF_COOKIE env var or cookie.txt in this directory.
"""
import sys
from _common import call, load_cookie, save_evidence, print_result

URL = "https://buff.163.com/api/market/goods/bill_order"
PARAMS = {"game": "csgo", "goods_id": 44000}

def run():
    cookie = load_cookie()
    if not cookie:
        print("ERROR: No cookie. Set BUFF_COOKIE env var or create cookie.txt")
        sys.exit(1)

    status, latency, data, error, raw = call(URL, PARAMS, cookie=cookie)
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/goods/bill_order",
        "params": PARAMS,
        "auth_used": True,
        "status_code": status,
        "latency_ms": latency,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        total = data.get("data", {}).get("total_count", "?")
        print(f"code: {data.get('code')}  |  total transactions: {total}")

    save_evidence("evidence/ep09_bill_order.evidence.json", evidence)

if __name__ == "__main__":
    run()

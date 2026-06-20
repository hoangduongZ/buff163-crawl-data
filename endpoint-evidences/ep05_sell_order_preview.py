"""
Endpoint #5 — GET /api/market/sell_order/preview
Documented as Public. Check if a sell order is still available at its listed price.
Fetches a live sell_order_id from ep03 first (requires auth).
"""
import sys
from _common import call, load_cookie, save_evidence, print_result

PREVIEW_URL = "https://buff.163.com/api/market/sell_order/preview"
SELL_ORDER_URL = "https://buff.163.com/api/market/goods/sell_order"

def get_first_sell_order_id(cookie):
    _, _, data, error, _ = call(
        SELL_ORDER_URL,
        {"game": "csgo", "goods_id": 44000, "page_num": 1, "sort_by": "price.asc"},
        cookie=cookie,
    )
    if error or not data:
        return None, error or "empty response"
    items = data.get("data", {}).get("items", [])
    if not items:
        return None, "no items in sell_order response"
    return items[0].get("id"), None

def run():
    cookie = load_cookie()

    sell_order_id, err = get_first_sell_order_id(cookie)
    if err or not sell_order_id:
        print(f"ERROR fetching sell_order_id: {err}")
        print("ep03 (sell_order) must return data first — likely needs cookie.")
        sys.exit(1)

    print(f"Using sell_order_id: {sell_order_id}")

    status, latency, data, error, raw = call(
        PREVIEW_URL,
        {"sell_orders": sell_order_id, "game": "csgo"},
        cookie=cookie,
    )
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/sell_order/preview",
        "params": {"sell_orders": sell_order_id, "game": "csgo"},
        "auth_used": bool(cookie),
        "status_code": status,
        "latency_ms": latency,
        "sell_order_id_used": sell_order_id,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        print(f"code: {data.get('code')}")

    save_evidence("evidence/ep05_sell_order_preview.evidence.json", evidence)

if __name__ == "__main__":
    run()

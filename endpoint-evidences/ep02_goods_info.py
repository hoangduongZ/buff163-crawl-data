"""
Endpoint #2 — GET /api/market/goods/info
Documented as Public. Full metadata for a single item by goods_id.
"""
from _common import call, load_cookie, save_evidence, print_result

URL = "https://buff.163.com/api/market/goods/info"
PARAMS = {"game": "csgo", "goods_id": 44000}

def run():
    cookie = load_cookie()
    status, latency, data, error, raw = call(URL, PARAMS, cookie=cookie)
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/goods/info",
        "params": PARAMS,
        "auth_used": bool(cookie),
        "status_code": status,
        "latency_ms": latency,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        item = data.get("data", {})
        print(f"code: {data.get('code')}  |  name: {item.get('name')}")

    save_evidence("evidence/ep02_goods_info.evidence.json", evidence)

if __name__ == "__main__":
    run()

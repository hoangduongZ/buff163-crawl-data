"""
Endpoint #1 — GET /api/market/goods
Documented as Public. Lists market items for CS2.
"""
from _common import call, load_cookie, save_evidence, print_result

URL = "https://buff.163.com/api/market/goods"
PARAMS = {"game": "csgo", "page_num": 1, "page_size": 3}

def run():
    cookie = load_cookie()
    status, latency, data, error, raw = call(URL, PARAMS, cookie=cookie)
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/goods",
        "params": PARAMS,
        "auth_used": bool(cookie),
        "status_code": status,
        "latency_ms": latency,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        total = data.get("data", {}).get("total_count", "?")
        print(f"code: {data.get('code')}  |  total_count: {total}")

    save_evidence("evidence/ep01_goods.evidence.json", evidence)

if __name__ == "__main__":
    run()

"""
Endpoint #7a — GET /api/market/category
Documented as Public. Returns all categories and tag IDs for CS2.
NOTE: Currently returns "Path Not Found" — endpoint may be deprecated or path incorrect.
"""
from _common import call, load_cookie, save_evidence, print_result

URL = "https://buff.163.com/api/market/category"
PARAMS = {"game": "csgo"}

def run():
    cookie = load_cookie()
    status, latency, data, error, raw = call(URL, PARAMS, cookie=cookie)
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/category",
        "params": PARAMS,
        "auth_used": bool(cookie),
        "status_code": status,
        "latency_ms": latency,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        print(f"code: {data.get('code')}")

    save_evidence("evidence/ep07_category.evidence.json", evidence)

if __name__ == "__main__":
    run()

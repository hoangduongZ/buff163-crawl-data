"""
Endpoint #10 — GET /api/market/steam_price_history
Documented as Public. Steam market price history for an item.
NOTE: Currently returns "Path Not Found" — endpoint may be deprecated or path incorrect.
"""
from _common import call, load_cookie, save_evidence, print_result

URL = "https://buff.163.com/api/market/steam_price_history"
PARAMS = {"game": "csgo", "market_hash_name": "★ Bayonet | Night (Factory New)"}

def run():
    cookie = load_cookie()
    status, latency, data, error, raw = call(URL, PARAMS, cookie=cookie)
    print_result(status, latency, error)

    evidence = {
        "endpoint": "/api/market/steam_price_history",
        "params": PARAMS,
        "auth_used": bool(cookie),
        "status_code": status,
        "latency_ms": latency,
        "error": error,
        "raw_response": data if data else raw,
    }

    if data:
        print(f"code: {data.get('code')}")

    save_evidence("evidence/ep10_steam_price_history.evidence.json", evidence)

if __name__ == "__main__":
    run()

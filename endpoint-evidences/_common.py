"""Shared helpers for all endpoint verification scripts."""
import json, os, sys, time
from curl_cffi import requests as cf_requests

HEADERS_BASE = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://buff.163.com/market/",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
}

def load_cookie():
    cookie_str = os.environ.get("BUFF_COOKIE")
    if cookie_str:
        return cookie_str
    cookie_file = os.path.join(os.path.dirname(__file__), "cookie.txt")
    if os.path.exists(cookie_file):
        with open(cookie_file) as f:
            return f.read().strip()
    return None

def call(url, params=None, cookie=None):
    headers = dict(HEADERS_BASE)
    if cookie:
        headers["Cookie"] = cookie

    t0 = time.time()
    r = cf_requests.get(url, params=params, headers=headers, impersonate="chrome124", timeout=15)
    latency_ms = int((time.time() - t0) * 1000)

    content_type = r.headers.get("content-type", "")
    is_json = "json" in content_type or (r.text.strip().startswith("{") and "DOCTYPE" not in r.text)

    if not is_json:
        # Buff redirected to login page
        return r.status_code, latency_ms, None, "AUTH_REQUIRED — response is HTML (login page redirect)", r.text[:500]

    try:
        data = r.json()
    except Exception as e:
        return r.status_code, latency_ms, None, f"JSON_PARSE_ERROR: {e}", r.text[:500]

    return r.status_code, latency_ms, data, None, r.text

def save_evidence(filename, payload):
    with open(filename, "w") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"\nEvidence saved → {filename}")

def print_result(status_code, latency_ms, error):
    if error:
        print(f"HTTP {status_code}  |  {latency_ms}ms  |  ⚠️  {error}")
    else:
        print(f"HTTP {status_code}  |  {latency_ms}ms  |  ✅ JSON received")

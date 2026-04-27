# BUFF Inspect Capture

## 1) Request Summary

- Request URL: `https://buff.163.com/api/message/notification?_=1777214443670`
- Request Method: `GET`
- Status Code: `200 OK`
- Remote Address: `106.2.95.192:443`
- Referrer Policy: `strict-origin-when-cross-origin`

## 2) Response Headers

| Header | Value |
|---|---|
| content-encoding | gzip |
| content-type | application/json |
| date | Sun, 26 Apr 2026 14:40:45 GMT |
| ntes-trace-id | 22ef13a0aaab4593:22ef13a0aaab4593:0:0 |
| server | nginx |
| set-cookie | client_id=qm4KzMNn7irFab0PUHHkdw; HttpOnly; Path=/ |
| set-cookie | display_appids_v2="[730\054 570]"; HttpOnly; Path=/ |
| set-cookie | csrf_token=IjUwNTU4MzI5ZWU2ODU1Y2Y3ZWQ2MGE2OTJhNmU5YmYyYmM4YjdjYzYi.ae4j7Q.4tFFi8QS8qQkKQHItLbDSadfeR0; Path=/ |
| x-envoy-upstream-service-time | 4 |
| x-trace-id | e4c90d990937f02ad19dc65dd0f5305d |

## 3) Request Headers

| Header | Value |
|---|---|
| :authority | buff.163.com |
| :method | GET |
| :path | /api/message/notification?_=1777214443670 |
| :scheme | https |
| accept | */* |
| accept-encoding | gzip, deflate, br, zstd |
| accept-language | en-US,en;q=0.9 |
| cookie | Device-Id=oylzTOmQBhRrR1pSHkeV; client_id=qm4KzMNn7irFab0PUHHkdw; Locale-Supported=en; game=csgo; display_appids_v2="[730\054 570]"; csrf_token=IjViZDM0OGM5MzFlY2YwODk0OGE3YWJlZjQ0NGEyMzAwNTI0ZGRjZjQi.ae4j6w.ffwgzFR7En06dJkZ6lGkMJxZkdI |
| priority | u=1, i |
| referer | https://buff.163.com/ |
| sec-ch-ua | "Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145" |
| sec-ch-ua-mobile | ?0 |
| sec-ch-ua-platform | "macOS" |
| sec-fetch-dest | empty |
| sec-fetch-mode | cors |
| sec-fetch-site | same-origin |
| user-agent | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 |
| x-requested-with | XMLHttpRequest |

## 4) Query Parameters

| Name | Type | Value |
|---|---|---|
| _ | query-string parameter | 1777214443670 |

## 5) Response Body

```json
{
    "code": "OK",
    "data": {
        "unread_message": {
            "total": 0
        },
        "to_deliver_order": {
            "dota2": 0,
            "pubg": 0
        },
        "to_receive_order": {
            "dota2": 0,
            "pubg": 0
        },
        "unread_feedback_replay": {
            "total": 0
        },
        "unread_system_message": {
            "total": 0
        },
        "unread_social_message": {
            "total": 0
        },
        "unread_social_comment_message": {
            "total": 0
        },
        "unread_social_up_message": {
            "total": 0
        },
        "new_roll_room": {
            "has_new": false
        },
        "new_coupon": {
            "total": 0
        },
        "unread_sell_bargain_chat_message": {
            "dota2": 0,
            "pubg": 0
        },
        "unread_buy_bargain_chat_message": {
            "dota2": 0,
            "pubg": 0
        },
        "to_send_offer_order": {
            "dota2": 0,
            "pubg": 0
        },
        "to_accept_offer_order": {
            "dota2": 0,
            "pubg": 0
        },
        "to_handle_bargain": {
            "dota2": 0,
            "pubg": 0
        },
        "to_pay_order": {
            "dota2": 0,
            "pubg": 0
        },
        "to_pay_bargain": {
            "dota2": 0,
            "pubg": 0
        },
        "to_pay_buy_order": {
            "dota2": 0,
            "pubg": 0
        },
        "fast_supply": {
            "dota2": 0,
            "pubg": 0
        },
        "to_confirm_buy": {
            "dota2": 0,
            "pubg": 0
        },
        "to_confirm_sell": {
            "dota2": 0,
            "pubg": 0
        },
        "to_deliver_rent": {
            "dota2": 0,
            "pubg": 0
        },
        "to_send_offer_rent": {
            "dota2": 0,
            "pubg": 0
        },
        "to_accept_offer_rent": {
            "dota2": 0,
            "pubg": 0
        },
        "to_receive_return_rent": {
            "dota2": 0,
            "pubg": 0
        },
        "to_pay_rent": {
            "dota2": 0,
            "pubg": 0
        },
        "to_return_rent": {
            "dota2": 0,
            "pubg": 0
        },
        "auction_buyer": {
            "dota2": 0,
            "pubg": 0
        },
        "auction_seller": {
            "dota2": 0,
            "pubg": 0
        },
        "auction_buyer_end": {
            "dota2": 0,
            "pubg": 0
        },
        "to_deliver_pre_sell": {
            "dota2": 0,
            "pubg": 0
        },
        "updated_at": {}
    },
    "msg": null
}
```

## 6) Cookies (as captured)

| Name | Value | Domain | Path | Expires | Size | HttpOnly | Priority |
|---|---|---|---|---|---|---|---|
| Device-Id | oylzTOmQBhRrR1pSHkeV | buff.163.com | / | 2027-05-31T13:52:38.145Z | 29 |  | Medium |
| Locale-Supported | en | buff.163.com | / | Session | 18 |  | Medium |
| client_id | qm4KzMNn7irFab0PUHHkdw | buff.163.com | / | Session | 31 | ✓ | Medium |
| csrf_token | IjViZDM0OGM5MzFlY2YwODk0OGE3YWJlZjQ0NGEyMzAwNTI0ZGRjZjQi.ae4j6w.ffwgzFR7En06dJkZ6lGkMJxZkdI | buff.163.com | / | Session | 101 |  | Medium |
| display_appids_v2 | "[730\054 570]" | buff.163.com | / | Session | 32 | ✓ | Medium |
| game | csgo | buff.163.com | / | Session | 8 |  | Medium |
| client_id | qm4KzMNn7irFab0PUHHkdw | buff.163.com | / | Session | 51 | ✓ | Medium |
| csrf_token | IjUwNTU4MzI5ZWU2ODU1Y2Y3ZWQ2MGE2OTJhNmU5YmYyYmM4YjdjYzYi.ae4j7Q.4tFFi8QS8qQkKQHItLbDSadfeR0 | buff.163.com | / | Session | 110 |  | Medium |
| display_appids_v2 | "[730\054 570]" | buff.163.com | / | Session | 52 | ✓ | Medium |
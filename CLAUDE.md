# CLAUDE.md — Buff163 CS2 Sniper

**Project**: Sniping tool phát hiện mispricing sell order Buff163, notify real-time. macOS M1 Pro, 1 user, local-only. Stage: planning / early build.

---

## Đọc doc theo loại task

| Task | Đọc trước |
|---|---|
| Feature / architecture / stack | `doc/tool-spec/tool-spec.md` + `doc/tool-spec/tech-stack.md` |
| API / crawling / endpoint | `doc/tool-spec/endpoints.md` |
| Business / trading logic | `doc/business-logic/trading-strategy.md` |

Không đọc tất cả mọi lúc — chỉ đọc khi task liên quan.

---

## Workflow

Rule đầy đủ: `workspace/WORKFLOW-RULE/rules_vie.md`  
Template: `workspace/WORKFLOW-RULE/template/TICKET_ID/`  
Ticket folder: `workspace/tasks/<ticket-id>/`

| Chế độ | Khi nào | Files |
|---|---|---|
| **Lightweight** | ≤ 2 file, < 30 min | `plan_YYYYMMDD_00.md` → code → `handover.md` → `README.md` |
| **Standard** | Feature / refactor / ≥ 3 file | + `impl_`, `test_`, `problem_` (nếu có) |

`plan_` phải có trước khi sửa code. Ghi chép: bullet points, tối đa 5 dòng/section.

---

## Hard Constraints

- HTTP: chỉ dùng `curl_cffi` — không `requests`/`httpx` (Buff detect TLS fingerprint)
- Max 3 concurrent request (`asyncio.Semaphore(3)`)
- Không commit cookie/session lên git
- Không auto-buy cho đến khi tool ổn ≥ 1 tháng
- Build order: polling → notify → persistence → dashboard (không đảo)

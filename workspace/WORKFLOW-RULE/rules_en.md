# AI Markdown Folder Workflow Rule

You are an AI coding agent supporting software development tasks and tickets.

Your responsibility is not only to modify code, but also to organize Markdown documentation so that a future AI session can resume without re-asking from the beginning.

---

## 1. Folder Structure

```txt
docs/<ticket-id>/
├── README.md
├── plan_YYYYMMDD_00.md
├── impl_YYYYMMDD_00.md       (Standard mode only)
├── problem_YYYYMMDD_00.md    (create only if problems occur)
├── test_YYYYMMDD_00.md       (Standard mode only)
└── handover.md
```

---

## 2. Working Mode

Choose a mode before starting the task:

| Mode | When to use | Files required |
|---|---|---|
| **Lightweight** | ≤ 2 files changed, task < 30 min, small fix / config / copy | `plan_` → code → `handover` → `README` |
| **Standard** | New feature, refactor, ≥ 3 files changed | `plan_` → code → `impl_` → `test_` → `handover` → `README` |

In Lightweight mode: write impl summary and test result directly in `handover.md`.

---

## 3. File Meaning

| File | Purpose |
|---|---|
| `README.md` | Navigation: status + latest files |
| `plan_YYYYMMDD_NN.md` | Requirement + context + analysis + plan |
| `impl_YYYYMMDD_NN.md` | Changed files, what, why, key logic |
| `problem_YYYYMMDD_NN.md` | Errors, root cause, solution |
| `test_YYYYMMDD_NN.md` | Commands, test cases, results |
| `handover.md` | Session summary — enough to resume next time |

---

## 4. File Naming

```txt
plan_YYYYMMDD_00.md      (increment counter if re-created same day)
impl_YYYYMMDD_00.md
problem_YYYYMMDD_00.md
test_YYYYMMDD_00.md
```

Stable (overwrite directly): `README.md`, `handover.md`

Do not use: `final.md`, `new.md`, `note.md`, `latest.md`.

---

## 5. Lifecycle

**Lightweight:**
```
1. Create folder + plan_YYYYMMDD_00.md
2. Code
3. Update handover.md  (include impl summary + test result)
4. Update README.md
```

**Standard:**
```
1. Create folder + plan_YYYYMMDD_00.md
2. Code
3. Create impl_YYYYMMDD_00.md
4. If problems occur → create problem_YYYYMMDD_00.md
5. Create test_YYYYMMDD_00.md
6. Update handover.md
7. Update README.md
```

---

## 6. Rule Before Coding

`plan_` must exist before modifying any code.

Required content — **bullet points, max 5 lines per section, no prose**:

* **Requirement** — what needs to be done
* **Context** — branch, affected modules/APIs/DB (non-obvious only)
* **Current behavior**
* **Expected behavior**
* **Implementation steps** — short ordered list
* **Test plan** — checklist

Add **Risks / Open Questions** only if non-trivial.

---

## 7. Writing Rules

Apply to **every file**:
- Bullet points only — no paragraphs
- Max 5 lines per section
- Only record what is non-obvious from reading the code
- Never repeat information already present in another file

**`impl_`**: table of changed files + logic not obvious from the diff.

**`problem_`**: error log → root cause → fix → status.

**`test_`**: commands + test case table (expected / actual / status).

---

## 8. Rule After Coding

**`handover.md`** — enough to resume next session, keep it concise:
* Status
* What was done (bullets)
* Changed files (table)
* Test result (1 line)
* Remaining tasks
* Specific next steps

**`README.md`** — only update 2 things: Status + Latest Files table.

---

## 9. README.md

```md
# Ticket <ticket-id>

## Status
In Progress / Done / Blocked / Waiting Confirmation

## Summary
<!-- 1 line -->

## Latest Files

| Type | File |
|---|---|
| Plan | `plan_YYYYMMDD_NN.md` |
| Implementation | `impl_YYYYMMDD_NN.md` (if any) |
| Problem | `problem_YYYYMMDD_NN.md` (if any) |
| Test | `test_YYYYMMDD_NN.md` (if any) |
| Handover | `handover.md` |
```

> No "Next Action" in README — read `handover.md` instead.

---

## 10. Core Principles

* `plan_` first, code second.
* Bullet points, no prose, max 5 lines per section.
* Only record what is non-obvious from code.
* Never repeat information across files.
* Never overwrite versioned files.
* Every file must be readable by a fresh AI session with no prior context.

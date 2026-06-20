# AI Markdown Folder Workflow Rule

You are an AI coding agent supporting software development tasks and tickets.

Your responsibility is not only to modify code, but also to organize Markdown documentation using a standard workflow so that you (or a future AI session) can resume the task without re-asking from the beginning.

---

## 1. Purpose

For every coding task or ticket, create a dedicated folder that stores all related Markdown documents.

Goals:
* Capture the original requirement.
* Record technical context (non-obvious only).
* Record analysis before coding.
* Record implementation details.
* Record problems and debugging history.
* Record build/test results.
* Record handover for the next AI session.

---

## 2. Standard Folder Structure

```txt
docs/<ticket-id>/
├── README.md
├── 00_original/
│   └── index.md
├── 01_context/
│   └── context.md
├── 02_analysis/
│   └── plan-and-analysis_YYYYMMDD_00.md
├── 03_implementation/
│   └── implementation_YYYYMMDD_00.md
├── 04_problem/                        (create only if problems occur)
│   └── problem_YYYYMMDD_00.md
├── 05_test/
│   └── test-result_YYYYMMDD_00.md
└── 99_handover/
    └── handover.md
```

---

## 3. Folder Meaning

| Folder              | Purpose                                                      |
| ------------------- | ------------------------------------------------------------ |
| `00_original`       | Original ticket content                                      |
| `01_context`        | Non-obvious context: branch, modules, APIs, DB tables        |
| `02_analysis`       | Requirement analysis and implementation plan before coding   |
| `03_implementation` | Implementation log: changed files, what, why                 |
| `04_problem`        | Errors, root causes, investigation steps, solutions          |
| `05_test`           | Build/test commands and results                              |
| `99_handover`       | Session summary — enough to resume next time without re-asking |

---

## 4. File Naming Rules

Stable files:
```txt
README.md
00_original/index.md
01_context/context.md
99_handover/handover.md
```

Versioned files (date + counter, never overwrite):
```txt
02_analysis/plan-and-analysis_YYYYMMDD_COUNTER.md
03_implementation/implementation_YYYYMMDD_COUNTER.md
04_problem/problem_YYYYMMDD_COUNTER.md
05_test/test-result_YYYYMMDD_COUNTER.md
```

Counter starts from `00`. Increment if the same type is created multiple times on the same day.

Do not use vague names: `final.md`, `new.md`, `note.md`, `latest.md`, `fix.md`.

---

## 5. Lifecycle

Process each task in this order:

```
1. Create folder → save requirement in 00_original/index.md
2. Write context in 01_context/context.md
3. Write analysis in 02_analysis/plan-and-analysis_YYYYMMDD_00.md
4. Implement code
5. Record implementation in 03_implementation/
6. If problems occur → create 04_problem/ (on-demand)
7. Record test results in 05_test/
8. Update 99_handover/handover.md + README.md
```

---

## 6. Rule Before Coding

Before modifying any code, these files must exist:

```txt
00_original/index.md
01_context/context.md
02_analysis/plan-and-analysis_YYYYMMDD_00.md
```

The `plan-and-analysis` file must include:
* Requirement
* Current behavior
* Expected behavior
* Affected files / modules / APIs / DB tables
* Implementation steps
* Test plan

Add **Risks** or **Open Questions** only if non-trivial.

---

## 7. Rule During Coding

Record in `03_implementation/`:
* Changed files
* What was changed and why
* Key logic changes
* API / DB / config impact if any

If any error or blocker occurs, create a file in `04_problem/`:
* When it happened
* Full error log
* Root cause
* Investigation steps
* Solution or workaround
* Current status

---

## 8. Rule After Coding

Create or update:
```txt
05_test/test-result_YYYYMMDD_COUNTER.md
99_handover/handover.md
README.md
```

`test-result` must include:
* Commands executed
* Test cases → expected → actual → status

`handover.md` must include enough to resume next session without re-asking:
* Status
* Completed work + changed files
* Test result summary
* Remaining tasks
* How to continue

---

## 9. README.md Rule

`README.md` is the navigation index. Keep it short.

Required content:
```md
# Ticket <ticket-id>

## Status
In Progress / Done / Blocked / Waiting Confirmation

## Summary
One-line task summary.

## Latest Files

| Type | File |
|---|---|
| Latest analysis | `02_analysis/...` |
| Latest implementation | `03_implementation/...` |
| Latest problem | `04_problem/...` (if any) |
| Latest test result | `05_test/...` |
| Handover | `99_handover/handover.md` |

## Next Action
Write next action here.
```

---

## 10. Core Principles

* Analyze before coding.
* Document while coding.
* Record problems when they happen.
* Never overwrite old versioned files.
* Write only what is non-obvious — skip information derivable from reading the code.
* Every file must be readable by a fresh AI session with no prior context.

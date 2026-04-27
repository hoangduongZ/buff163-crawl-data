# VS Code Python Extensions — Đã cài

## Lệnh cài đặt

```bash
# Lần 1 — bộ Python core
code --install-extension ms-python.python \
  ms-python.vscode-pylance \
  ms-python.debugpy \
  charliermarsh.ruff \
  ms-python.mypy-type-checker \
  usernamehw.errorlens \
  oderwat.indent-rainbow \
  tamasfe.even-better-toml \
  mikestead.dotenv \
  eamodio.gitlens

# Lần 2 — cài lại với flag đúng cú pháp (từng --install-extension)
code --install-extension charliermarsh.ruff \
  --install-extension ms-python.mypy-type-checker \
  --install-extension usernamehw.errorlens \
  --install-extension oderwat.indent-rainbow \
  --install-extension tamasfe.even-better-toml \
  --install-extension mikestead.dotenv \
  --install-extension eamodio.gitlens
```

---

## Danh sách extension đã cài

| # | Tên | Extension ID | Phiên bản | Mục đích |
|---|---|---|---|---|
| 1 | **Python** | `ms-python.python` | v2026.4.0 | Extension Python chính thức — IntelliSense, linting, quản lý môi trường ảo |
| 2 | **Pylance** | `ms-python.vscode-pylance` | v2026.2.1 | Language server mạnh — type inference, auto-import, phân tích code tĩnh |
| 3 | **Python Debugger (Debugpy)** | `ms-python.debugpy` | v2025.18.0 | Debugger chính thức — đặt breakpoint, inspect variable, step through code |
| 4 | **Python Envs** | `ms-python.vscode-python-envs` | v1.28.0 | Quản lý virtual environment (venv, conda, pyenv) — cài tự động kèm Python |
| 5 | **Ruff** | `charliermarsh.ruff` | v2026.40.0 | Linter + formatter cực nhanh — thay thế flake8, black, isort trong 1 extension |
| 6 | **Mypy Type Checker** | `ms-python.mypy-type-checker` | v2025.2.0 | Kiểm tra kiểu tĩnh (static type checking) với mypy |
| 7 | **Error Lens** | `usernamehw.errorlens` | v3.28.0 | Hiển thị lỗi và warning trực tiếp inline trên dòng code, không cần hover |
| 8 | **indent-rainbow** | `oderwat.indent-rainbow` | v8.3.1 | Tô màu các mức indent — rất hữu ích với Python vì indent có nghĩa cú pháp |
| 9 | **Even Better TOML** | `tamasfe.even-better-toml` | v0.21.2 | IntelliSense và syntax highlight cho file `pyproject.toml`, `Cargo.toml` |
| 10 | **DotENV** | `mikestead.dotenv` | v1.0.1 | Syntax highlight cho file `.env` — dễ đọc biến môi trường |
| 11 | **GitLens** | `eamodio.gitlens` | v17.12.2 | Git blame inline, lịch sử commit, so sánh diff mạnh hơn built-in Git |

---

## Sau khi cài

Reload VS Code để extension có hiệu lực:

```
Cmd+Shift+P → Reload Window
```

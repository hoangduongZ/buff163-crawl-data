# VS Code Extensions cho Python Development

## Bắt buộc cài

| Extension | ID | Mô tả |
|---|---|---|
| **Python** | `ms-python.python` | Extension chính thức của Microsoft — IntelliSense, linting, debugging, environments |
| **Pylance** | `ms-python.vscode-pylance` | Language server mạnh, type checking tĩnh, auto-import |
| **Python Debugger** | `ms-python.debugpy` | Debugger chính thức (thường đi kèm Python extension) |

---

## Chất lượng code

| Extension | ID | Mô tả |
|---|---|---|
| **Ruff** | `charliermarsh.ruff` | Linter + formatter cực nhanh (thay thế flake8, isort, black) — **khuyên dùng** |
| **Black Formatter** | `ms-python.black-formatter` | Formatter black tích hợp sâu vào VS Code |
| **isort** | `ms-python.isort` | Tự động sắp xếp import |
| **Mypy Type Checker** | `ms-python.mypy-type-checker` | Static type checking với mypy |

> **Gợi ý:** Dùng **Ruff** là đủ thay cho Black + isort + flake8.

---

## Testing

| Extension | ID | Mô tả |
|---|---|---|
| **Python Test Explorer** | `littlefoxteam.vscode-python-test-adapter` | Giao diện chạy pytest/unittest trực quan |
| **Coverage Gutters** | `ryanluker.vscode-coverage-gutters` | Hiển thị code coverage trực tiếp trên editor |

---

## Jupyter / Data

| Extension | ID | Mô tả |
|---|---|---|
| **Jupyter** | `ms-toolsai.jupyter` | Chạy notebook `.ipynb` trong VS Code |
| **Jupyter Keymap** | `ms-toolsai.jupyter-keymap` | Keybinding của Jupyter trong VS Code |

---

## Tiện ích chung

| Extension | ID | Mô tả |
|---|---|---|
| **GitLens** | `eamodio.gitlens` | Git blame, history, diff mạnh hơn built-in |
| **Git Graph** | `mhutchie.git-graph` | Visualize git branch graph |
| **Docker** | `ms-azuretools.vscode-docker` | Quản lý container, viết Dockerfile |
| **YAML** | `redhat.vscode-yaml` | IntelliSense cho YAML (config, CI/CD) |
| **TOML** | `tamasfe.even-better-toml` | IntelliSense cho `pyproject.toml` |
| **DotENV** | `mikestead.dotenv` | Syntax highlight file `.env` |
| **indent-rainbow** | `oderwat.indent-rainbow` | Tô màu indent — rất hữu ích với Python |
| **Error Lens** | `usernamehw.errorlens` | Hiển thị lỗi inline ngay trên dòng code |
| **Path Intellisense** | `christian-kohler.path-intellisense` | Autocomplete đường dẫn file |

---

## AI Assistant (chọn 1)

| Extension | ID | Mô tả |
|---|---|---|
| **GitHub Copilot** | `github.copilot` | AI code completion phổ biến nhất |
| **Codeium** | `codeium.codeium` | Miễn phí, tương tự Copilot |

---

## Cài nhanh qua terminal

```bash
# Bắt buộc
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy

# Chất lượng code
code --install-extension charliermarsh.ruff
code --install-extension ms-python.mypy-type-checker

# Tiện ích
code --install-extension usernamehw.errorlens
code --install-extension oderwat.indent-rainbow
code --install-extension tamasfe.even-better-toml
code --install-extension mikestead.dotenv
code --install-extension eamodio.gitlens
```

---

## Cấu hình settings.json gợi ý

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },
  "python.languageServer": "Pylance",
  "python.analysis.typeCheckingMode": "basic",
  "mypy-type-checker.importStrategy": "useBundled"
}
```

# Python cho Java Developer — Đủ để đọc hiểu code Buff Crawler

> **Mục tiêu**: Sau khi đọc xong, bạn đọc được toàn bộ 3 file Python tôi generate (`buff_crawler.py`, `buff_item_orders.py`, `buff_monitor.py`) và sửa được logic đơn giản.
>
> **Không mục tiêu**: Trở thành Python expert. Bỏ qua: metaclass, descriptor, asyncio internal, GIL deep-dive, packaging system phức tạp.

---

## 1. Mental model — khác biệt cốt lõi

### 1.1 Indentation thay vì `{}`

Đây là shock đầu tiên của Java dev. Python **không có** dấu ngoặc nhọn — block code được xác định bởi **độ thụt đầu dòng**.

**Java:**
```java
if (price > 100) {
    System.out.println("expensive");
    if (price > 1000) {
        System.out.println("very expensive");
    }
}
```

**Python:**
```python
if price > 100:
    print("expensive")
    if price > 1000:
        print("very expensive")
```

Quy tắc:
- Sau `:` luôn có block thụt vào (4 spaces là convention, KHÔNG dùng tab)
- Cùng cấp = cùng số space
- Lỗi indentation = `IndentationError`, code không chạy

### 1.2 Không có type declaration bắt buộc

**Java:**
```java
String name = "AK-47";
int price = 100;
List<String> items = new ArrayList<>();
```

**Python:**
```python
name = "AK-47"
price = 100
items = []
```

Type **suy ra từ giá trị** (dynamic typing). Biến có thể đổi type bất cứ lúc nào (nhưng đừng làm vậy):
```python
x = 5           # int
x = "hello"     # giờ là string — Java không cho phép
x = [1, 2, 3]   # giờ là list
```

### 1.3 Type hints (optional) — giống Java generic nhưng không bắt buộc

Python 3.5+ có **type hints** — nhìn giống Java nhưng **runtime KHÔNG check**, chỉ giúp IDE/linter:

```python
def fetch_page(page_num: int, game: str) -> dict:
    # int, str, dict chỉ là gợi ý
    # truyền page_num="abc" vẫn chạy (sẽ lỗi runtime sau)
    return {}

name: str = "AK"
prices: list[float] = [10.5, 20.3]
```

→ Trong code tôi viết có nhiều type hints, đọc như đọc Java generic là được.

### 1.4 `None` thay vì `null`

```java
String x = null;
if (x == null) { ... }
```

```python
x = None
if x is None:        # convention: dùng `is None`, không dùng `== None`
    ...
```

`None` là **singleton** — chỉ có 1 instance trong toàn chương trình. Vì vậy dùng `is` (so sánh identity) chứ không dùng `==`.

### 1.5 Không có `;` cuối dòng

Mỗi dòng = 1 statement. Hết dòng = hết statement, không cần `;`.

Nếu dòng quá dài, dùng `\` hoặc bọc trong `()` `[]` `{}`:
```python
total = (price * quantity 
         + tax 
         - discount)
```

### 1.6 `print()` thay vì `System.out.println()`

```python
print("hello")
print("price:", 100, "name:", "AK")    # ngăn cách bằng space tự động
print(f"price = {price}, name = {name}")  # f-string, giống String.format
```

f-string (`f"..."`) là cách format chuỗi phổ biến nhất — như JavaScript template literal:
```python
name = "AK"
price = 100
msg = f"Item {name} costs {price} CNY"
# = "Item AK costs 100 CNY"
```

---

## 2. Type cơ bản — mapping với Java

| Python | Java tương đương | Ghi chú |
|---|---|---|
| `int` | `long` (không giới hạn) | Python int **không overflow** |
| `float` | `double` | Không có `float` 32-bit |
| `bool` | `boolean` | Viết hoa: `True` / `False` |
| `str` | `String` | Immutable |
| `list` | `ArrayList` | `[1, 2, 3]` |
| `tuple` | `List.of(...)` (immutable) | `(1, 2, 3)` |
| `dict` | `HashMap` | `{"key": "value"}` |
| `set` | `HashSet` | `{1, 2, 3}` |
| `None` | `null` | |

### 2.1 List

**Java:**
```java
List<String> names = new ArrayList<>();
names.add("AK");
names.add("M4");
String first = names.get(0);
int size = names.size();
```

**Python:**
```python
names = []                  # khởi tạo rỗng
names.append("AK")
names.append("M4")
first = names[0]            # indexing trực tiếp
size = len(names)           # KHÔNG có .size(), dùng len()
```

Slice (cắt list) — Python rất mạnh ở đây:
```python
arr = [10, 20, 30, 40, 50]
arr[0]      # 10 — phần tử đầu
arr[-1]     # 50 — phần tử cuối (negative index)
arr[1:3]    # [20, 30] — từ index 1 tới TRƯỚC index 3
arr[:2]     # [10, 20] — 2 đầu tiên
arr[-2:]    # [40, 50] — 2 cuối
```

### 2.2 Dict (= Java Map)

**Java:**
```java
Map<String, Object> item = new HashMap<>();
item.put("name", "AK-47");
item.put("price", 100);
String name = (String) item.get("name");
```

**Python:**
```python
item = {"name": "AK-47", "price": 100}
name = item["name"]              # KeyError nếu không tồn tại
name = item.get("name")          # trả None nếu không tồn tại
name = item.get("name", "N/A")   # trả "N/A" nếu không tồn tại
```

→ `.get()` rất phổ biến trong code crawler vì JSON từ API có thể thiếu field.

Iterate:
```python
for key in item:                       # iterate keys
    print(key, item[key])

for key, value in item.items():        # iterate cả key và value (giống entrySet)
    print(key, value)

for value in item.values():            # chỉ values
    print(value)
```

### 2.3 Tuple — list không sửa được

```python
point = (10, 20)        # immutable
point[0]                # 10
# point[0] = 5          # ERROR — không sửa được
```

Đặc biệt, Python **return nhiều giá trị** bằng tuple:
```python
def get_min_max(arr):
    return min(arr), max(arr)        # return tuple

low, high = get_min_max([1, 5, 3])   # unpack — Java không có
print(low, high)                     # 1 5
```

→ Trong code tôi có dòng `changes, alerts = diff_and_alert(...)` — đây là tuple unpacking.

### 2.4 String

```python
s = "hello"
s.upper()              # "HELLO"
s.lower()              # "hello"
s.strip()              # bỏ space đầu cuối, như String.trim()
s.split(",")           # ["hello"] — như Java
s.replace("h", "H")    # "Hello"
"A" in "AK-47"         # True — substring check, gọn hơn .contains()
len(s)                 # 5 — không có .length()
```

f-string (đã thấy ở trên):
```python
price = 100.5
f"Price: {price}"           # "Price: 100.5"
f"Price: {price:.2f}"       # "Price: 100.50" — 2 chữ số thập phân
f"Hex: {255:x}"             # "Hex: ff"
```

---

## 3. Function — KEY DIFFERENCES

### 3.1 Định nghĩa function

**Java:**
```java
public int add(int a, int b) {
    return a + b;
}
```

**Python:**
```python
def add(a, b):
    return a + b

# Với type hints (encouraged):
def add(a: int, b: int) -> int:
    return a + b
```

Không có `public/private/protected` — convention dùng `_` ở đầu tên:
```python
def public_function():       # public
    pass

def _private_function():     # convention private (vẫn gọi được, chỉ là quy ước)
    pass
```

### 3.2 Default arguments

Python hỗ trợ default value rất gọn:
```python
def fetch_page(page_num, game="csgo", page_size=80):
    ...

fetch_page(1)                          # game="csgo", page_size=80
fetch_page(1, "dota2")                 # page_size=80
fetch_page(1, page_size=20)            # named arg — Java không có
fetch_page(page_num=1, game="dota2")   # named hết
```

→ Trong code tôi có nhiều function dùng named args để dễ đọc, ví dụ:
```python
fetch_page(page, game, sort_by, cookie, max_retries=3)
```

### 3.3 `*args` và `**kwargs` — variable arguments

```python
def log(*args):              # *args = tuple chứa tất cả positional args
    for a in args:
        print(a)

log("hello", "world", 123)
# args = ("hello", "world", 123)

def configure(**kwargs):     # **kwargs = dict chứa tất cả named args
    print(kwargs)

configure(host="localhost", port=8080)
# kwargs = {"host": "localhost", "port": 8080}
```

Tương đương Java varargs `Object... args` nhưng linh hoạt hơn vì có cả named.

---

## 4. Class — gọn hơn Java rất nhiều

### 4.1 Định nghĩa class

**Java:**
```java
public class Item {
    private String name;
    private double price;

    public Item(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    @Override
    public String toString() {
        return "Item{name='" + name + "', price=" + price + "}";
    }
}
```

**Python:**
```python
class Item:
    def __init__(self, name, price):    # constructor
        self.name = name                 # self = this
        self.price = price
    
    def __repr__(self):                  # toString()
        return f"Item(name={self.name!r}, price={self.price})"

item = Item("AK-47", 100.5)              # KHÔNG có "new"
print(item.name)                         # truy cập trực tiếp, không getter
item.name = "M4"                         # set trực tiếp
```

Đặc điểm khác Java:
- `self` = `this` (bắt buộc là first argument của method)
- Không có `new` keyword
- Không có private fields (convention `_name` cho private)
- Method "đặc biệt" có format `__name__` — gọi là **dunder** (double underscore)

### 4.2 Dunder methods quan trọng

| Dunder | Java tương đương | Khi nào dùng |
|---|---|---|
| `__init__` | constructor | Khởi tạo |
| `__repr__` | `toString()` | Debug |
| `__str__` | `toString()` | User-friendly |
| `__eq__` | `equals()` | So sánh `==` |
| `__hash__` | `hashCode()` | Dùng trong set/dict |
| `__len__` | `.size()` | `len(obj)` |

→ Trong code crawler tôi **không tự define class** vì script đơn giản dùng dict cho data — Pythonic style. Java dev hay nghĩ "phải có class cho mọi thứ" — Python KHÔNG cần.

### 4.3 dataclass — gần giống Java record

Khi cần class chứa data, dùng `@dataclass` thay vì viết tay:

```python
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    price: float
    sell_num: int = 0      # default value

item = Item("AK-47", 100.5)
print(item)               # Item(name='AK-47', price=100.5, sell_num=0)
```

Tương đương Java 14+ record:
```java
public record Item(String name, double price, int sellNum) {}
```

→ Code crawler không dùng dataclass vì xử lý JSON dict trực tiếp tiện hơn.

---

## 5. Control flow — khác biệt nhỏ nhưng nhiều

### 5.1 `if/elif/else`

```python
if price > 1000:
    category = "expensive"
elif price > 100:                # KHÔNG phải else if
    category = "medium"
else:
    category = "cheap"
```

Truthy/falsy — Python **rất khoan dung**:
```python
if items:           # True nếu list không rỗng
    ...
if name:            # True nếu string không rỗng
    ...
if data:            # True nếu dict không rỗng
    ...
if value is not None:    # an toàn hơn `if value:` khi value có thể là 0
    ...
```

→ Trong code tôi có nhiều `if not items:` = "nếu list rỗng".

### 5.2 `for` — luôn là for-each

Python **không có** `for (int i = 0; i < n; i++)`. Chỉ có for-each:

```python
# Iterate list
for item in items:
    print(item)

# Iterate với index
for i, item in enumerate(items):
    print(i, item)

# Range giống for-i Java
for i in range(10):           # 0..9
    print(i)

for i in range(1, 11):        # 1..10
    print(i)

for i in range(0, 100, 5):    # 0, 5, 10, ..., 95
    print(i)

# Iterate dict (đã đề cập ở phần dict)
for key, value in d.items():
    ...
```

### 5.3 `while`

```python
while condition:
    ...
    if should_stop:
        break
    if should_skip:
        continue
```

Trong code monitor có:
```python
while not stop["flag"]:
    ...
```

### 5.4 List comprehension — siêu năng lực Python

Cấu trúc đặc trưng nhất Python, **không có** ở Java (Stream gần giống nhưng verbose hơn):

```python
# Java:
List<Integer> doubled = new ArrayList<>();
for (int x : numbers) {
    if (x > 0) {
        doubled.add(x * 2);
    }
}

# Python:
doubled = [x * 2 for x in numbers if x > 0]
```

Cấu trúc:
```python
[expression for item in iterable if condition]
```

Ví dụ thực tế trong code crawler:
```python
# Lấy tên tất cả item có giá > 100
names = [item["name"] for item in items if item["price"] > 100]

# Tạo dict mới
prices = {item["id"]: item["price"] for item in items}

# Tạo set unique tags
tags = {item["category"] for item in items}
```

Đọc list comp **từ giữa ra**:
1. `for item in items` — iterate
2. `if condition` — filter
3. `expression` — transform

---

## 6. Exception handling — `try/except`

**Java:**
```java
try {
    doSomething();
} catch (IOException e) {
    log.error("IO error", e);
} catch (Exception e) {
    log.error("Other error", e);
} finally {
    cleanup();
}
```

**Python:**
```python
try:
    do_something()
except IOError as e:
    print("IO error:", e)
except Exception as e:
    print("Other error:", e)
finally:
    cleanup()
```

Khác biệt chính:
- `except` thay vì `catch`
- `as e` thay vì `(Exception e)`
- KHÔNG có checked exception — không cần `throws` declaration
- Raise = throw: `raise ValueError("invalid input")`

Trong code crawler:
```python
try:
    r = requests.get(...)
    if r.status_code == 200:
        return r.json()
    raise RuntimeError(f"HTTP {r.status_code}")
except Exception as e:
    if attempt == max_retries - 1:
        raise                        # re-throw
    time.sleep(5 * (attempt + 1))    # retry với backoff
```

---

## 7. Module & import — khác Java rất nhiều

### 7.1 Không có package declaration

Java có `package com.company.module;` ở đầu mỗi file. Python **không có** — file `.py` chính là module, tên module = tên file.

### 7.2 Import

```python
# Import toàn module
import json
data = json.loads('{"a": 1}')          # phải prefix json.

# Import cụ thể
from datetime import datetime, timezone
now = datetime.now(timezone.utc)        # không cần prefix

# Import với alias
import pandas as pd                     # convention chuẩn
df = pd.DataFrame(...)

# Import từ subpackage
from curl_cffi import requests
```

### 7.3 `__name__ == "__main__"`

Block này ở cuối mọi script Python:
```python
if __name__ == "__main__":
    main()
```

Tương đương Java `public static void main(String[] args)` — chỉ chạy khi file được execute trực tiếp (`python file.py`), KHÔNG chạy khi import:

```python
# file: utils.py
def helper():
    return 1

if __name__ == "__main__":
    print("chạy trực tiếp")     # chỉ in khi `python utils.py`
                                  # KHÔNG in khi `import utils`
```

### 7.4 pip — package manager

| Java (Maven) | Python (pip) |
|---|---|
| `pom.xml` | `requirements.txt` |
| `mvn install` | `pip install -r requirements.txt` |
| `<dependency>` block | mỗi dòng 1 lib |

`requirements.txt`:
```
curl_cffi>=0.7.0
requests==2.31.0
```

Cài 1 lib:
```bash
pip install curl_cffi
```

---

## 8. Working with JSON — cốt lõi của crawler

### 8.1 Parse JSON

```python
import json

# String → dict/list
data = json.loads('{"name": "AK", "price": 100}')
print(data["name"])     # AK

# File → dict/list  
with open("data.json") as f:
    data = json.load(f)

# Dict/list → string
text = json.dumps(data, indent=2, ensure_ascii=False)

# Dict/list → file
with open("out.json", "w") as f:
    json.dump(data, f, indent=2)
```

`ensure_ascii=False` quan trọng khi có chữ tiếng Việt/Trung — để giữ nguyên ký tự thay vì escape thành `\u...`.

### 8.2 Map JSON keys giống Java GSON

JSON `{"goods_id": 100, "price": 50.5}` → trong Python access trực tiếp:
```python
item["goods_id"]
item.get("price", 0)        # default 0 nếu không có
```

→ Pythonic = không cần convert sang object class. Java thì hay viết DTO + Jackson/GSON deserialize.

---

## 9. File I/O — `with` statement

`with` = Java try-with-resources. **Luôn dùng `with`** khi mở file:

**Java:**
```java
try (FileWriter w = new FileWriter("out.txt")) {
    w.write("hello");
}
```

**Python:**
```python
with open("out.txt", "w") as f:
    f.write("hello")
# file tự đóng kể cả khi exception
```

Mode chính:
- `"r"` — read (default)
- `"w"` — write (overwrite)
- `"a"` — append
- `"rb"` / `"wb"` — binary

Ví dụ trong code monitor:
```python
def append_jsonl(path, records):
    with open(path, "a", encoding="utf-8") as f:    # append mode
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
```

`pathlib.Path` — modern, tiện hơn `os.path`:
```python
from pathlib import Path

p = Path("./buff_data/state.json")
p.exists()                    # boolean
p.parent                      # Path("./buff_data")
p.parent.mkdir(parents=True, exist_ok=True)  # mkdir -p
p.read_text(encoding="utf-8")
p.write_text("hello", encoding="utf-8")
list(p.parent.glob("*.json")) # tìm file
```

---

## 10. CLI args — `argparse`

Tương đương `args[0], args[1]` của Java nhưng có declarative API:

```python
import argparse

p = argparse.ArgumentParser(description="My tool")
p.add_argument("--pages", type=int, default=5, help="Số page")
p.add_argument("--output", default="out.json")
p.add_argument("--verbose", action="store_true")     # boolean flag
args = p.parse_args()

print(args.pages)        # int
print(args.output)       # str
print(args.verbose)      # bool
```

Chạy:
```bash
python file.py --pages 10 --output result.json --verbose
python file.py --help    # auto-generated help
```

→ Code crawler dùng argparse cho CLI options. Java tương đương phải dùng Picocli hoặc Apache Commons CLI.

---

## 11. Đọc code Buff Crawler — walkthrough

Giờ áp dụng tất cả kiến thức trên để đọc 1 đoạn code thực tế. Lấy từ `buff_crawler.py`:

```python
def fetch_page(
    page_num: int,
    game: str,
    sort_by: str,
    min_price: float | None,
    max_price: float | None,
    cookie: str | None,
    max_retries: int = 3,
) -> dict:
```

**Đọc**:
- `def fetch_page(...)` — định nghĩa function tên `fetch_page`
- `page_num: int` — tham số `page_num` kiểu int (hint, không enforce)
- `min_price: float | None` — kiểu float HOẶC None (tương đương Java `Optional<Double>`)
- `max_retries: int = 3` — default value 3
- `-> dict` — return type là dict

```python
    params: dict[str, object] = {
        "game": game,
        "page_num": page_num,
        "page_size": 80,
        "sort_by": sort_by,
        "_": int(time.time() * 1000),
    }
```

**Đọc**:
- Khởi tạo dict `params` với 5 key-value pairs
- `int(time.time() * 1000)` — convert sang int, lấy timestamp millis
- `time.time()` trả float seconds since epoch

```python
    if min_price is not None:
        params["min_price"] = min_price
```

**Đọc**: Nếu `min_price` không phải None thì add vào dict. (Pythonic check None.)

```python
    last_err: Exception | None = None
    for attempt in range(max_retries):
        try:
            r = requests.get(BASE_URL, params=params, headers=headers,
                             impersonate="chrome120", timeout=20)
            if r.status_code == 200:
                data = r.json()
                if data.get("code") == "OK":
                    return data["data"]
                raise RuntimeError(...)
            ...
        except Exception as e:
            last_err = e
            if attempt == max_retries - 1:
                raise
            time.sleep(5 * (attempt + 1))
```

**Đọc**:
- Loop `max_retries` lần, đếm từ 0 (`range(3)` = [0,1,2])
- `requests.get(..., impersonate="chrome120")` — gọi HTTP với Chrome TLS fingerprint
- `r.json()` — parse response body thành dict (JSON deserialize)
- `data.get("code") == "OK"` — safe access (không KeyError nếu thiếu)
- `data["data"]` — direct access (sẽ KeyError nếu thiếu — đây là OK vì biết chắc có)
- `except Exception as e:` — catch all
- `raise` (không có argument) = re-throw
- `time.sleep(5 * (attempt + 1))` — backoff: 5s, 10s, 15s

→ Pattern này = **HTTP retry with exponential backoff**, equivalent Java code phải viết với `Resilience4j` hoặc tự implement.

---

## 12. Quick reference — Java → Python cheat sheet

| Java | Python |
|---|---|
| `System.out.println(x)` | `print(x)` |
| `String.format("%d", x)` | `f"{x}"` |
| `if (x == null)` | `if x is None:` |
| `if (x != null)` | `if x is not None:` |
| `list.size()` | `len(list)` |
| `list.get(0)` | `list[0]` |
| `list.add(x)` | `list.append(x)` |
| `map.get(k)` | `d[k]` (KeyError) hoặc `d.get(k)` (None) |
| `map.containsKey(k)` | `k in d` |
| `for (T x : list)` | `for x in list:` |
| `for (int i=0; i<n; i++)` | `for i in range(n):` |
| `try/catch/finally` | `try/except/finally` |
| `throw new X()` | `raise X()` |
| `null` | `None` |
| `true / false` | `True / False` |
| `&&  /  \|\|  /  !` | `and / or / not` |
| `instanceof` | `isinstance(x, Type)` |
| `obj.toString()` | `str(obj)` |
| `Integer.parseInt(s)` | `int(s)` |
| `String.valueOf(n)` | `str(n)` |
| `new ArrayList<>()` | `[]` |
| `new HashMap<>()` | `{}` |
| `Arrays.asList(1,2,3)` | `[1, 2, 3]` |
| `Stream.filter().map()` | list comprehension |
| `Optional<T>` | `T \| None` |
| `record` | `@dataclass` |
| `package` | (không có, file = module) |
| `import x.y.Z` | `from x.y import Z` |
| `static` | (function ngoài class) |
| `final` | (không có, convention UPPER_CASE) |

---

## 13. Setup môi trường để bạn chạy code

### 13.1 Cài Python

Mac:
```bash
brew install python@3.12
```

Windows: Tải từ python.org, **NHỚ tick "Add Python to PATH"**.

Verify:
```bash
python3 --version       # phải >= 3.10
pip3 --version
```

### 13.2 Virtual environment (= Java mỗi project có dependency riêng)

Java có Maven/Gradle quản lý dependency per-project. Python: **virtualenv**.

```bash
# Tạo môi trường ảo cho project
cd buff_project
python3 -m venv venv

# Activate (mỗi lần làm việc với project)
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

# Cài dependencies
pip install -r requirements.txt

# Khi xong
deactivate
```

→ **Luôn dùng venv** cho mọi project, không cài global. Tránh conflict version giữa các project.

### 13.3 IDE

PyCharm Community (free) — nếu bạn quen IntelliJ thì native nhất.

VS Code + Python extension — nhẹ hơn, nhiều người dùng.

Cả 2 đều support:
- Type hint check
- Autocomplete
- Debug với breakpoint
- Run config

---

## 14. Roadmap học thêm (nếu cần đào sâu)

Khi đã đọc được code crawler, để **tự viết** thêm tính năng:

1. **Tuần 1**: Đọc kỹ doc này, chạy thử 3 file Python tôi viết, sửa thresholds alert
2. **Tuần 2**: Học `requests` library cơ bản (GET/POST, headers, params)
3. **Tuần 3**: Học `pandas` — xử lý data tabular (như SQL trong Python)
4. **Tuần 4**: Học `asyncio` — concurrent crawl nhiều endpoint cùng lúc
5. **Sau đó**: FastAPI để build REST API (= Spring Boot tương đương trong Python)

Tài liệu khuyến nghị (theo thứ tự):
- **Real Python** (realpython.com) — tutorial thực dụng nhất
- **Python docs official** (docs.python.org) — reference, không phải tutorial
- **Fluent Python (book)** — khi đã viết được Python cơ bản, đọc để lên level

---

## TL;DR — checklist đọc code Python với Java mindset

Khi đọc 1 file Python, để ý:

1. **Indentation** = block — đếm space để biết scope
2. **`def`** = method, **`class`** = class
3. **`self`** = `this`, là first param của method
4. **`__init__`** = constructor
5. **`if __name__ == "__main__"`** = `main()` của file
6. **`with ... as`** = try-with-resources
7. **`for x in y`** = for-each, KHÔNG có for-i
8. **`[x for x in ...]`** = list comprehension = Stream gọn
9. **`dict["key"]`** vs **`dict.get("key")`** — exception vs None
10. **`None`** = `null`, dùng `is None` để check
11. **`raise`** = throw, **`except`** = catch
12. **f-string `f"..."`** = String.format
13. **`*args` `**kwargs`** = varargs (positional & named)
14. **Type hints `: int`** = optional, runtime không enforce
15. **Module = file**, import bằng tên file (không có package)

Đọc code crawler giờ chỉ cần look up cheat sheet ở mục 12 mỗi khi gặp syntax lạ. Sau 2-3 ngày là quen.
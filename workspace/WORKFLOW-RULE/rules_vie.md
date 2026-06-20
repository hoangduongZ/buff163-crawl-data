# AI Markdown Folder Workflow Rule

Bạn là AI coding agent hỗ trợ xử lý task/ticket trong dự án phần mềm.

Nhiệm vụ không chỉ là sửa code, mà còn tổ chức tài liệu Markdown để AI session sau có thể tiếp tục mà không cần hỏi lại từ đầu.

---

## 1. Cấu trúc folder

```txt
docs/<ticket-id>/
├── README.md
├── plan_YYYYMMDD_00.md
├── impl_YYYYMMDD_00.md       (chỉ dùng ở chế độ Standard)
├── problem_YYYYMMDD_00.md    (chỉ tạo khi có lỗi)
├── test_YYYYMMDD_00.md       (chỉ dùng ở chế độ Standard)
└── handover.md
```

---

## 2. Chế độ làm việc

Chọn chế độ trước khi bắt đầu task:

| Chế độ | Khi nào dùng | File cần tạo |
|---|---|---|
| **Lightweight** | Sửa ≤ 2 file, task < 30 phút, fix nhỏ / config / copy | `plan_` → code → `handover` → `README` |
| **Standard** | Tính năng mới, refactor, sửa ≥ 3 file | `plan_` → code → `impl_` → `test_` → `handover` → `README` |

Ở chế độ Lightweight: ghi tóm tắt impl và kết quả test trực tiếp vào `handover.md`.

---

## 3. Ý nghĩa từng file

| File | Mục đích |
|---|---|
| `README.md` | Điều hướng: status + file mới nhất |
| `plan_YYYYMMDD_NN.md` | Yêu cầu + context + phân tích + plan |
| `impl_YYYYMMDD_NN.md` | File đã sửa, nội dung, lý do, logic chính |
| `problem_YYYYMMDD_NN.md` | Lỗi, nguyên nhân, cách xử lý |
| `test_YYYYMMDD_NN.md` | Lệnh chạy, test case, kết quả |
| `handover.md` | Tóm tắt đủ để resume session sau |

---

## 4. Quy tắc đặt tên file

```txt
plan_YYYYMMDD_00.md      (tăng counter nếu tạo lại trong ngày)
impl_YYYYMMDD_00.md
problem_YYYYMMDD_00.md
test_YYYYMMDD_00.md
```

Stable: `README.md`, `handover.md` — không version, ghi đè trực tiếp.

Không dùng: `final.md`, `new.md`, `note.md`, `latest.md`.

---

## 5. Lifecycle

**Lightweight:**
```
1. Tạo folder + plan_YYYYMMDD_00.md
2. Code
3. Cập nhật handover.md (ghi tóm tắt impl + test result)
4. Cập nhật README.md
```

**Standard:**
```
1. Tạo folder + plan_YYYYMMDD_00.md
2. Code
3. Tạo impl_YYYYMMDD_00.md
4. Nếu có lỗi → tạo problem_YYYYMMDD_00.md
5. Tạo test_YYYYMMDD_00.md
6. Cập nhật handover.md
7. Cập nhật README.md
```

---

## 6. Rule bắt buộc trước khi coding

`plan_` phải tồn tại trước khi sửa bất kỳ dòng code nào.

Nội dung bắt buộc — **bullet points, tối đa 5 dòng mỗi section, không viết prose**:

* **Requirement** — cần làm gì
* **Context** — branch, module/API/DB bị ảnh hưởng (chỉ ghi những gì không rõ từ code)
* **Current behavior** — hiện tại đang xảy ra gì
* **Expected behavior** — sau khi fix/feature sẽ như thế nào
* **Implementation steps** — danh sách bước ngắn gọn
* **Test plan** — checklist

Thêm **Risks / Open Questions** chỉ khi thực sự cần.

---

## 7. Rule ghi chép

Quy tắc chung cho **mọi file**:
- Dùng bullet points, không viết đoạn văn dài
- Mỗi section tối đa 5 dòng
- Chỉ ghi những gì không rõ từ đọc code trực tiếp
- Không lặp lại thông tin đã có ở file khác

**`impl_`**: bảng file đã sửa + logic không rõ từ diff.

**`problem_`**: log lỗi → nguyên nhân → cách xử lý → status.

**`test_`**: lệnh chạy + bảng test case (expected / actual / status).

---

## 8. Rule sau khi coding

**`handover.md`** phải đủ để tiếp tục session sau — ghi ngắn gọn:
* Status
* Đã làm gì (bullet)
* File đã sửa (bảng)
* Kết quả test (1 dòng)
* Việc còn lại
* Bước tiếp theo cụ thể

**`README.md`** — chỉ cập nhật 2 thứ: Status + bảng Latest Files.

---

## 9. README.md

```md
# Ticket <ticket-id>

## Status
In Progress / Done / Blocked / Waiting Confirmation

## Summary
<!-- 1 dòng -->

## Latest Files

| Loại | File |
|---|---|
| Plan | `plan_YYYYMMDD_NN.md` |
| Implementation | `impl_YYYYMMDD_NN.md` (nếu có) |
| Problem | `problem_YYYYMMDD_NN.md` (nếu có) |
| Test | `test_YYYYMMDD_NN.md` (nếu có) |
| Handover | `handover.md` |
```

> Không có "Next Action" ở README — đọc `handover.md`.

---

## 10. Nguyên tắc cốt lõi

* `plan_` trước, code sau.
* Bullet points, không prose, tối đa 5 dòng/section.
* Chỉ ghi những gì không rõ từ code.
* Không lặp thông tin giữa các file.
* Không ghi đè file version cũ.
* Mọi file phải đọc được bởi AI session mới không có context trước.

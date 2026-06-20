# AI Markdown Folder Workflow Rule

Bạn là AI coding agent hỗ trợ xử lý task/ticket trong dự án phần mềm.

Nhiệm vụ của bạn không chỉ là sửa code, mà còn phải tổ chức tài liệu Markdown theo một workflow chuẩn để con người hoặc AI agent khác có thể đọc lại, hiểu lại và tiếp tục bảo trì trong tương lai.

---

## 1. Mục tiêu

Với mỗi coding task hoặc ticket, phải tạo một folder riêng để lưu toàn bộ tài liệu liên quan.

Mục tiêu của hệ thống này:

* Lưu lại yêu cầu gốc.
* Lưu lại bản dịch/tóm tắt tiếng Việt nếu cần.
* Lưu lại context kỹ thuật.
* Lưu lại phân tích trước khi code.
* Lưu lại quá trình implement.
* Lưu lại lỗi phát sinh.
* Lưu lại kết quả test/build.
* Lưu lại tổng hợp sau khi hoàn thành.
* Lưu lại handover để người khác hoặc AI agent khác có thể tiếp tục task.

---

## 2. Cấu trúc folder chuẩn

Mỗi ticket phải được lưu tại:

```txt
docs/<ticket-id>/
```

Ví dụ:

```txt
docs/123/
```

Cấu trúc chuẩn:

```txt
docs/<ticket-id>/
├── README.md
├── 00_original/
│   ├── index.md
│   └── index_vi.md
├── 01_context/
│   └── context.md
├── 02_analysis/
│   └── plan-and-analysis_YYYYMMDD_00.md
├── 03_implementation/
│   └── implementation_YYYYMMDD_00.md
├── 04_problem/
│   └── problem_YYYYMMDD_00.md
├── 05_test/
│   └── test-result_YYYYMMDD_00.md
├── 06_resolved/
│   └── resolved_YYYYMMDD_00.md
└── 99_handover/
    └── handover.md
```

---

## 3. Ý nghĩa từng folder

| Folder              | Mục đích                                                      |
| ------------------- | ------------------------------------------------------------- |
| `00_original`       | Lưu ticket/yêu cầu gốc và bản dịch tiếng Việt                 |
| `01_context`        | Lưu context hệ thống, branch, module, API, DB, file liên quan |
| `02_analysis`       | Lưu phân tích yêu cầu và plan trước khi code                  |
| `03_implementation` | Lưu quá trình implement, file đã sửa, lý do sửa               |
| `04_problem`        | Lưu lỗi phát sinh, log lỗi, nguyên nhân, cách xử lý           |
| `05_test`           | Lưu kết quả build/test/verify                                 |
| `06_resolved`       | Lưu tổng hợp sau khi task hoàn thành                          |
| `99_handover`       | Lưu bàn giao cuối cùng cho người/AI đọc tiếp                  |

---

## 4. Quy tắc đặt tên file

Các file ổn định:

```txt
README.md
00_original/index.md
00_original/index_vi.md
01_context/context.md
99_handover/handover.md
```

Các file có version theo ngày và counter:

```txt
02_analysis/plan-and-analysis_YYYYMMDD_COUNTER.md
03_implementation/implementation_YYYYMMDD_COUNTER.md
04_problem/problem_YYYYMMDD_COUNTER.md
05_test/test-result_YYYYMMDD_COUNTER.md
06_resolved/resolved_YYYYMMDD_COUNTER.md
```

Counter bắt đầu từ:

```txt
00, 01, 02, 03...
```

Ví dụ:

```txt
plan-and-analysis_20260529_00.md
plan-and-analysis_20260529_01.md
problem_20260529_00.md
problem_20260529_01.md
test-result_20260529_00.md
```

Quy tắc quan trọng:

* Không ghi đè file version cũ.
* Nếu cùng một loại tài liệu được tạo nhiều lần trong cùng ngày, tăng counter.
* Không dùng tên mơ hồ như `final.md`, `new.md`, `note.md`, `latest.md`, `fix.md`.

---

## 5. Lifecycle bắt buộc

AI agent phải xử lý task theo thứ tự sau:

```txt
1. Tạo folder ticket
2. Lưu yêu cầu gốc vào 00_original/index.md
3. Tạo bản dịch/tóm tắt tiếng Việt tại 00_original/index_vi.md nếu cần
4. Tạo context tại 01_context/context.md
5. Tạo plan phân tích tại 02_analysis/
6. Thực hiện coding
7. Ghi log implement tại 03_implementation/
8. Nếu có lỗi, ghi vào 04_problem/
9. Ghi kết quả test/build tại 05_test/
10. Ghi tổng hợp hoàn thành tại 06_resolved/
11. Cập nhật 99_handover/handover.md
12. Cập nhật README.md
```

---

## 6. Rule bắt buộc trước khi coding

Trước khi sửa code, bắt buộc phải có:

```txt
00_original/index.md
01_context/context.md
02_analysis/plan-and-analysis_YYYYMMDD_00.md
```

Không được bắt đầu coding nếu chưa có phân tích.

File `plan-and-analysis` phải ghi rõ:

* Yêu cầu cần làm là gì.
* Hành vi hiện tại là gì.
* Hành vi mong muốn là gì.
* Phạm vi ảnh hưởng.
* File/module/API/DB có thể bị ảnh hưởng.
* Phương án xử lý.
* Các bước implement.
* Kế hoạch test.
* Rủi ro.
* Câu hỏi cần xác nhận nếu có.

---

## 7. Rule trong quá trình coding

Trong quá trình coding, phải ghi lại vào `03_implementation/`:

* File đã sửa.
* Nội dung sửa.
* Lý do sửa.
* Logic chính đã thay đổi.
* API/DB/UI/config bị ảnh hưởng nếu có.
* Ghi chú kỹ thuật quan trọng.

Nếu có lỗi phát sinh, phải tạo file trong `04_problem/`.

Mỗi problem file phải ghi:

* Lỗi xảy ra khi nào.
* Log lỗi đầy đủ.
* Nguyên nhân nếu tìm được.
* Các bước điều tra.
* Cách xử lý.
* Trạng thái hiện tại.

---

## 8. Rule sau khi coding

Sau khi coding xong, phải tạo hoặc cập nhật:

```txt
05_test/test-result_YYYYMMDD_COUNTER.md
06_resolved/resolved_YYYYMMDD_COUNTER.md
99_handover/handover.md
README.md
```

File `test-result` phải ghi:

* Môi trường test.
* Command build/test đã chạy.
* Test case.
* Expected result.
* Actual result.
* Status.
* Evidence nếu có.

File `resolved` phải ghi:

* Đã hoàn thành những gì.
* File nào đã thay đổi.
* Hành vi cuối cùng sau khi sửa.
* Kết quả test.
* Issue còn lại nếu có.
* Follow-up task nếu có.

File `handover` phải ghi đủ để một developer khác hoặc AI agent khác có thể đọc và tiếp tục task mà không cần hỏi lại từ đầu.

---

## 9. README.md rule

Mỗi ticket folder phải có `README.md`.

`README.md` phải đóng vai trò bản đồ điều hướng.

Nội dung bắt buộc:

```md
# Ticket <ticket-id>

## Status

In Progress / Done / Blocked / Waiting Confirmation

## Summary

Short task summary.

## Reading Order

1. `00_original/index.md`
2. `00_original/index_vi.md`
3. `01_context/context.md`
4. `02_analysis/plan-and-analysis_YYYYMMDD_00.md`
5. `03_implementation/implementation_YYYYMMDD_00.md`
6. `04_problem/problem_YYYYMMDD_00.md`
7. `05_test/test-result_YYYYMMDD_00.md`
8. `06_resolved/resolved_YYYYMMDD_00.md`
9. `99_handover/handover.md`

## Latest Important Files

| Type | File |
|---|---|
| Latest analysis | `02_analysis/...` |
| Latest implementation | `03_implementation/...` |
| Latest problem | `04_problem/...` |
| Latest test result | `05_test/...` |
| Latest resolved | `06_resolved/...` |
| Final handover | `99_handover/handover.md` |

## Current Status

Write current status here.

## Next Action

Write next action here.
```

---

## 10. Final mandatory principles

AI agent must follow these principles:

* Do not only code.
* Analyze before coding.
* Document while coding.
* Record problems when they happen.
* Record test results after testing.
* Summarize after completion.
* Create handover before finishing.
* Do not overwrite old versioned Markdown files.
* Keep all documents specific to the ticket.
* If information is missing, write it into `Open Questions` or `Confirmation Needed`.
* The final folder must be understandable by both humans and future AI agents.

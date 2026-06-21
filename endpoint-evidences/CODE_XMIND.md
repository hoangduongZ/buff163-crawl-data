# Endpoint Verification Tool — XMind

## Tool này làm gì
### Mục đích
#### Gõ cửa máy chủ Buff163 và lưu lại câu trả lời làm bằng chứng
### Kết quả
#### File .evidence.json cho mỗi endpoint
#### Dữ liệu thô từ Buff — không chỉnh sửa

## Các file code
### _common.py
#### Vai trò
##### Bộ công cụ dùng chung cho tất cả script
#### load_cookie()
##### Đọc thông tin đăng nhập từ cookie.txt
##### Không có cookie → một số endpoint bị từ chối
#### call()
##### Gửi yêu cầu HTTP đến Buff163
##### Dùng curl_cffi giả lập Chrome 124
##### Buff không phân biệt được với người dùng thật
#### save_evidence()
##### Ghi kết quả ra file .json
#### print_result()
##### In tóm tắt ra màn hình khi chạy

### ep01_goods.py
#### Hỏi gì
##### Danh sách tất cả skin CS2 đang bán
#### Cần cookie
##### Có
#### Kết quả
##### ✅ OK — 33.876 items
#### Dùng để làm gì
##### Xem toàn bộ thị trường
##### Lọc theo loại skin

### ep02_goods_info.py
#### Hỏi gì
##### Thông tin chi tiết 1 item theo mã số
#### Cần cookie
##### Không
#### Kết quả
##### ✅ OK
#### Dùng để làm gì
##### Tra cứu tên, ảnh, giá Steam
##### Xác minh mã item hợp lệ

### ep03_sell_order.py
#### Hỏi gì
##### Ai đang bán item này — giá bao nhiêu, float thế nào
#### Cần cookie
##### Có + liên kết Steam
#### Kết quả
##### ⚠️ Steam Binding Required
#### Dùng để làm gì
##### Phát hiện hàng rao bán rẻ bất thường
##### Nguồn dữ liệu cốt lõi của sniping tool

### ep04_buy_order.py
#### Hỏi gì
##### Ai đang muốn mua item này — trả giá bao nhiêu
#### Cần cookie
##### Không
#### Kết quả
##### ✅ OK
#### Dùng để làm gì
##### Biết giá người mua sẵn sàng trả
##### Tính khoảng cách giữa giá bán và giá mua

### ep08_price_history.py
#### Hỏi gì
##### Giá của item này trong 30 ngày qua
#### Cần cookie
##### Có + liên kết Steam
#### Kết quả
##### ⚠️ Steam Binding Required
#### Cảnh báo
##### Gọi nhiều lần có thể bị khóa tài khoản

### ep09_bill_order.py
#### Hỏi gì
##### Những giao dịch mua bán gần đây nhất của item này
#### Cần cookie
##### Có + liên kết Steam
#### Kết quả
##### ⚠️ Steam Binding Required
#### Dùng để làm gì
##### Theo dõi giá thực tế đã giao dịch
##### An toàn hơn ep08 để dùng thường xuyên

## Cookie
### Là gì
#### Thẻ đăng nhập Buff163 lấy từ trình duyệt
### Lấy ở đâu
#### Đăng nhập buff.163.com → F12 → Network → copy Cookie header
### Lưu ở đâu
#### File cookie.txt trong thư mục endpoint-evidences
### Gồm những gì
#### session — chứng minh đã đăng nhập
#### csrf_token — mã bảo mật
#### Device-Id — nhận dạng thiết bị

## Blocker hiện tại
### Steam Binding Required
#### ep03, ep08, ep09 đều bị chặn
#### Nguyên nhân
##### Tài khoản Buff chưa liên kết với Steam
#### Cách fix
##### Đăng nhập Buff163
##### Vào Settings → liên kết Steam account

## Kết quả đã có
### ep01 ✅
#### 33.876 skin CS2 confirmed
### ep02 ✅
#### goods_id 44000 = ★ Bayonet Night FN
### ep04 ✅
#### Buy order hoạt động không cần đăng nhập

## goods_id range
### Dota2
#### 1 đến 39.999
### CS2 / CSGO
#### 40.000 trở lên
### Không brute-force
#### Dùng dataset ModestSerhat/cs2-marketplace-ids

# TeachingSchedule

## Giới thiệu
Đây là ứng dụng Streamlit tạo lịch học tự động cho L theo block 14 ngày và chu kỳ chống quên:

Ngày 0 → Ngày 1 → Ngày 3 → Ngày 7 → Kiểm tra chẩn đoán cuối block → Vá đúng phần kiến thức còn yếu

## Triết lý
Không dùng điểm tổng để tự động quyết định pass/fail toàn bộ block hoặc học lại toàn bộ chương.

Điểm số chỉ là tín hiệu mô tả thứ cấp.

Mục tiêu chính của bài kiểm tra cuối block là xác định chính xác từng đơn vị kiến thức L chưa nắm, còn hiểu sai, đã quên hoặc áp dụng sai.

Chỉ xử lý đúng những đơn vị kiến thức cần thiết.

## Tính năng
- Tự động sinh lịch theo block 14 ngày.
- Hiển thị lịch theo tháng.
- Chuyển tháng trước/sau.
- Chọn trực tiếp tháng.
- Chọn trực tiếp năm.
- Nút Hôm nay.
- Xem được lịch tương lai, bao gồm tháng 12/2027 và xa hơn.
- Chạm vào ngày để xem chi tiết.
- Hiển thị tất cả nhiệm vụ nếu một ngày có nhiều sự kiện.
- Hiển thị hướng dẫn chi tiết cho từng loại ngày.
- Hiển thị 4 loại lỗi sau kiểm tra.
- Hiển thị 3 trạng thái sau ngày đen.
- Hiển thị quy tắc kiến thức tiên quyết.
- Hiển thị quy tắc lỗ hổng dai dẳng.
- Hiển thị quy tắc ngày tím.
- Tối ưu cơ bản cho Safari trên iPad.

## Chạy local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Chạy test
```bash
pytest -q
```

## Deploy lên Streamlit Community Cloud
1. Push code lên GitHub.
2. Đăng nhập Streamlit Community Cloud bằng GitHub.
3. Tạo app mới.
4. Chọn repository này.
5. Chọn branch chứa code, thông thường là main.
6. Main file path là app.py.
7. Deploy.

## Hạn chế hiện tại
Phiên bản này chưa có:
- database;
- tài khoản người dùng;
- lưu điểm số;
- lưu từng câu sai;
- lưu trạng thái thực tế của từng đơn vị kiến thức;
- tự động chuyển nợ kiến thức thực tế giữa các block;
- tự động tạo ngày tím vì chưa có ngày bắt đầu chu kỳ cụ thể.

Các quy tắc về lỗi, trạng thái vá và nợ kiến thức hiện được hiển thị để hướng dẫn quá trình học, chưa được lưu trữ như dữ liệu trạng thái.

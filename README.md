# TeachingSchedule

Ứng dụng Streamlit hiển thị lịch học tự động cho L theo chu kỳ chống quên và block 14 ngày.

## Tính năng
- Lịch tháng tương tác
- Chạm vào ngày để xem chi tiết
- Nhiều nhiệm vụ trong cùng ngày
- Chuyển tháng trước/sau
- Chọn trực tiếp tháng và năm
- Nút Hôm nay
- Hiển thị nhiệm vụ hôm nay
- Tự tính block
- Tự động sinh lịch trong tương lai
- Tối ưu cho iPad Safari

## Chạy local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Chạy test
```bash
pytest -q
```

## Deploy Streamlit Community Cloud
1. Đảm bảo code đã được push lên GitHub.
2. Đăng nhập Streamlit Community Cloud bằng GitHub.
3. Chọn repository.
4. Chọn branch main hoặc branch chứa code.
5. Main file path: app.py.
6. Nhấn Deploy.

## Hạn chế hiện tại
- Không có database.
- Không lưu điểm số.
- Không quản lý trạng thái từng đơn vị kiến thức.
- Chưa tự động tạo ngày tím vì chưa xác định ngày bắt đầu chu kỳ.
- Cấu hình lịch hiện nằm trong code.

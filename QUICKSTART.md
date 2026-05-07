# 🚀 HƯỚNG DẪN CHẠY NHANH

## 1️⃣ Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

## 2️⃣ Chạy Ứng Dụng

```bash
streamlit run src/app.py
```

## 3️⃣ Truy Cập Ứng Dụng

Mở trình duyệt và vào: **http://localhost:8501**

---

## ✨ Các Chức Năng Chính

### 🏠 Trang Chủ
- Giới thiệu ứng dụng
- Click **"Load Dữ Liệu Mẫu"** để bắt đầu ngay

### 📁 Upload Dữ Liệu
- Upload file CSV hoặc Excel của bạn
- Hoặc sử dụng dữ liệu mẫu (data/sample_orders.csv hoặc .xlsx)

### 🧹 Làm Sạch Dữ Liệu
- Xóa trùng lặp
- Xử lý giá trị NULL
- Chuẩn hóa dữ liệu

### 📊 Phân Tích Dữ Liệu
- Xem thống kê doanh thu, sản phẩm, khách hàng
- Dùng bộ lọc bên trái để lọc dữ liệu
- Xem biểu đồ chi tiết

### 📈 Dashboard
- Xem tổng quan đầy đủ
- Các tab chuyên sâu (Doanh Thu, Sản Phẩm, Khách Hàng)

### 🔮 Dự Báo
- Dự báo doanh thu hoặc số đơn hàng
- Lựa chọn kỳ dự báo

### 📋 Xuất Báo Cáo
- Xuất các báo cáo khác nhau
- Download CSV

---

## 📂 Cấu Trúc Thư Mục

```
BTL_cd3/
├── src/app.py                 # File chính
├── src/utils/                 # Module utilities
├── src/analysis/              # Module phân tích
├── src/visualization/         # Module biểu đồ
├── data/                      # Dữ liệu
├── requirements.txt           # Dependencies
├── README.md                  # Tài liệu đầy đủ
└── .streamlit/config.toml    # Cấu hình Streamlit
```

---

## 🔧 Yêu Cầu Hệ Thống

- Python 3.8+
- pip (quản lý gói)
- ~500MB đĩa cứng

---

## ⚡ Mẹo Sử Dụng

1. **Lần đầu**: Click "Load Dữ Liệu Mẫu" để thử
2. **Bộ lọc**: Sử dụng sidebar bên trái để lọc dữ liệu realtime
3. **Biểu đồ**: Hover chuột vào biểu đồ xem chi tiết
4. **Export**: Tab "📋 Xuất Báo Cáo" để tải CSV

---

## 🐛 Khắc Phục Sự Cố

### "ModuleNotFoundError"
→ Chạy: `pip install -r requirements.txt`

### Port 8501 đang được sử dụng
→ Chạy: `streamlit run src/app.py --server.port 8502`

### Dữ liệu không tải
→ Kiểm tra file CSV/Excel có hợp lệ không

---

## 📞 Liên Hệ

Nếu có vấn đề, kiểm tra console output để xem lỗi chi tiết.

**Chúc bạn sử dụng vui vẻ!** 🎉


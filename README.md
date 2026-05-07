# 📊 PHÂN TÍCH DỮ LIỆU ĐƠN HÀNG THƯƠNG MẠI ĐIỆN TỬ (E-Commerce Analytics Dashboard)

Ứng dụng phân tích dữ liệu TMĐT hoàn chỉnh được xây dựng bằng **Python** và **Streamlit**.

---

## 🎯 Mục Đích Ứng Dụng

Ứng dụng này cung cấp các công cụ mạnh mẽ để:

✅ **Đọc dữ liệu** - Hỗ trợ file CSV và Excel (.xlsx)

✅ **Làm sạch dữ liệu** - Tự động xóa trùng lặp, xử lý NULL, chuẩn hóa dữ liệu

✅ **Phân tích dữ liệu** - Doanh thu, sản phẩm, khách hàng

✅ **Dashboard trực quan** - Biểu đồ đẹp với Plotly

✅ **Dự báo dữ liệu** - Sử dụng Prophet dự báo doanh thu và số đơn hàng

✅ **Bộ lọc dữ liệu** - Lọc theo ngày, danh mục, khu vực

✅ **Xuất báo cáo** - Xuất dữ liệu ở định dạng CSV

---

## 📋 Yêu Cầu Kỹ Thuật

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Plotly
- Seaborn
- Prophet
- Scikit-learn

---

## 🚀 Cài Đặt và Chạy

### 1. Clone hoặc Download Dự Án

```bash
cd D:\BTL_cd3
```

### 2. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### 3. Chạy Ứng Dụng

```bash
streamlit run src/app.py
```

Ứng dụng sẽ mở tại: **http://localhost:8501**

---

## 📁 Cấu Trúc Dự Án

```
BTL_cd3/
├── src/
│   ├── app.py                      # File chính của Streamlit
│   ├── utils/
│   │   ├── data_loader.py         # Đọc file CSV/Excel
│   │   ├── cleaning.py            # Làm sạch dữ liệu
│   │   ├── forecast.py            # Dự báo bằng Prophet
│   │   └── __init__.py
│   ├── analysis/
│   │   ├── revenue_analysis.py    # Phân tích doanh thu
│   │   ├── product_analysis.py    # Phân tích sản phẩm
│   │   ├── customer_analysis.py   # Phân tích khách hàng
│   │   └── __init__.py
│   ├── visualization/
│   │   ├── charts.py              # Tạo biểu đồ
│   │   ├── dashboard.py           # Dashboard UI
│   │   └── __init__.py
│   └── __init__.py
├── data/
│   ├── sample_orders.csv          # Dữ liệu mẫu CSV
│   └── sample_orders.xlsx         # Dữ liệu mẫu Excel
├── reports/                       # Folder lưu báo cáo
├── charts/                        # Folder lưu biểu đồ
├── requirements.txt               # Dependencies
├── generate_sample_data.py        # Script tạo dữ liệu mẫu
└── README.md                      # File này
```

---

## 📊 Chức Năng Chính

### 1. **Trang Chủ** 🏠
   - Giới thiệu ứng dụng
   - Load dữ liệu mẫu

### 2. **Upload Dữ Liệu** 📁
   - Upload file CSV hoặc Excel
   - Hiển thị thông tin file (số dòng, cột, kiểu dữ liệu)
   - Xem trước dữ liệu
   - Hiển thị giá trị thiếu

### 3. **Làm Sạch Dữ Liệu** 🧹
   - Xóa dữ liệu trùng lặp
   - Xử lý giá trị NULL/NaN
   - Chuẩn hóa ngày tháng
   - Chuyển đổi kiểu dữ liệu
   - Loại bỏ dữ liệu lỗi
   - Báo cáo chi tiết

### 4. **Đánh Giá Chất Lượng Dữ Liệu** 🔍
   - Tính điểm chất lượng (0-100)
   - Phân tích tỷ lệ hoàn chỉnh per cột
   - Phát hiện bản ghi trùng lặp
   - Tìm giá trị ngoại lệ
   - Xem thống kê mô tả
   - Phân tích phân phối giá trị
   - Nhận khuyến nghị cải thiện

### 5. **Phân Tích Dữ Liệu** 📊
   - Phân tích doanh thu (tổng, theo tháng, ngày, khu vực, danh mục)
   - Phân tích sản phẩm (top 10 bán chạy, doanh thu cao)
   - Phân tích khách hàng (tổng, repeat customers, LTV)
   - Bộ lọc động (ngày, danh mục, khu vực)
   - Biểu đồ trực quan

### 6. **Dashboard** 📈
   - Hiển thị KPI chính
   - Tab phân tích (Doanh Thu, Sản Phẩm, Khách Hàng)
   - Biểu đồ interactive
   - Bộ lọc dữ liệu realtime

### 7. **Dự Báo** 🔮
   - Dự báo doanh thu
   - Dự báo số đơn hàng
   - Lựa chọn kỳ dự báo (hàng ngày hoặc hàng tháng)
   - Hiển thị trend, seasonality
   - Khoảng tin cậy 95%

### 8. **Xuất Báo Cáo** 📋
   - Báo cáo tổng quan
   - Báo cáo doanh thu
   - Báo cáo sản phẩm
   - Báo cáo khách hàng
   - Xuất CSV

---

## 📊 Các Biểu Đồ Được Hỗ Trợ

- 📊 **Biểu đồ cột** (Bar Chart)
- 📈 **Biểu đồ đường** (Line Chart)
- 🥧 **Biểu đồ tròn** (Pie Chart)
- 📉 **Biểu đồ diện tích** (Area Chart)
- 🔵 **Biểu đồ scatter** (Scatter Plot)
- 🔥 **Heatmap** (Tương quan dữ liệu)
- 📊 **Histogram** (Phân phối)
- 📦 **Box Plot** (Phân tích phân phối)
- ☀️ **Sunburst Chart** (Cấu trúc phân cấp)

---

## 🎨 Giao Diện

- **Layout**: Wide layout (rộng tối đa)
- **Sidebar**: Menu điều khiển bên trái
- **Responsive**: Tự động thích ứng với kích thước màn hình
- **Dark/Light Mode**: Hỗ trợ cả hai chế độ

---

## 🔧 Dữ Liệu Mẫu

File `data/sample_orders.csv` và `data/sample_orders.xlsx` chứa **1000 bản ghi** đơn hàng với các trường:

| Trường | Kiểu | Mô Tả |
|--------|------|-------|
| Order_ID | String | ID đơn hàng |
| Date | DateTime | Ngày đặt hàng |
| Customer_ID | String | ID khách hàng |
| Product_Category | String | Danh mục sản phẩm |
| Product_Name | String | Tên sản phẩm |
| Quantity | Integer | Số lượng |
| Unit_Price | Float | Giá đơn vị |
| Discount_Percent | Integer | % Chiết khấu |
| Region | String | Khu vực |
| Payment_Method | String | Phương thức thanh toán |
| Shipping_Cost | Float | Chi phí vận chuyển |
| Status | String | Trạng thái đơn hàng |
| Total_Price | Float | Tổng giá (sau chiết khấu) |
| Revenue | Float | Doanh thu (sau vận chuyển) |
| Profit | Float | Lợi nhuận |

---

## 🔍 Cách Sử Dụng Chi Tiết

### Bước 1: Upload Dữ Liệu
1. Chọn menu **"📁 Upload Dữ Liệu"**
2. Click **"Load Dữ Liệu Mẫu"** hoặc upload file của bạn
3. Xem thông tin file

### Bước 2: Làm Sạch Dữ Liệu
1. Chọn menu **"🧹 Làm Sạch Dữ Liệu"**
2. Click **"🚀 Kích Hoạt Làm Sạch Dữ Liệu"**
3. Xem báo cáo chi tiết

### Bước 3: Phân Tích Dữ Liệu
1. Chọn menu **"📊 Phân Tích Dữ Liệu"**
2. Sử dụng bộ lọc bên trái
3. Xem biểu đồ và thống kê

### Bước 4: Xem Dashboard
1. Chọn menu **"📈 Dashboard"**
2. Sử dụng bộ lọc để lọc dữ liệu
3. Xem các biểu đồ chuyên sâu trong các tab

### Bước 5: Dự Báo
1. Chọn menu **"🔮 Dự Báo"**
2. Chọn loại dự báo (Doanh Thu / Số Đơn Hàng)
3. Chọn kỳ dự báo (Hàng ngày / Hàng tháng)
4. Xem kết quả dự báo

### Bước 6: Xuất Báo Cáo
1. Chọn menu **"📋 Xuất Báo Cáo"**
2. Chọn loại báo cáo
3. Click **"📥 Tạo Báo Cáo"**
4. Download CSV nếu cần

---

## 📝 Ví Dụ Dữ Liệu Đầu Vào

### File CSV Format:
```csv
Order_ID,Date,Customer_ID,Product_Category,Product_Name,Quantity,Unit_Price,Discount_Percent,Region,Payment_Method,Shipping_Cost,Status,Total_Price,Revenue,Profit
ORD00000,2023-01-01,CUST0103,Clothing,Phone,5,527.225,0,North,Cash on Delivery,37.405,Pending,2636.127,2598.722,753.433
```

### File Excel Format:
- 1 sheet
- Header ở dòng đầu
- Dữ liệu từ dòng 2

---

## 🐛 Xử Lý Lỗi

- ❌ **File không hợp lệ** → Thông báo lỗi rõ ràng
- ❌ **CSV/Excel bị hỏng** → Phần mềm sẽ báo lỗi
- ❌ **Dữ liệu thiếu cột quan trọng** → Tính toán lại hoặc bỏ qua

---

## 🎓 Công Nghệ Sử Dụng

| Thư Viện | Phiên Bản | Mục Đích |
|---------|---------|-----------|
| **Streamlit** | >=1.18.0 | Framework web |
| **Pandas** | >=1.5.0 | Xử lý dữ liệu |
| **NumPy** | >=1.23.0 | Tính toán số học |
| **Plotly** | >=5.11.0 | Biểu đồ interactive |
| **Matplotlib** | >=3.6.0 | Vẽ biểu đồ |
| **Seaborn** | >=0.12.0 | Trực quan hóa thống kê |
| **Prophet** | >=1.1.2 | Dự báo thời gian |
| **Scikit-learn** | >=1.2.0 | Machine learning |
| **OpenPyXL** | >=3.0.0 | Xử lý Excel |

---

## ⚙️ Cấu Hình Streamlit

Tệp `.streamlit/config.toml` (tùy chọn):
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[client]
toolbarMode = "minimal"

[logger]
level = "error"
```

---

## 🔔 Ghi Chú Quan Trọng

1. **Dữ liệu mẫu**: Được tạo tự động nếu chưa tồn tại
2. **Cải thiện hiệu suất**: Sử dụng caching của Streamlit
3. **Tương thích**: Hoạt động trên Windows, macOS, Linux
4. **Bảo mật**: Không lưu dữ liệu người dùng

---

## 📞 Hỗ Trợ và Cải Thiện

- Kiểm tra các lỗi trong console
- Đảm bảo Python phiên bản 3.8+
- Cập nhật pip: `pip install --upgrade pip`

---

## 📄 Giấy Phép

Dự án này được tạo cho mục đích giáo dục.

---

## 🎉 Tính Năng Nổi Bật

✨ **Trao đổi dữ liệu thực tế** - Không giả lập  
✨ **Giao diện hiện đại** - Streamlit + Plotly  
✨ **Bộ lọc mạnh mẽ** - Lọc realtime  
✨ **Dự báo thông minh** - Sử dụng Prophet  
✨ **Export dữ liệu** - Xuất CSV ngay  
✨ **Code sạch** - Chia module hợp lý  

---

**Chúc bạn sử dụng ứng dụng vui vẻ! 🚀**


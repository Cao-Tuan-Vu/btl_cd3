import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Tạo dữ liệu mẫu cho các đơn hàng
np.random.seed(42)

# Tháng bắt đầu và số lượng bản ghi
start_date = datetime(2023, 1, 1)
num_records = 1000

# Tạo danh sách ngày
dates = [start_date + timedelta(days=x) for x in range(365)]
dates = dates * (num_records // len(dates) + 1)
dates = dates[:num_records]

# Tạo dữ liệu
data = {
    'Order_ID': [f'ORD{i:05d}' for i in range(num_records)],
    'Date': dates,
    'Customer_ID': [f'CUST{np.random.randint(1, 500):04d}' for _ in range(num_records)],
    'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Home & Kitchen', 'Sports', 'Beauty'], num_records),
    'Product_Name': np.random.choice(['Laptop', 'Phone', 'T-Shirt', 'Dresses', 'Jeans', 'Mattress', 'Pillow', 'Sofa', 'Running Shoes', 'Skincare'], num_records),
    'Quantity': np.random.randint(1, 6, num_records),
    'Unit_Price': np.random.uniform(10, 1000, num_records),
    'Discount_Percent': np.random.choice([0, 5, 10, 15, 20], num_records),
    'Region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], num_records),
    'Payment_Method': np.random.choice(['Credit Card', 'Debit Card', 'E-Wallet', 'Bank Transfer', 'Cash on Delivery'], num_records),
    'Sales_Channel': np.random.choice(['Website', 'Mobile App', 'Social Commerce', 'Marketplace'], num_records),
    'Shipping_Cost': np.random.uniform(5, 50, num_records),
    'Status': np.random.choice(['Completed', 'Pending', 'Cancelled', 'Shipped'], num_records),
}

# Tính toán các cột doanh thu
df = pd.DataFrame(data)
df['Total_Price'] = df['Quantity'] * df['Unit_Price'] * (1 - df['Discount_Percent'] / 100)
df['Revenue'] = df['Total_Price'] - df['Shipping_Cost']
df['Profit'] = df['Total_Price'] * 0.3 - df['Shipping_Cost']  # Giả định lợi nhuận 30%

# Lưu vào file CSV
df.to_csv('data/sample_orders.csv', index=False)
# Lưu vào file Excel
df.to_excel('data/sample_orders.xlsx', index=False)

print("✓ Đã tạo file dữ liệu mẫu:")
print(f"  - data/sample_orders.csv ({len(df)} dòng)")
print(f"  - data/sample_orders.xlsx ({len(df)} dòng)")
print("\nCác cột của dữ liệu:")
print(df.info())
print("\nDữ liệu mẫu:")
print(df.head())


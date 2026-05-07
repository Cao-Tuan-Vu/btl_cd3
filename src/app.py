"""
Ứng Dụng Phân Tích Dữ Liệu Đơn Hàng Thương Mại Điện Tử (E-Commerce)
===================================================================

Ứng dụng này dùng để:
- Đọc dữ liệu từ file CSV/Excel
- Làm sạch dữ liệu tự động
- Phân tích doanh thu, sản phẩm, khách hàng
- Trực quan hóa dữ liệu với dashboard
- Dự báo doanh thu và số đơn hàng
"""

import streamlit as st
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Import các module tự viết
import sys
sys.path.insert(0, 'src')

from utils.data_loader import DataLoader
from utils.cleaning import DataCleaner
from utils.forecast import DataForecaster

from analysis.revenue_analysis import RevenueAnalysis
from analysis.product_analysis import ProductAnalysis
from analysis.customer_analysis import CustomerAnalysis

from visualization.charts import ChartGenerator
from visualization.dashboard import Dashboard


# ==================== CẤU HÌNH STREAMLIT ====================
st.set_page_config(
    page_title="📊 E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS tùy chỉnh
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
        margin-bottom: 30px;
    }
    h2 {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== KHỞI TẠO SESSION STATE ====================
if 'df' not in st.session_state:
    st.session_state.df = None
if 'df_cleaned' not in st.session_state:
    st.session_state.df_cleaned = None
if 'cleaning_report' not in st.session_state:
    st.session_state.cleaning_report = None


# ==================== HÀM CHÍNH ====================
def main():
    """Hàm chính của ứng dụng"""

    # Tiêu đề chính
    st.markdown("""
        <h1>📊 PHÂN TÍCH DỮ LIỆU ĐƠN HÀNG THƯƠNG MẠI ĐIỆN TỬ</h1>
    """, unsafe_allow_html=True)

    # Hộp điều khiển bên trái (Sidebar)
    st.sidebar.markdown("## ⚙️ MENU")

    menu_options = [
        "🏠 Trang Chủ",
        "📁 Upload Dữ Liệu",
        "🧹 Làm Sạch Dữ Liệu",
        "📊 Phân Tích Dữ Liệu",
        "📈 Dashboard",
        "🔮 Dự Báo",
        "📋 Xuất Báo Cáo"
    ]

    selected_menu = st.sidebar.selectbox("Chọn chức năng", menu_options)

    # ========== TRANG CHỦ ==========
    if selected_menu == "🏠 Trang Chủ":
        display_home_page()

    # ========== UPLOAD DỮ LIỆU ==========
    elif selected_menu == "📁 Upload Dữ Liệu":
        display_upload_page()

    # ========== LÀM SẠCH DỮ LIỆU ==========
    elif selected_menu == "🧹 Làm Sạch Dữ Liệu":
        if st.session_state.df is None:
            st.warning("⚠️ Vui lòng upload dữ liệu trước")
        else:
            display_cleaning_page()

    # ========== PHÂN TÍCH DỮ LIỆU ==========
    elif selected_menu == "📊 Phân Tích Dữ Liệu":
        if st.session_state.df_cleaned is None:
            st.warning("⚠️ Vui lòng làm sạch dữ liệu trước")
        else:
            display_analysis_page()

    # ========== DASHBOARD ==========
    elif selected_menu == "📈 Dashboard":
        if st.session_state.df_cleaned is None:
            st.warning("⚠️ Vui lòng làm sạch dữ liệu trước")
        else:
            display_dashboard_page()

    # ========== DỰ BÁO ==========
    elif selected_menu == "🔮 Dự Báo":
        if st.session_state.df_cleaned is None:
            st.warning("⚠️ Vui lòng làm sạch dữ liệu trước")
        else:
            display_forecast_page()

    # ========== XUẤT BÁO CÁO ==========
    elif selected_menu == "📋 Xuất Báo Cáo":
        if st.session_state.df_cleaned is None:
            st.warning("⚠️ Vui lòng làm sạch dữ liệu trước")
        else:
            display_report_page()


# ==================== CÁC TRANG CHỨC NĂNG ====================

def display_home_page():
    """Trang chủ"""
    st.markdown("""
    ## 🎯 Chào Mừng Đến Với Ứng Dụng Phân Tích Dữ Liệu TMĐT
    
    Ứng dụng này cung cấp các công cụ mạnh mẽ để:
    
    ✅ **Đọc dữ liệu** - Hỗ trợ CSV và Excel
    
    ✅ **Làm sạch dữ liệu** - Xóa trùng lặp, xử lý NULL, chuẩn hóa dữ liệu
    
    ✅ **Phân tích dữ liệu** - Doanh thu, sản phẩm, khách hàng
    
    ✅ **Dashboard trực quan** - Biểu đồ đẹp, dễ hiểu
    
    ✅ **Dự báo** - Sử dụng Prophet dự báo doanh thu
    
    ✅ **Bộ lọc dữ liệu** - Lọc theo ngày, danh mục, khu vực, v.v.
    
    ---
    
    ### 🚀 Cách Sử Dụng:
    
    1. **Bước 1**: Upload file CSV hoặc Excel từ menu "Upload Dữ Liệu"
    2. **Bước 2**: Làm sạch dữ liệu tại "Làm Sạch Dữ Liệu"
    3. **Bước 3**: Xem phân tích chi tiết tại "Phân Tích Dữ Liệu"
    4. **Bước 4**: Xem Dashboard trực quan
    5. **Bước 5**: Dự báo doanh thu cho tương lai
    
    ---
    
    ### 📊 Thông Tin Ứng Dụng:
    
    - **Giao diện**: Streamlit
    - **Thư viện**: Pandas, NumPy, Plotly, Prophet
    - **Hỗ trợ định dạng**: CSV, Excel (.xlsx)
    - **Ngôn ngữ**: Python
    """)

    # Hiển thị dữ liệu mẫu
    st.markdown("---")
    st.markdown("### 📌 Dữ Liệu Mẫu")

    if st.button("📥 Load Dữ Liệu Mẫu"):
        try:
            df_sample = pd.read_csv('data/sample_orders.csv')
            st.session_state.df = df_sample
            st.success("✅ Đã load dữ liệu mẫu thành công!")
            st.info(f"Dữ liệu có {len(df_sample)} dòng và {len(df_sample.columns)} cột")
        except Exception as e:
            st.error(f"❌ Lỗi load dữ liệu mẫu: {str(e)}")


def display_upload_page():
    """Trang upload dữ liệu"""
    st.markdown("## 📁 Upload Dữ Liệu")

    st.markdown("""
    Upload file dữ liệu của bạn dưới định dạng CSV hoặc Excel (.xlsx)
    """)

    uploaded_file = st.file_uploader(
        "Chọn file CSV hoặc Excel",
        type=['csv', 'xlsx']
    )

    if uploaded_file:
        # Đọc file
        loader = DataLoader()
        df = loader.load_file(uploaded_file)

        if df is not None:
            st.session_state.df = df
            st.success("✅ Upload thành công!")

            # Hiển thị thông tin file
            file_info = loader.get_file_info(df)

            st.markdown("### 📋 Thông Tin File")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"📌 Số dòng: {file_info['rows']}")
            with col2:
                st.info(f"📌 Số cột: {file_info['columns']}")
            with col3:
                st.info(f"📌 Dung lượng: {file_info['memory_usage']:.2f} MB")

            # Hiển thị xem trước dữ liệu
            dashboard = Dashboard(df)
            dashboard.display_data_preview(df)

            # Hiển thị kiểu dữ liệu
            dashboard.display_data_types(df)

            # Hiển thị dữ liệu thiếu
            st.markdown("### ⚠️ Giá Trị Thiếu")
            missing_info = pd.DataFrame({
                'Cột': file_info['missing_values'].keys(),
                'Giá Trị Thiếu': file_info['missing_values'].values()
            })
            st.dataframe(missing_info, use_container_width=True)


def display_cleaning_page():
    """Trang làm sạch dữ liệu"""
    st.markdown("## 🧹 Làm Sạch Dữ Liệu")

    st.markdown("""
    Module này sẽ tự động:
    - ✅ Xóa dữ liệu trùng lặp
    - ✅ Xử lý giá trị NULL
    - ✅ Chuẩn hóa dữ liệu ngày tháng
    - ✅ Chuyển đổi kiểu dữ liệu
    - ✅ Loại bỏ dữ liệu lỗi
    """)

    if st.button("🚀 Kích Hoạt Làm Sạch Dữ Liệu", key="clean_btn"):
        with st.spinner("⏳ Đang xử lý..."):
            cleaner = DataCleaner(st.session_state.df)
            df_cleaned = cleaner.clean()
            st.session_state.df_cleaned = df_cleaned
            st.session_state.cleaning_report = cleaner.get_report()

        st.success("✅ Làm sạch dữ liệu thành công!")

    if st.session_state.cleaning_report:
        st.markdown("### 📊 Báo Cáo Làm Sạch")

        report = st.session_state.cleaning_report

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📌 Dòng Gốc",
                f"{report['original_rows']:,}"
            )

        with col2:
            st.metric(
                "📌 Dòng Sau Xử Lý",
                f"{report['final_rows']:,}"
            )

        with col3:
            st.metric(
                "📌 Dòng Bị Xóa",
                f"{report['total_rows_removed']:,}"
            )

        with col4:
            if report['original_rows'] > 0:
                pct_removed = (report['total_rows_removed'] / report['original_rows']) * 100
                st.metric("📌 % Bị Xóa", f"{pct_removed:.2f}%")

        # Hiển thị chi tiết
        st.markdown("### 📋 Chi Tiết Xử Lý")

        details = pd.DataFrame({
            'Loại Xử Lý': [
                'Dòng Trùng Lặp',
                'Giá Trị NULL',
                'Dữ Liệu Lỗi'
            ],
            'Số Lượng': [
                report.get('duplicates_removed', 0),
                report.get('null_values_filled', 0),
                report.get('invalid_rows_removed', 0)
            ]
        })

        st.dataframe(details, use_container_width=True)

        # Xem trước dữ liệu sau khi làm sạch
        st.markdown("### 👀 Xem Trước Dữ Liệu Sau Sạch")
        st.dataframe(st.session_state.df_cleaned.head(10), use_container_width=True)


def display_analysis_page():
    """Trang phân tích dữ liệu"""
    st.markdown("## 📊 Phân Tích Dữ Liệu")

    df = st.session_state.df_cleaned

    # Tạo bộ lọc
    st.markdown("### 🔍 Bộ Lọc Dữ Liệu")

    dashboard = Dashboard(df)
    filtered_df = dashboard.apply_all_filters()

    st.info(f"📌 Dữ liệu hiển thị: {len(filtered_df)} dòng (từ {len(df)} dòng gốc)")

    # Phân tích doanh thu
    st.markdown("---")
    st.markdown("### 💰 Phân Tích Doanh Thu")

    revenue_analysis = RevenueAnalysis(filtered_df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💵 Tổng Doanh Thu", f"${revenue_analysis.total_revenue():,.2f}")

    with col2:
        st.metric("📦 Tổng Đơn Hàng", f"{revenue_analysis.total_orders():,}")

    with col3:
        st.metric("📈 Tổng Sản Phẩm", f"{revenue_analysis.total_products_sold():,}")

    with col4:
        st.metric("💳 Giá Trị TB/Đơn", f"${revenue_analysis.average_order_value():,.2f}")

    # Biểu đồ doanh thu theo tháng
    col1, col2 = st.columns(2)

    with col1:
        revenue_by_month = revenue_analysis.revenue_by_month()
        if not revenue_by_month.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.line_chart(
                revenue_by_month,
                'Month', 'Revenue',
                '📊 Doanh Thu Theo Tháng'
            )
            st.plotly_chart(fig, use_container_width=True)

    # Doanh thu theo ngày
    revenue_by_day = revenue_analysis.revenue_by_day()
    if not revenue_by_day.empty:
        chart_gen = ChartGenerator()
        fig = chart_gen.line_chart(
            revenue_by_day,
            'Date', 'Revenue',
            '📅 Doanh Thu Theo Ngày'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Lợi nhuận, thanh toán và kênh bán hàng
    st.markdown("---")
    st.markdown("### 💹 Phân Tích Lợi Nhuận & Kênh Bán Hàng")

    profit_stats = revenue_analysis.profit_summary()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📈 Tổng Lợi Nhuận", f"${profit_stats['total_profit']:,.2f}")
    with col2:
        st.metric("📊 Biên Lợi Nhuận", f"{profit_stats['margin_pct']:.2f}%")

    col1, col2 = st.columns(2)
    with col1:
        payment_method = revenue_analysis.revenue_by_payment_method()
        if not payment_method.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.pie_chart(
                payment_method,
                'Revenue', 'Payment Method',
                '💳 Cơ Cấu Doanh Thu Theo Thanh Toán'
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        channel_data = revenue_analysis.revenue_by_sales_channel()
        if not channel_data.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(
                channel_data,
                'Sales Channel', 'Revenue',
                '🛒 Doanh Thu Theo Kênh Bán Hàng'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Không tìm thấy cột kênh bán hàng (ví dụ: Sales_Channel/Channel).")

    with col2:
        revenue_by_region = revenue_analysis.revenue_by_region()
        if not revenue_by_region.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(
                revenue_by_region,
                'Region', 'Revenue',
                '📊 Doanh Thu Theo Khu Vực'
            )
            st.plotly_chart(fig, use_container_width=True)

    # Phân tích sản phẩm
    st.markdown("---")
    st.markdown("### 📦 Phân Tích Sản Phẩm")

    product_analysis = ProductAnalysis(filtered_df)

    col1, col2 = st.columns(2)

    with col1:
        top_products_sales = product_analysis.top_products_by_sales(10)
        if not top_products_sales.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(
                top_products_sales,
                'Product', 'Total_Quantity',
                '🏆 Top 10 Sản Phẩm Bán Chạy'
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        top_products_revenue = product_analysis.top_products_by_revenue(10)
        if not top_products_revenue.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(
                top_products_revenue,
                'Product', 'Revenue',
                '💰 Top 10 Sản Phẩm Doanh Thu'
            )
            st.plotly_chart(fig, use_container_width=True)

    # Phân tích khách hàng
    st.markdown("---")
    st.markdown("### 👥 Phân Tích Khách Hàng")

    customer_analysis = CustomerAnalysis(filtered_df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("👥 Tổng Khách Hàng", f"{customer_analysis.total_customers():,}")

    with col2:
        st.metric("🔄 Khách Mua Lại", f"{customer_analysis.repeat_customers():,}")

    with col3:
        st.metric("💵 LTV Trung Bình", f"${customer_analysis.customer_lifetime_value():,.2f}")

    with col4:
        st.metric("📊 Đơn/Khách TB", f"{customer_analysis.orders_per_customer():.2f}")

    # Top khách hàng
    col1, col2 = st.columns(2)

    with col1:
        top_customers = customer_analysis.top_customers_by_spending(10)
        if not top_customers.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(
                top_customers,
                'Customer', 'Total_Spending',
                '💰 Top 10 Khách Hàng Chi Tiêu'
            )
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        customers_per_region = customer_analysis.customer_per_region()
        if not customers_per_region.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.pie_chart(
                customers_per_region,
                'Customer_Count', 'Region',
                '🗺️ Khách Hàng Theo Khu Vực'
            )
            st.plotly_chart(fig, use_container_width=True)


def display_dashboard_page():
    """Trang dashboard"""
    st.markdown("## 📈 DASHBOARD TRỰC QUAN")

    df = st.session_state.df_cleaned

    # Tạo bộ lọc
    dashboard = Dashboard(df)

    st.markdown("### 🔍 Bộ Lọc Dữ Liệu")
    filtered_df = dashboard.apply_all_filters()

    st.info(f"📌 Dữ liệu hiển thị: {len(filtered_df)} dòng (từ {len(df)} dòng gốc)")

    # Hiển thị KPI
    st.markdown("---")
    st.markdown("### 📊 KPI CHÍNH")

    dashboard.display_summary_stats(filtered_df)

    # Tab để phân chia nội dung
    tab1, tab2, tab3 = st.tabs(["💰 Doanh Thu", "📦 Sản Phẩm", "👥 Khách Hàng"])

    # Tab 1: Doanh Thu
    with tab1:
        revenue_analysis = RevenueAnalysis(filtered_df)
        chart_gen = ChartGenerator()

        col1, col2 = st.columns(2)

        with col1:
            revenue_by_month = revenue_analysis.revenue_by_month()
            if not revenue_by_month.empty:
                fig = chart_gen.area_chart(
                    revenue_by_month,
                    'Month', 'Revenue',
                    '📊 Doanh Thu Theo Tháng'
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            revenue_by_category = revenue_analysis.revenue_by_category()
            if not revenue_by_category.empty:
                fig = chart_gen.pie_chart(
                    revenue_by_category,
                    'Revenue', 'Category',
                    '📊 Doanh Thu Theo Danh Mục'
                )
                st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            revenue_by_region = revenue_analysis.revenue_by_region()
            if not revenue_by_region.empty:
                fig = chart_gen.bar_chart(
                    revenue_by_region,
                    'Region', 'Revenue',
                    '📊 Doanh Thu Theo Khu Vực'
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            payment_method = revenue_analysis.revenue_by_payment_method()
            if not payment_method.empty:
                fig = chart_gen.bar_chart(
                    payment_method,
                    'Payment Method', 'Revenue',
                    '📊 Doanh Thu Theo Phương Thức Thanh Toán'
                )
                st.plotly_chart(fig, use_container_width=True)

        channel_data = revenue_analysis.revenue_by_sales_channel()
        if not channel_data.empty:
            fig = chart_gen.pie_chart(
                channel_data,
                'Revenue', 'Sales Channel',
                '🛒 Doanh Thu Theo Kênh Bán Hàng'
            )
            st.plotly_chart(fig, use_container_width=True)

    # Tab 2: Sản Phẩm
    with tab2:
        product_analysis = ProductAnalysis(filtered_df)
        chart_gen = ChartGenerator()

        col1, col2 = st.columns(2)

        with col1:
            top_products = product_analysis.top_products_by_sales(10)
            if not top_products.empty:
                fig = chart_gen.bar_chart(
                    top_products,
                    'Product', 'Total_Quantity',
                    '🏆 Top 10 Sản Phẩm Bán Chạy'
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            products_by_cat = product_analysis.products_by_category()
            if not products_by_cat.empty:
                fig = chart_gen.pie_chart(
                    products_by_cat,
                    'Total_Quantity', 'Category',
                    '📊 Sản Phẩm Theo Danh Mục'
                )
                st.plotly_chart(fig, use_container_width=True)

    # Tab 3: Khách Hàng
    with tab3:
        customer_analysis = CustomerAnalysis(filtered_df)
        chart_gen = ChartGenerator()

        col1, col2 = st.columns(2)

        with col1:
            top_customers = customer_analysis.top_customers_by_spending(10)
            if not top_customers.empty:
                fig = chart_gen.bar_chart(
                    top_customers,
                    'Customer', 'Total_Spending',
                    '💰 Top 10 Khách Hàng'
                )
                st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔥 Heatmap Tương Quan")
    numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) >= 2:
        chart_gen = ChartGenerator()
        fig = chart_gen.heatmap_chart(filtered_df[numeric_cols], "Tương Quan Các Biến Số")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Cần ít nhất 2 cột số để hiển thị heatmap.")

        with col2:
            customers_per_region = customer_analysis.customer_per_region()
            if not customers_per_region.empty:
                fig = chart_gen.bar_chart(
                    customers_per_region,
                    'Region', 'Customer_Count',
                    '🗺️ Khách Hàng Theo Khu Vực'
                )
                st.plotly_chart(fig, use_container_width=True)


def display_forecast_page():
    """Trang dự báo"""
    st.markdown("## 🔮 DỰ BÁO DỮ LIỆU")

    df = st.session_state.df_cleaned

    # Chọn loại dự báo
    forecast_type = st.selectbox(
        "Chọn loại dự báo",
        ["Doanh Thu", "Số Đơn Hàng"]
    )

    # Chọn kỳ dự báo
    forecast_period = st.selectbox(
        "Chọn kỳ dự báo",
        ["Hàng Ngày (30 ngày tới)", "Hàng Tháng (12 tháng tới)"]
    )

    if st.button("🚀 Thực Hiện Dự Báo"):
        with st.spinner("⏳ Đang tính toán..."):
            try:
                # Xác định cột để dự báo
                date_col = [col for col in df.columns if 'date' in col.lower()]
                if not date_col:
                    st.error("❌ Không tìm thấy cột ngày tháng")
                    return

                date_col = date_col[0]

                if forecast_type == "Doanh Thu":
                    value_col = [col for col in df.columns if 'revenue' in col.lower()]
                    if not value_col:
                        st.error("❌ Không tìm thấy cột doanh thu")
                        return
                    value_col = value_col[0]
                    title_prefix = "Doanh Thu"
                else:
                    value_col = [col for col in df.columns if 'quantity' in col.lower()]
                    if not value_col:
                        st.error("❌ Không tìm thấy cột số lượng")
                        return
                    value_col = value_col[0]
                    title_prefix = "Số Đơn Hàng"

                # Tạo và huấn luyện mô hình
                forecast_model = DataForecaster(df, date_col, value_col)
                prepared = forecast_model.prepare_data()

                if forecast_period == "Hàng Ngày (30 ngày tới)":
                    forecast_df = forecast_model.forecast_days(30)
                    title = f"🔮 Dự Báo {title_prefix} - 30 Ngày Tới"
                else:
                    forecast_df = forecast_model.forecast_months(12)
                    title = f"🔮 Dự Báo {title_prefix} - 12 Tháng Tới"

                forecast_future = forecast_df[forecast_df['ds'] > prepared['ds'].max()].copy()
                if forecast_future.empty:
                    forecast_future = forecast_df.copy()

                # Hiển thị biểu đồ dự báo
                import plotly.graph_objects as go

                fig = go.Figure()

                # Dữ liệu gốc
                fig.add_trace(go.Scatter(
                    x=prepared['ds'],
                    y=prepared['y'],
                    name='Dữ Liệu Gốc',
                    mode='lines',
                    line=dict(color='blue')
                ))

                # Dự báo
                fig.add_trace(go.Scatter(
                    x=forecast_future['ds'],
                    y=forecast_future['yhat'],
                    name='Dự Báo',
                    mode='lines',
                    line=dict(color='red')
                ))

                # Vùng tin cậy
                fig.add_trace(go.Scatter(
                    x=forecast_future['ds'].tolist() + forecast_future['ds'].tolist()[::-1],
                    y=forecast_future['yhat_upper'].tolist() + forecast_future['yhat_lower'].tolist()[::-1],
                    fill='toself',
                    fillcolor='rgba(255, 0, 0, 0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='Khoảng tin cậy 95%'
                ))

                fig.update_layout(
                    title=title,
                    xaxis_title='Thời Gian',
                    yaxis_title='Giá Trị',
                    height=600,
                    hovermode='x unified',
                    template='plotly_white'
                )

                st.plotly_chart(fig, use_container_width=True)

                components_fig = forecast_model.get_components()
                if components_fig is not None:
                    st.markdown("### 📉 Trend & Seasonality")
                    st.plotly_chart(components_fig, use_container_width=True)

                # Hiển thị bảng dự báo
                st.markdown("### 📋 Bảng Đặc Biệt")
                forecast_display = forecast_future[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
                forecast_display.columns = ['Ngày', 'Dự Báo', 'Giới Hạn Dưới', 'Giới Hạn Trên']
                st.dataframe(forecast_display, use_container_width=True)

                # Hiển thị metrics
                metrics = forecast_model.get_metrics()
                st.markdown("### 📊 Chỉ Số Hiệu Quả")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("MAPE (%)", f"{metrics.get('mape', 0):.2f}%")
                with col2:
                    st.metric("Số Điểm Dữ Liệu", f"{metrics.get('data_points', 0)}")

            except Exception as e:
                st.error(f"❌ Lỗi dự báo: {str(e)}")


def display_report_page():
    """Trang xuất báo cáo"""
    st.markdown("## 📋 XUẤT BÁO CÁO")

    df = st.session_state.df_cleaned

    st.markdown("""
    Chọn loại báo cáo muốn xuất:
    """)

    report_type = st.multiselect(
        "Chọn báo cáo",
        [
            "📊 Báo Cáo Tổng Quan",
            "💰 Báo Cáo Doanh Thu",
            "📦 Báo Cáo Sản Phẩm",
            "👥 Báo Cáo Khách Hàng",
            "📁 Xuất Dữ Liệu (CSV)"
        ],
        default=["📊 Báo Cáo Tổng Quan"]
    )

    if st.button("📥 Tạo Báo Cáo"):
        if "📊 Báo Cáo Tổng Quan" in report_type:
            st.markdown("### 📊 Báo Cáo Tổng Quan")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"📌 Tổng Dòng: {len(df):,}")
            with col2:
                st.info(f"📌 Tổng Cột: {len(df.columns)}")
            with col3:
                st.info(f"📌 Khoảng Thời Gian: Từ ... đến ...")

        if "💰 Báo Cáo Doanh Thu" in report_type:
            st.markdown("### 💰 Báo Cáo Doanh Thu")
            revenue_analysis = RevenueAnalysis(df)
            st.info(f"Tổng Doanh Thu: ${revenue_analysis.total_revenue():,.2f}")

        if "📦 Báo Cáo Sản Phẩm" in report_type:
            st.markdown("### 📦 Báo Cáo Sản Phẩm")
            product_analysis = ProductAnalysis(df)
            st.info(f"Tổng Sản Phẩm: {product_analysis.product_count()}")

        if "👥 Báo Cáo Khách Hàng" in report_type:
            st.markdown("### 👥 Báo Cáo Khách Hàng")
            customer_analysis = CustomerAnalysis(df)
            st.info(f"Tổng Khách Hàng: {customer_analysis.total_customers()}")

        if "📁 Xuất Dữ Liệu (CSV)" in report_type:
            st.markdown("### 📁 Xuất Dữ Liệu")

            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Tải Xuống CSV",
                data=csv,
                file_name="ecommerce_data.csv",
                mime="text/csv"
            )

    st.markdown("---")
    st.markdown("### 💡 Ghi Chú")
    st.info("""
    - Báo cáo có thể được tạo nhiều lần
    - Có thể xuất dữ liệu ở định dạng CSV
    - Báo cáo chứa dữ liệu đã được làm sạch
    """)


# ==================== CHẠY ỨNG DỤNG ====================
if __name__ == "__main__":
    main()


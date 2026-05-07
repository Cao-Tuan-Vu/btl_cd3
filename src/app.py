import streamlit as st
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Import các module tự viết
import sys
sys.path.insert(0, 'src')

from utils.data_loader import DataLoader
from utils.cleaning import DataCleaner
from analysis.revenue_analysis import RevenueAnalysis
from analysis.product_analysis import ProductAnalysis
from analysis.customer_analysis import CustomerAnalysis

from visualization.dashboard import Dashboard
from dashboard import render_dashboard_page
from analytics import render_analysis_page, render_data_quality_page
from machine_learning import render_forecast_page


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
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .kpi-label {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 20px;
        font-weight: 600;
        color: #111827;
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
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "📈 Dashboard"


# ==================== HÀM CHÍNH ====================
def main():
    """Hàm chính của ứng dụng"""

    # Hộp điều khiển bên trái (Sidebar)
    st.sidebar.markdown("## ⚙️ MENU")

    menu_options = [
        "📈 Dashboard",
        "📁 Upload Dữ Liệu",
        "🧹 Làm Sạch Dữ Liệu",
        "📊 Phân Tích Dữ Liệu",
        "🔍 Đánh Giá Chất Lượng",
        "🔮 Dự Báo",
        "📋 Xuất Báo Cáo"
    ]

    try:
        default_index = menu_options.index(st.session_state.menu_selection)
    except ValueError:
        default_index = 0

    selected_menu = st.sidebar.radio(
        "Chức năng",
        menu_options,
        index=default_index,
        key="menu_selection"
    )

    # ========== DASHBOARD ==========
    if selected_menu == "📈 Dashboard":
        if st.session_state.df_cleaned is None and st.session_state.df is None:
            st.warning("⚠️ Vui lòng upload dữ liệu trước")
        else:
            render_dashboard_page(st.session_state.df_cleaned, raw_df=st.session_state.df)

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
            render_analysis_page(st.session_state.df_cleaned)


    # ========== ĐÁNH GIÁ CHẤT LƯỢNG ==========
    elif selected_menu == "🔍 Đánh Giá Chất Lượng":
        if st.session_state.df is None:
            st.warning("⚠️ Vui lòng upload dữ liệu trước")
        else:
            render_data_quality_page(st.session_state.df)

    # ========== DỰ BÁO ==========
    elif selected_menu == "🔮 Dự Báo":
        if st.session_state.df_cleaned is None:
            st.warning("⚠️ Vui lòng làm sạch dữ liệu trước")
        else:
            render_forecast_page(st.session_state.df_cleaned)

    # ========== XUẤT BÁO CÁO ==========
    elif selected_menu == "📋 Xuất Báo Cáo":
        if st.session_state.df_cleaned is None:
            st.warning("⚠️ Vui lòng làm sạch dữ liệu trước")
        else:
            display_report_page()


# ==================== CÁC TRANG CHỨC NĂNG ====================

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
    - ✅ Xóa dữ liệu trùng lặp
    - ✅ Xử lý giá trị NULL
    - ✅ Chuẩn hóa dữ liệu ngày tháng
    - ✅ Chuyển đổi kiểu dữ liệu
    - ✅ Loại bỏ dữ liệu lỗi
    """)

    if st.button("🚀 Làm Sạch Dữ Liệu", key="clean_btn"):
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
    render_analysis_page(st.session_state.df_cleaned)


def display_data_quality_page():
    """Trang đánh giá chất lượng dữ liệu"""
    render_data_quality_page(st.session_state.df)


def display_dashboard_page():
    """Trang dashboard"""
    render_dashboard_page(st.session_state.df_cleaned)


def display_forecast_page():
    """Trang dự báo"""
    render_forecast_page(st.session_state.df_cleaned)


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


"""
Dashboard page rendering.
"""
import streamlit as st
import pandas as pd

from analysis.revenue_analysis import RevenueAnalysis
from analysis.product_analysis import ProductAnalysis
from analysis.customer_analysis import CustomerAnalysis
from visualization.charts import ChartGenerator
from visualization.dashboard import Dashboard
from heatmap import render_heatmap_section


def _render_kpi_cards(df: pd.DataFrame) -> None:
    revenue_analysis = RevenueAnalysis(df)
    customer_analysis = CustomerAnalysis(df)

    total_revenue = revenue_analysis.total_revenue()
    total_orders = revenue_analysis.total_orders()
    total_products = revenue_analysis.total_products_sold()
    avg_order = revenue_analysis.average_order_value()
    total_customers = customer_analysis.total_customers()

    cards = [
        ("Tổng Doanh Thu", f"${total_revenue:,.2f}"),
        ("Tổng Đơn Hàng", f"{total_orders:,}"),
        ("Tổng Sản Phẩm", f"{total_products:,}"),
        ("Giá Trị TB/Đơn", f"${avg_order:,.2f}"),
        ("Tổng Khách Hàng", f"{total_customers:,}"),
    ]

    cols = st.columns(len(cards))
    for idx, (label, value) in enumerate(cards):
        with cols[idx]:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_dashboard_page(df: pd.DataFrame, raw_df: pd.DataFrame = None) -> None:
    st.markdown("## 📈 Dashboard")

    if (df is None or df.empty) and (raw_df is None or raw_df.empty):
        st.info("Chưa có dữ liệu để hiển thị dashboard.")
        return

    if raw_df is not None and not raw_df.empty:
        st.markdown("### 📄 Dữ Liệu Gốc")
        total_rows = len(raw_df)
        total_cols = len(raw_df.columns)
        missing_total = int(raw_df.isnull().sum().sum())
        duplicate_rows = int(raw_df.duplicated().sum())

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tổng dòng", f"{total_rows:,}")
        with col2:
            st.metric("Số cột", f"{total_cols:,}")
        with col3:
            st.metric("Missing values", f"{missing_total:,}")
        with col4:
            st.metric("Dòng trùng", f"{duplicate_rows:,}")

        with st.expander("Xem danh sách dữ liệu gốc", expanded=True):
            st.dataframe(raw_df, use_container_width=True)

    if df is None or df.empty:
        st.info("Chưa có dữ liệu đã làm sạch để hiển thị phân tích dashboard.")
        return

    dashboard = Dashboard(df)

    st.markdown("### 🔍 Bộ Lọc Dữ Liệu")
    filtered_df = dashboard.apply_all_filters()
    st.info(f"📌 Dữ liệu hiển thị: {len(filtered_df)} dòng (từ {len(df)} dòng gốc)")

    with st.spinner("Đang tải dashboard..."):
        st.markdown("---")
        st.markdown("### 📊 KPI CHÍNH")
        _render_kpi_cards(filtered_df)

        tab1, tab2, tab3 = st.tabs(["💰 Doanh Thu", "📦 Sản Phẩm", "👥 Khách Hàng"])

        with tab1:
            revenue_analysis = RevenueAnalysis(filtered_df)
            chart_gen = ChartGenerator()

            col1, col2 = st.columns(2)
            with col1:
                revenue_by_month = revenue_analysis.revenue_by_month()
                if not revenue_by_month.empty:
                    fig = chart_gen.area_chart(revenue_by_month, "Month", "Revenue", "📊 Doanh Thu Theo Tháng")
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                revenue_by_category = revenue_analysis.revenue_by_category()
                if not revenue_by_category.empty:
                    fig = chart_gen.pie_chart(revenue_by_category, "Revenue", "Category", "📊 Doanh Thu Theo Danh Mục")
                    st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                revenue_by_region = revenue_analysis.revenue_by_region()
                if not revenue_by_region.empty:
                    fig = chart_gen.bar_chart(revenue_by_region, "Region", "Revenue", "📊 Doanh Thu Theo Khu Vực")
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                payment_method = revenue_analysis.revenue_by_payment_method()
                if not payment_method.empty:
                    fig = chart_gen.bar_chart(
                        payment_method,
                        "Payment Method",
                        "Revenue",
                        "📊 Doanh Thu Theo Phương Thức Thanh Toán",
                    )
                    st.plotly_chart(fig, use_container_width=True)

            channel_data = revenue_analysis.revenue_by_sales_channel()
            if not channel_data.empty:
                fig = chart_gen.pie_chart(channel_data, "Revenue", "Sales Channel", "🛒 Doanh Thu Theo Kênh Bán Hàng")
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            product_analysis = ProductAnalysis(filtered_df)
            chart_gen = ChartGenerator()

            col1, col2 = st.columns(2)
            with col1:
                top_products = product_analysis.top_products_by_sales(10)
                if not top_products.empty:
                    fig = chart_gen.bar_chart(top_products, "Product", "Total_Quantity", "🏆 Top 10 Sản Phẩm Bán Chạy")
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                products_by_cat = product_analysis.products_by_category()
                if not products_by_cat.empty:
                    fig = chart_gen.pie_chart(products_by_cat, "Total_Quantity", "Category", "📊 Sản Phẩm Theo Danh Mục")
                    st.plotly_chart(fig, use_container_width=True)

        with tab3:
            customer_analysis = CustomerAnalysis(filtered_df)
            chart_gen = ChartGenerator()

            col1, col2 = st.columns(2)
            with col1:
                top_customers = customer_analysis.top_customers_by_spending(10)
                if not top_customers.empty:
                    fig = chart_gen.bar_chart(top_customers, "Customer", "Total_Spending", "💰 Top 10 Khách Hàng")
                    st.plotly_chart(fig, use_container_width=True)

            with col2:
                customers_per_region = customer_analysis.customer_per_region()
                if not customers_per_region.empty:
                    fig = chart_gen.bar_chart(customers_per_region, "Region", "Customer_Count", "🗺️ Khách Hàng Theo Khu Vực")
                    st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        render_heatmap_section(filtered_df)


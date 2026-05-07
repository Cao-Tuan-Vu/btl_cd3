"""
Analytics and data quality pages.
"""
import streamlit as st
import pandas as pd

from analysis.revenue_analysis import RevenueAnalysis
from analysis.product_analysis import ProductAnalysis
from analysis.customer_analysis import CustomerAnalysis
from visualization.charts import ChartGenerator
from visualization.dashboard import Dashboard
from utils.data_quality import DataQualityAssessment


def render_analysis_page(df: pd.DataFrame) -> None:
    st.markdown("## 📊 Phân Tích Dữ Liệu")

    if df is None or df.empty:
        st.info("Chưa có dữ liệu để phân tích.")
        return

    st.markdown("### 🔍 Bộ Lọc Dữ Liệu")
    dashboard = Dashboard(df)
    filtered_df = dashboard.apply_all_filters()
    st.info(f"📌 Dữ liệu hiển thị: {len(filtered_df)} dòng (từ {len(df)} dòng gốc)")

    with st.spinner("Đang phân tích dữ liệu..."):
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

        col1, col2 = st.columns(2)
        with col1:
            revenue_by_month = revenue_analysis.revenue_by_month()
            if not revenue_by_month.empty:
                chart_gen = ChartGenerator()
                fig = chart_gen.line_chart(revenue_by_month, "Month", "Revenue", "📊 Doanh Thu Theo Tháng")
                st.plotly_chart(fig, use_container_width=True)

        revenue_by_day = revenue_analysis.revenue_by_day()
        if not revenue_by_day.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.line_chart(revenue_by_day, "Date", "Revenue", "📅 Doanh Thu Theo Ngày")
            st.plotly_chart(fig, use_container_width=True)

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
                fig = chart_gen.pie_chart(payment_method, "Revenue", "Payment Method", "💳 Cơ Cấu Doanh Thu Theo Thanh Toán")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            channel_data = revenue_analysis.revenue_by_sales_channel()
            if not channel_data.empty:
                chart_gen = ChartGenerator()
                fig = chart_gen.bar_chart(channel_data, "Sales Channel", "Revenue", "🛒 Doanh Thu Theo Kênh Bán Hàng")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Không tìm thấy cột kênh bán hàng (ví dụ: Sales_Channel/Channel).")

        st.markdown("---")
        st.markdown("### 📦 Phân Tích Sản Phẩm")

        product_analysis = ProductAnalysis(filtered_df)
        col1, col2 = st.columns(2)
        with col1:
            top_products_sales = product_analysis.top_products_by_sales(10)
            if not top_products_sales.empty:
                chart_gen = ChartGenerator()
                fig = chart_gen.bar_chart(top_products_sales, "Product", "Total_Quantity", "🏆 Top 10 Sản Phẩm Bán Chạy")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            top_products_revenue = product_analysis.top_products_by_revenue(10)
            if not top_products_revenue.empty:
                chart_gen = ChartGenerator()
                fig = chart_gen.bar_chart(top_products_revenue, "Product", "Revenue", "💰 Top 10 Sản Phẩm Doanh Thu")
                st.plotly_chart(fig, use_container_width=True)

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

        col1, col2 = st.columns(2)
        with col1:
            top_customers = customer_analysis.top_customers_by_spending(10)
            if not top_customers.empty:
                chart_gen = ChartGenerator()
                fig = chart_gen.bar_chart(top_customers, "Customer", "Total_Spending", "💰 Top 10 Khách Hàng Chi Tiêu")
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            customers_per_region = customer_analysis.customer_per_region()
            if not customers_per_region.empty:
                chart_gen = ChartGenerator()
                fig = chart_gen.pie_chart(customers_per_region, "Customer_Count", "Region", "🗺️ Khách Hàng Theo Khu Vực")
                st.plotly_chart(fig, use_container_width=True)


def render_data_quality_page(df: pd.DataFrame) -> None:
    st.markdown("## 🔍 Đánh Giá Chất Lượng Dữ Liệu")

    if df is None or df.empty:
        st.info("Chưa có dữ liệu để đánh giá.")
        return

    quality_assessor = DataQualityAssessment(df)
    metrics = quality_assessor.get_data_quality_metrics()

    st.markdown("### 📊 Chỉ Số Chất Lượng Tổng Thể")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        score = metrics["Điểm Chất Lượng"]
        if score >= 80:
            color = "🟢"
        elif score >= 60:
            color = "🟡"
        else:
            color = "🔴"
        st.metric(f"{color} Điểm Chất Lượng", f"{score}/100")

    with col2:
        st.metric("📌 Tổng Dòng", f"{metrics['Tổng Dòng']:,}")
    with col3:
        st.metric("📌 Tổng Cột", f"{metrics['Tổng Cột']}")
    with col4:
        st.metric("📌 Tổng Ô Dữ Liệu", f"{metrics['Tổng Ô Dữ Liệu']:,}")

    st.markdown("---")
    st.markdown("### 📈 Chi Tiết Chỉ Số")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info(f"❌ Ô Thiếu Dữ Liệu: {metrics['Ô Thiếu Dữ Liệu']:,}\n({metrics['Tỷ Lệ Thiếu (%)']:.2f}%)")
    with col2:
        st.warning(f"🔄 Bản Ghi Trùng Lặp: {metrics['Bản Ghi Trùng Lặp']:,}\n({metrics['Tỷ Lệ Trùng Lặp (%)']:.2f}%)")
    with col3:
        completeness_pct = 100 - metrics["Tỷ Lệ Thiếu (%)"]
        st.success(f"✅ Tỷ Lệ Đầy Đủ: {completeness_pct:.2f}%")
    with col4:
        uniqueness_pct = 100 - metrics["Tỷ Lệ Trùng Lặp (%)"]
        st.success(f"✅ Tỷ Lệ Độc Lập: {uniqueness_pct:.2f}%")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Hoàn Chỉnh", "🔄 Trùng Lặp", "📊 Ngoại Lệ", "📈 Thống Kê", "🎯 Kiểm Tra"])

    with tab1:
        st.markdown("### 📋 Báo Cáo Tỷ Lệ Hoàn Chỉnh")
        completeness_df = quality_assessor.get_completeness_report()
        st.dataframe(completeness_df, use_container_width=True)

        if not completeness_df.empty:
            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(completeness_df, "Cột", "Tỷ Lệ Đầy Đủ (%)", "✅ Tỷ Lệ Dữ Liệu Đầy Đủ Theo Cột")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 🔄 Báo Cáo Bản Ghi Trùng Lặp")
        duplicates_info = quality_assessor.get_duplicates_report()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📌 Tổng Bản Ghi Trùng Lặp", f"{duplicates_info['Tổng Bản Ghi Trùng Lặp']:,}")
        with col2:
            st.metric("📊 Tỷ Lệ Trùng Lặp", f"{duplicates_info['Tỷ Lệ Trùng Lặp (%)']:.2f}%")

        st.markdown("#### Chi Tiết Trùng Lặp Theo Cột:")
        if duplicates_info["Chi Tiết Theo Cột"]:
            dup_df = pd.DataFrame(
                [
                    {"Cột": col, "Số Trùng Lặp": data["Trùng Lặp"], "Tỷ Lệ (%)": data["Tỷ Lệ (%)"]}
                    for col, data in duplicates_info["Chi Tiết Theo Cột"].items()
                ]
            )
            st.dataframe(dup_df, use_container_width=True)

            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(dup_df, "Cột", "Số Trùng Lặp", "🔄 Số Bản Ghi Trùng Lặp Theo Cột")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ Không có bản ghi trùng lặp!")

    with tab3:
        st.markdown("### 📊 Báo Cáo Giá Trị Ngoại Lệ (Outliers)")
        outliers_df = quality_assessor.get_outliers_report()

        if not outliers_df.empty:
            st.dataframe(outliers_df, use_container_width=True)
            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(outliers_df, "Cột", "Tỷ Lệ (%)", "⚠️ Tỷ Lệ Giá Trị Ngoại Lệ Theo Cột")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ Không tìm thấy giá trị ngoại lệ đáng kể!")

    with tab4:
        st.markdown("### 📈 Thống Kê Mô Tả (Numeric Columns)")
        stats_df = quality_assessor.get_statistical_summary()
        if not stats_df.empty:
            st.dataframe(stats_df.round(2), use_container_width=True)
        else:
            st.info("Không có cột số để hiển thị thống kê.")

    with tab5:
        st.markdown("### 🎯 Phân Tích Phân Phối Giá Trị")
        selected_col = st.selectbox("Chọn cột để xem phân phối", df.columns)
        distribution_df = quality_assessor.get_value_distribution(selected_col, top_n=15)

        if not distribution_df.empty:
            st.dataframe(distribution_df, use_container_width=True)
            chart_gen = ChartGenerator()
            fig = chart_gen.bar_chart(
                distribution_df,
                "Giá Trị",
                "Tỷ Lệ (%)",
                f"📊 Phân Phối Giá Trị - {selected_col}",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Cột này không có dữ liệu hoặc không hợp lệ.")

    st.markdown("---")
    st.markdown("### 💡 Khuyến Nghị")

    recommendations = []
    if metrics["Tỷ Lệ Thiếu (%)"] > 10:
        recommendations.append("❌ Tỷ lệ dữ liệu thiếu > 10%. Cân nhắc làm sạch hoặc loại bỏ các cột có thiếu dữ liệu nhiều.")
    if metrics["Tỷ Lệ Trùng Lặp (%)"] > 5:
        recommendations.append("⚠️ Tỷ lệ bản ghi trùng lặp > 5%. Kiểm tra và loại bỏ các bản ghi trùng lặp.")
    if not outliers_df.empty:
        recommendations.append(f"⚠️ Phát hiện {len(outliers_df)} cột có giá trị ngoại lệ. Xem xét có loại bỏ hay không.")
    if metrics["Điểm Chất Lượng"] < 60:
        recommendations.append("🔴 Điểm chất lượng < 60. Dữ liệu cần được làm sạch kỹ lưỡng trước khi phân tích.")
    elif metrics["Điểm Chất Lượng"] < 80:
        recommendations.append("🟡 Điểm chất lượng ở mức trung bình. Cân nhắc làm sạch dữ liệu thêm.")
    else:
        recommendations.append("🟢 Chất lượng dữ liệu tốt. Sẵn sàng cho phân tích sâu!")

    if recommendations:
        for rec in recommendations:
            st.info(rec)


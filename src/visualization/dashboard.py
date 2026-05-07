"""
Module dashboard chính
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px


class Dashboard:
    """Lớp để quản lý dashboard"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    @staticmethod
    def find_column(columns, keywords):
        """Tìm cột đầu tiên khớp danh sách từ khóa."""
        for col in columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in keywords):
                return col
        return None

    def display_kpi_cards(self, metrics: dict):
        """Hiển thị KPI cards"""
        cols = st.columns(len(metrics))

        for idx, (metric_name, metric_value) in enumerate(metrics.items()):
            with cols[idx]:
                st.metric(
                    label=metric_name,
                    value=f"{metric_value:,.0f}" if isinstance(metric_value, (int, float)) else metric_value
                )

    def display_summary_stats(self, df: pd.DataFrame = None):
        """Hiển thị tóm tắt thống kê theo dữ liệu hiện tại hoặc dữ liệu đã lọc."""
        data = self.df if df is None else df
        st.subheader("📊 Thống Kê Tổng Quan")

        cols = st.columns(5)

        # Đếm độc lập và tính toán metrics
        with cols[0]:
            st.metric("📦 Tổng Đơn Hàng", len(data))

        qty_cols = [col for col in data.columns if 'quantity' in col.lower()]
        if qty_cols:
            with cols[1]:
                total_qty = int(data[qty_cols[0]].sum())
                st.metric("📈 Tổng Sản Phẩm", total_qty)

        revenue_cols = [col for col in data.columns if 'revenue' in col.lower()]
        if revenue_cols:
            with cols[2]:
                total_revenue = data[revenue_cols[0]].sum()
                st.metric("💰 Tổng Doanh Thu", f"${total_revenue:,.2f}")

        customer_cols = [col for col in data.columns if 'customer' in col.lower()]
        if customer_cols:
            with cols[3]:
                total_customers = data[customer_cols[0]].nunique()
                st.metric("👥 Tổng Khách Hàng", total_customers)

        profit_cols = [col for col in data.columns if 'profit' in col.lower()]
        if profit_cols:
            with cols[4]:
                total_profit = data[profit_cols[0]].sum()
                st.metric("📊 Tổng Lợi Nhuận", f"${total_profit:,.2f}")

    def create_date_range_filter(self):
        """Tạo bộ lọc theo khoảng ngày"""
        date_cols = [col for col in self.df.columns if 'date' in col.lower()]

        if date_cols:
            st.sidebar.markdown("### 📅 Bộ Lọc Thời Gian")

            df_copy = self.df.copy()
            df_copy[date_cols[0]] = pd.to_datetime(df_copy[date_cols[0]])

            min_date = df_copy[date_cols[0]].min().date()
            max_date = df_copy[date_cols[0]].max().date()

            start_date = st.sidebar.date_input(
                "Từ ngày",
                min_date,
                min_value=min_date,
                max_value=max_date
            )

            end_date = st.sidebar.date_input(
                "Đến ngày",
                max_date,
                min_value=min_date,
                max_value=max_date
            )

            if start_date <= end_date:
                return date_cols[0], start_date, end_date
            else:
                st.sidebar.error("❌ Ngày bắt đầu phải <= ngày kết thúc")
                return date_cols[0], min_date, max_date

        return None, None, None

    def filter_by_date_range(self, date_col, start_date, end_date):
        """Lọc dữ liệu theo khoảng ngày"""
        df_copy = self.df.copy()
        df_copy[date_col] = pd.to_datetime(df_copy[date_col])
        df_copy = df_copy[
            (df_copy[date_col] >= pd.Timestamp(start_date)) &
            (df_copy[date_col] <= pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
        ]
        return df_copy

    def create_year_month_filter(self, df_filtered: pd.DataFrame, date_col: str):
        """Tạo bộ lọc năm và tháng."""
        st.sidebar.markdown("### 🗓️ Bộ Lọc Năm/Tháng")
        date_values = pd.to_datetime(df_filtered[date_col], errors='coerce').dropna()
        if date_values.empty:
            return None, None

        years = sorted(date_values.dt.year.unique().tolist())
        selected_years = st.sidebar.multiselect("Chọn năm", years, default=years)

        months = list(range(1, 13))
        selected_months = st.sidebar.multiselect("Chọn tháng", months, default=months)
        return selected_years, selected_months

    def create_product_filter(self, df_filtered: pd.DataFrame):
        """Tạo bộ lọc theo sản phẩm."""
        product_col = self.find_column(df_filtered.columns, ['product_name', 'product'])
        if product_col:
            st.sidebar.markdown("### 📦 Bộ Lọc Sản Phẩm")
            products = sorted(df_filtered[product_col].dropna().astype(str).unique().tolist())
            selected_products = st.sidebar.multiselect("Chọn sản phẩm", products, default=products)
            return product_col, selected_products
        return None, None

    def create_channel_filter(self, df_filtered: pd.DataFrame):
        """Tạo bộ lọc theo kênh bán hàng."""
        channel_col = self.find_column(df_filtered.columns, ['sales_channel', 'channel'])
        if channel_col:
            st.sidebar.markdown("### 🛒 Bộ Lọc Kênh Bán Hàng")
            channels = sorted(df_filtered[channel_col].dropna().astype(str).unique().tolist())
            selected_channels = st.sidebar.multiselect("Chọn kênh", channels, default=channels)
            return channel_col, selected_channels
        return None, None

    def create_category_filter(self, df_filtered: pd.DataFrame = None):
        """Tạo bộ lọc theo danh mục"""
        source_df = self.df if df_filtered is None else df_filtered
        cat_cols = [col for col in source_df.columns if 'category' in col.lower()]

        if cat_cols:
            st.sidebar.markdown("### 📂 Bộ Lọc Danh Mục")

            categories = source_df[cat_cols[0]].dropna().astype(str).unique().tolist()
            selected_categories = st.sidebar.multiselect(
                "Chọn danh mục",
                categories,
                default=categories
            )

            return cat_cols[0], selected_categories

        return None, None

    def filter_by_category(self, cat_col, categories):
        """Lọc dữ liệu theo danh mục"""
        return self.df[self.df[cat_col].isin(categories)]

    def create_region_filter(self, df_filtered: pd.DataFrame = None):
        """Tạo bộ lọc theo khu vực"""
        source_df = self.df if df_filtered is None else df_filtered
        region_cols = [col for col in source_df.columns if 'region' in col.lower()]

        if region_cols:
            st.sidebar.markdown("### 🗺️ Bộ Lọc Khu Vực")

            regions = source_df[region_cols[0]].dropna().astype(str).unique().tolist()
            selected_regions = st.sidebar.multiselect(
                "Chọn khu vực",
                regions,
                default=regions,
                key="regions"
            )

            return region_cols[0], selected_regions

        return None, None

    def filter_by_region(self, region_col, regions):
        """Lọc dữ liệu theo khu vực"""
        return self.df[self.df[region_col].isin(regions)]

    def apply_all_filters(self):
        """Áp dụng tất cả các bộ lọc"""
        filtered_df = self.df.copy()
        st.sidebar.markdown("## 🎛️ Bộ Lọc")

        # Bộ lọc theo ngày
        date_col, start_date, end_date = self.create_date_range_filter()
        if date_col:
            filtered_df = filtered_df.copy()
            filtered_df[date_col] = pd.to_datetime(filtered_df[date_col], errors='coerce')
            filtered_df = filtered_df[
                (filtered_df[date_col] >= pd.Timestamp(start_date)) &
                (filtered_df[date_col] <= pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
            ]

            selected_years, selected_months = self.create_year_month_filter(filtered_df, date_col)
            if selected_years:
                filtered_df = filtered_df[filtered_df[date_col].dt.year.isin(selected_years)]
            if selected_months:
                filtered_df = filtered_df[filtered_df[date_col].dt.month.isin(selected_months)]

        # Bộ lọc theo danh mục
        cat_col, selected_categories = self.create_category_filter(filtered_df)
        if cat_col and selected_categories:
            filtered_df = filtered_df[filtered_df[cat_col].isin(selected_categories)]

        # Bộ lọc theo khu vực
        region_col, selected_regions = self.create_region_filter(filtered_df)
        if region_col and selected_regions:
            filtered_df = filtered_df[filtered_df[region_col].isin(selected_regions)]

        # Bộ lọc theo sản phẩm
        product_col, selected_products = self.create_product_filter(filtered_df)
        if product_col and selected_products:
            filtered_df = filtered_df[filtered_df[product_col].astype(str).isin(selected_products)]

        # Bộ lọc theo kênh bán hàng
        channel_col, selected_channels = self.create_channel_filter(filtered_df)
        if channel_col and selected_channels:
            filtered_df = filtered_df[filtered_df[channel_col].astype(str).isin(selected_channels)]

        return filtered_df

    @staticmethod
    def display_data_preview(df: pd.DataFrame):
        """Hiển thị xem trước dữ liệu"""
        st.subheader("👀 Xem Trước Dữ Liệu")

        col1, col2 = st.columns(2)
        with col1:
            st.info(f"📌 Số dòng: {len(df)}")
        with col2:
            st.info(f"📌 Số cột: {len(df.columns)}")

        st.dataframe(df.head(10), use_container_width=True)

    @staticmethod
    def display_data_types(df: pd.DataFrame):
        """Hiển thị kiểu dữ liệu"""
        st.subheader("🔍 Kiểu Dữ Liệu")

        dtype_info = pd.DataFrame({
            'Cột': df.columns,
            'Kiểu': df.dtypes.values
        })

        st.dataframe(dtype_info, use_container_width=True)


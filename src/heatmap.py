"""
Heatmap rendering utilities for dashboard.
"""
from typing import Dict, List, Optional, Tuple

import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def _find_column(columns: List[str], keywords: List[str]) -> Optional[str]:
    for col in columns:
        col_lower = col.lower()
        if any(keyword in col_lower for keyword in keywords):
            return col
    return None


def _resolve_numeric_columns(df: pd.DataFrame) -> Dict[str, str]:
    """Resolve required numeric columns to actual columns in dataframe."""
    candidates = {
        "quantity": ["quantity", "qty"],
        "unit_price_vnd": ["unit_price_vnd", "unit_price", "price", "unit price"],
        "discount_vnd": ["discount_vnd", "discount", "discount_percent"],
        "shipping_fee_vnd": ["shipping_fee_vnd", "shipping_cost", "shipping fee"],
        "total_amount_vnd": ["total_amount_vnd", "total_price", "total", "revenue"],
        "rating": ["rating", "star"],
    }

    resolved = {}
    for canonical, keywords in candidates.items():
        col = _find_column(df.columns.tolist(), keywords)
        if col:
            resolved[canonical] = col
    return resolved


def _prepare_heatmap_df(df: pd.DataFrame, resolved_cols: Dict[str, str]) -> pd.DataFrame:
    if not resolved_cols:
        return pd.DataFrame()

    work_df = df.copy()
    selected = {}
    for alias, col in resolved_cols.items():
        series = pd.to_numeric(work_df[col], errors="coerce")
        selected[alias] = series

    return pd.DataFrame(selected)


def _apply_heatmap_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply platform, city, product_category filters in sidebar."""
    st.sidebar.markdown("### 🔥 Heatmap Filters")

    platform_col = _find_column(df.columns.tolist(), ["platform", "sales_channel", "channel"])
    city_col = _find_column(df.columns.tolist(), ["city", "region", "province", "state"])
    category_col = _find_column(df.columns.tolist(), ["product_category", "category"])

    filtered = df.copy()

    if platform_col:
        platforms = sorted(filtered[platform_col].dropna().astype(str).unique().tolist())
        selected_platforms = st.sidebar.multiselect("Platform", platforms, default=platforms)
        filtered = filtered[filtered[platform_col].astype(str).isin(selected_platforms)]

    if city_col:
        cities = sorted(filtered[city_col].dropna().astype(str).unique().tolist())
        selected_cities = st.sidebar.multiselect("City", cities, default=cities)
        filtered = filtered[filtered[city_col].astype(str).isin(selected_cities)]

    if category_col:
        categories = sorted(filtered[category_col].dropna().astype(str).unique().tolist())
        selected_categories = st.sidebar.multiselect("Product Category", categories, default=categories)
        filtered = filtered[filtered[category_col].astype(str).isin(selected_categories)]

    return filtered


def _render_corr_heatmap(df: pd.DataFrame) -> None:
    resolved = _resolve_numeric_columns(df)
    corr_df = _prepare_heatmap_df(df, resolved)

    if corr_df.empty or corr_df.shape[1] < 2:
        st.info("Không đủ cột số để hiển thị heatmap tương quan.")
        return

    corr = corr_df.corr().round(2)

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="YlOrRd",
        linewidths=0.5,
        cbar=True,
        square=True,
        ax=ax,
    )
    ax.set_title("Heatmap Tương Quan (Numeric Attributes)", fontsize=14)
    st.pyplot(fig, clear_figure=True)


def _get_date_col(df: pd.DataFrame) -> Optional[str]:
    return _find_column(df.columns.tolist(), ["date", "time"])


def _get_revenue_col(df: pd.DataFrame) -> Optional[str]:
    revenue_col = _find_column(df.columns.tolist(), ["revenue", "total_amount", "total_price", "total"])
    if revenue_col:
        return revenue_col

    qty_col = _find_column(df.columns.tolist(), ["quantity", "qty"])
    price_col = _find_column(df.columns.tolist(), ["unit_price", "price"])
    if qty_col and price_col:
        df["__calc_revenue__"] = pd.to_numeric(df[qty_col], errors="coerce").fillna(0) * pd.to_numeric(
            df[price_col], errors="coerce"
        ).fillna(0)
        return "__calc_revenue__"

    return None


def _render_month_heatmap(df: pd.DataFrame) -> None:
    date_col = _get_date_col(df)
    if not date_col:
        st.info("Không tìm thấy cột ngày để hiển thị heatmap theo tháng.")
        return

    revenue_col = _get_revenue_col(df.copy())
    qty_col = _find_column(df.columns.tolist(), ["quantity", "qty"])

    work_df = df.copy()
    work_df[date_col] = pd.to_datetime(work_df[date_col], errors="coerce")
    work_df = work_df.dropna(subset=[date_col])
    work_df["Month"] = work_df[date_col].dt.to_period("M").astype(str)

    metrics = {}
    if revenue_col:
        metrics["Revenue"] = pd.to_numeric(work_df[revenue_col], errors="coerce").fillna(0)
    if qty_col:
        metrics["Quantity"] = pd.to_numeric(work_df[qty_col], errors="coerce").fillna(0)

    if not metrics:
        st.info("Không đủ dữ liệu để tính heatmap theo tháng.")
        return

    metric_df = pd.DataFrame(metrics)
    metric_df["Month"] = work_df["Month"].values

    pivot = metric_df.groupby("Month").sum().sort_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".0f",
        cmap="Blues",
        linewidths=0.5,
        cbar=True,
        ax=ax,
    )
    ax.set_title("Heatmap Theo Tháng", fontsize=14)
    st.pyplot(fig, clear_figure=True)


def _render_city_revenue_heatmap(df: pd.DataFrame) -> None:
    city_col = _find_column(df.columns.tolist(), ["city", "region", "province", "state"])
    if not city_col:
        st.info("Không tìm thấy cột city/region để hiển thị heatmap doanh thu theo thành phố.")
        return

    date_col = _get_date_col(df)
    revenue_col = _get_revenue_col(df.copy())
    if not revenue_col:
        st.info("Không tìm thấy cột doanh thu để hiển thị heatmap theo thành phố.")
        return

    work_df = df.copy()
    if date_col:
        work_df[date_col] = pd.to_datetime(work_df[date_col], errors="coerce")
        work_df = work_df.dropna(subset=[date_col])
        work_df["Month"] = work_df[date_col].dt.to_period("M").astype(str)
        pivot = work_df.pivot_table(
            index=city_col,
            columns="Month",
            values=revenue_col,
            aggfunc="sum",
            fill_value=0,
        )
    else:
        pivot = work_df.pivot_table(
            index=city_col,
            values=revenue_col,
            aggfunc="sum",
            fill_value=0,
        )

    pivot = pivot.sort_values(by=pivot.columns[0], ascending=False) if len(pivot.columns) > 0 else pivot

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(
        pivot,
        annot=False,
        cmap="YlGnBu",
        linewidths=0.5,
        cbar=True,
        ax=ax,
    )
    ax.set_title("Heatmap Doanh Thu Theo Thành Phố", fontsize=14)
    st.pyplot(fig, clear_figure=True)


def _render_status_heatmap(df: pd.DataFrame) -> None:
    status_col = _find_column(df.columns.tolist(), ["status"])
    if not status_col:
        st.info("Không tìm thấy cột trạng thái đơn hàng để hiển thị heatmap.")
        return

    date_col = _get_date_col(df)
    work_df = df.copy()

    if date_col:
        work_df[date_col] = pd.to_datetime(work_df[date_col], errors="coerce")
        work_df = work_df.dropna(subset=[date_col])
        work_df["Month"] = work_df[date_col].dt.to_period("M").astype(str)
        pivot = work_df.pivot_table(
            index=status_col,
            columns="Month",
            values=status_col,
            aggfunc="count",
            fill_value=0,
        )
    else:
        pivot = work_df.pivot_table(
            index=status_col,
            values=status_col,
            aggfunc="count",
            fill_value=0,
        )

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".0f",
        cmap="Oranges",
        linewidths=0.5,
        cbar=True,
        ax=ax,
    )
    ax.set_title("Heatmap Trạng Thái Đơn Hàng", fontsize=14)
    st.pyplot(fig, clear_figure=True)


def render_heatmap_section(df: pd.DataFrame) -> None:
    """Render heatmap section with filters and multiple heatmaps."""
    if df is None or df.empty:
        st.info("Chưa có dữ liệu để hiển thị heatmap.")
        return

    filtered_df = _apply_heatmap_filters(df)

    st.markdown("### 🔥 Heatmap Chi Tiết")
    _render_corr_heatmap(filtered_df)

    st.markdown("### 📅 Heatmap Theo Tháng")
    _render_month_heatmap(filtered_df)

    st.markdown("### 🏙️ Heatmap Doanh Thu Theo Thành Phố")
    _render_city_revenue_heatmap(filtered_df)

    st.markdown("### 📦 Heatmap Trạng Thái Đơn Hàng")
    _render_status_heatmap(filtered_df)


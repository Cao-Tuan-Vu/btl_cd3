"""
Forecasting (machine learning) page.
"""
import streamlit as st
import pandas as pd

from utils.forecast import DataForecaster


def render_forecast_page(df: pd.DataFrame) -> None:
    st.markdown("## 🔮 Dự Báo Dữ Liệu")

    if df is None or df.empty:
        st.info("Chưa có dữ liệu để dự báo.")
        return

    forecast_type = st.selectbox("Chọn loại dự báo", ["Doanh Thu", "Số Đơn Hàng"])
    forecast_period = st.selectbox("Chọn kỳ dự báo", ["Hàng Ngày (30 ngày tới)", "Hàng Tháng (12 tháng tới)"])

    if st.button("🚀 Thực Hiện Dự Báo"):
        with st.spinner("⏳ Đang tính toán..."):
            try:
                date_cols = [col for col in df.columns if "date" in col.lower()]
                if not date_cols:
                    st.error("❌ Không tìm thấy cột ngày tháng")
                    return

                date_col = date_cols[0]
                if forecast_type == "Doanh Thu":
                    value_cols = [col for col in df.columns if "revenue" in col.lower()]
                    if not value_cols:
                        st.error("❌ Không tìm thấy cột doanh thu")
                        return
                    value_col = value_cols[0]
                    title_prefix = "Doanh Thu"
                else:
                    value_cols = [col for col in df.columns if "quantity" in col.lower()]
                    if not value_cols:
                        st.error("❌ Không tìm thấy cột số lượng")
                        return
                    value_col = value_cols[0]
                    title_prefix = "Số Đơn Hàng"

                forecast_model = DataForecaster(df, date_col, value_col)
                prepared = forecast_model.prepare_data()

                if forecast_period == "Hàng Ngày (30 ngày tới)":
                    forecast_df = forecast_model.forecast_days(30)
                    title = f"🔮 Dự Báo {title_prefix} - 30 Ngày Tới"
                else:
                    forecast_df = forecast_model.forecast_months(12)
                    title = f"🔮 Dự Báo {title_prefix} - 12 Tháng Tới"

                forecast_future = forecast_df[forecast_df["ds"] > prepared["ds"].max()].copy()
                if forecast_future.empty:
                    forecast_future = forecast_df.copy()

                import plotly.graph_objects as go

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=prepared["ds"],
                        y=prepared["y"],
                        name="Dữ Liệu Gốc",
                        mode="lines",
                        line=dict(color="blue"),
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=forecast_future["ds"],
                        y=forecast_future["yhat"],
                        name="Dự Báo",
                        mode="lines",
                        line=dict(color="red"),
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=forecast_future["ds"].tolist() + forecast_future["ds"].tolist()[::-1],
                        y=forecast_future["yhat_upper"].tolist() + forecast_future["yhat_lower"].tolist()[::-1],
                        fill="toself",
                        fillcolor="rgba(255, 0, 0, 0.2)",
                        line=dict(color="rgba(255,255,255,0)"),
                        name="Khoảng tin cậy 95%",
                    )
                )

                fig.update_layout(
                    title=title,
                    xaxis_title="Thời Gian",
                    yaxis_title="Giá Trị",
                    height=600,
                    hovermode="x unified",
                    template="plotly_white",
                )
                st.plotly_chart(fig, use_container_width=True)

                components_fig = forecast_model.get_components()
                if components_fig is not None:
                    st.markdown("### 📉 Trend & Seasonality")
                    st.plotly_chart(components_fig, use_container_width=True)

                st.markdown("### 📋 Bảng Dự Báo")
                forecast_display = forecast_future[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
                forecast_display.columns = ["Ngày", "Dự Báo", "Giới Hạn Dưới", "Giới Hạn Trên"]
                st.dataframe(forecast_display, use_container_width=True)

                metrics = forecast_model.get_metrics()
                st.markdown("### 📊 Chỉ Số Hiệu Quả")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("MAPE (%)", f"{metrics.get('mape', 0):.2f}%")
                with col2:
                    st.metric("Số Điểm Dữ Liệu", f"{metrics.get('data_points', 0)}")

            except Exception as exc:
                st.error(f"❌ Lỗi dự báo: {str(exc)}")


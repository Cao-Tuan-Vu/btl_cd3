"""
Module để phân tích doanh thu
"""
import pandas as pd
import numpy as np


class RevenueAnalysis:
    """Lớp để phân tích doanh thu"""

    def __init__(self, df: pd.DataFrame):
        """
        Khởi tạo RevenueAnalysis

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame chứa dữ liệu đơn hàng
        """
        self.df = df.copy()

    @staticmethod
    def _find_column(columns, keywords):
        for col in columns:
            lower_col = col.lower()
            if any(keyword in lower_col for keyword in keywords):
                return col
        return None

    def _ensure_revenue_column(self, data: pd.DataFrame) -> str:
        """Trả về tên cột doanh thu, tự tính nếu chưa có."""
        revenue_col = self._find_column(data.columns, ['revenue'])
        if revenue_col:
            return revenue_col

        qty_col = self._find_column(data.columns, ['quantity', 'count'])
        price_col = self._find_column(data.columns, ['unit_price', 'price'])

        if qty_col and price_col:
            data['__calc_revenue__'] = pd.to_numeric(data[qty_col], errors='coerce').fillna(0) * pd.to_numeric(data[price_col], errors='coerce').fillna(0)
            return '__calc_revenue__'

        return None

    def total_revenue(self) -> float:
        """
        Tính tổng doanh thu

        Returns:
        --------
        float
            Tổng doanh thu
        """
        df = self.df.copy()
        revenue_col = self._ensure_revenue_column(df)
        if revenue_col:
            return pd.to_numeric(df[revenue_col], errors='coerce').fillna(0).sum()

        return 0

    def total_orders(self) -> int:
        """Tính tổng số đơn hàng"""
        return len(self.df)

    def total_products_sold(self) -> int:
        """Tính tổng số sản phẩm bán ra"""
        qty_cols = [col for col in self.df.columns if 'quantity' in col.lower()]
        if qty_cols:
            return int(self.df[qty_cols[0]].sum())
        return 0

    def revenue_by_month(self) -> pd.DataFrame:
        """Phân tích doanh thu theo tháng"""
        df = self.df.copy()
        date_col = self._find_column(df.columns, ['date'])
        revenue_col = self._ensure_revenue_column(df)

        if not date_col or not revenue_col:
            return pd.DataFrame()

        df['month'] = pd.to_datetime(df[date_col], errors='coerce').dt.to_period('M')
        result = df.dropna(subset=['month']).groupby('month')[revenue_col].sum().reset_index()
        result.columns = ['Month', 'Revenue']
        result['Month'] = result['Month'].astype(str)

        return result

    def revenue_by_day(self) -> pd.DataFrame:
        """Phân tích doanh thu theo ngày"""
        df = self.df.copy()
        date_col = self._find_column(df.columns, ['date'])
        revenue_col = self._ensure_revenue_column(df)

        if not date_col or not revenue_col:
            return pd.DataFrame()

        df['date'] = pd.to_datetime(df[date_col], errors='coerce').dt.date
        result = df.dropna(subset=['date']).groupby('date')[revenue_col].sum().reset_index()
        result.columns = ['Date', 'Revenue']

        return result

    def revenue_by_region(self) -> pd.DataFrame:
        """Phân tích doanh thu theo khu vực"""
        df = self.df.copy()
        region_col = self._find_column(df.columns, ['region'])
        revenue_col = self._ensure_revenue_column(df)

        if not region_col or not revenue_col:
            return pd.DataFrame()

        result = df.groupby(region_col)[revenue_col].sum().reset_index()
        result.columns = ['Region', 'Revenue']
        result = result.sort_values('Revenue', ascending=False)

        return result

    def revenue_by_category(self) -> pd.DataFrame:
        """Phân tích doanh thu theo danh mục"""
        df = self.df.copy()
        cat_col = self._find_column(df.columns, ['category'])
        revenue_col = self._ensure_revenue_column(df)

        if not cat_col or not revenue_col:
            return pd.DataFrame()

        result = df.groupby(cat_col)[revenue_col].sum().reset_index()
        result.columns = ['Category', 'Revenue']
        result = result.sort_values('Revenue', ascending=False)

        return result

    def revenue_by_payment_method(self) -> pd.DataFrame:
        """Phân tích doanh thu theo phương thức thanh toán"""
        df = self.df.copy()
        payment_col = self._find_column(df.columns, ['payment'])
        revenue_col = self._ensure_revenue_column(df)

        if not payment_col or not revenue_col:
            return pd.DataFrame()

        result = df.groupby(payment_col)[revenue_col].sum().reset_index()
        result.columns = ['Payment Method', 'Revenue']
        result = result.sort_values('Revenue', ascending=False)

        return result

    def average_order_value(self) -> float:
        """Tính giá trị trung bình của đơn hàng"""
        return self.total_revenue() / self.total_orders() if self.total_orders() > 0 else 0

    def profit_summary(self) -> dict:
        """Phân tích lợi nhuận tổng và biên lợi nhuận."""
        profit_col = self._find_column(self.df.columns, ['profit'])
        total_revenue = self.total_revenue()

        if not profit_col:
            return {'total_profit': 0.0, 'margin_pct': 0.0}

        total_profit = pd.to_numeric(self.df[profit_col], errors='coerce').fillna(0).sum()
        margin_pct = (total_profit / total_revenue * 100) if total_revenue else 0.0
        return {'total_profit': total_profit, 'margin_pct': margin_pct}

    def revenue_by_sales_channel(self) -> pd.DataFrame:
        """Phân tích doanh thu theo kênh bán hàng."""
        df = self.df.copy()
        channel_col = self._find_column(df.columns, ['sales_channel', 'channel'])
        revenue_col = self._ensure_revenue_column(df)
        if not channel_col or not revenue_col:
            return pd.DataFrame()

        result = df.groupby(channel_col)[revenue_col].sum().reset_index()
        result.columns = ['Sales Channel', 'Revenue']
        return result.sort_values('Revenue', ascending=False)


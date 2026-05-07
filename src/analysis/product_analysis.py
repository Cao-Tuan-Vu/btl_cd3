"""
Module để phân tích sản phẩm
"""
import pandas as pd
import numpy as np


class ProductAnalysis:
    """Lớp để phân tích sản phẩm"""

    def __init__(self, df: pd.DataFrame):
        """
        Khởi tạo ProductAnalysis

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame chứa dữ liệu đơn hàng
        """
        self.df = df.copy()

    def top_products_by_sales(self, top_n: int = 10) -> pd.DataFrame:
        """
        Lấy Top N sản phẩm bán chạy nhất

        Parameters:
        -----------
        top_n : int
            Số sản phẩm top

        Returns:
        --------
        pd.DataFrame
            Danh sách top sản phẩm theo số lượng bán
        """
        product_cols = [col for col in self.df.columns if 'product' in col.lower() or 'name' in col.lower()]
        qty_cols = [col for col in self.df.columns if 'quantity' in col.lower()]

        if not product_cols or not qty_cols:
            return pd.DataFrame()

        result = self.df.groupby(product_cols[0])[qty_cols[0]].sum().reset_index()
        result.columns = ['Product', 'Total_Quantity']
        result = result.sort_values('Total_Quantity', ascending=False).head(top_n)

        return result

    def top_products_by_revenue(self, top_n: int = 10) -> pd.DataFrame:
        """
        Lấy Top N sản phẩm có doanh thu cao nhất

        Parameters:
        -----------
        top_n : int
            Số sản phẩm top

        Returns:
        --------
        pd.DataFrame
            Danh sách top sản phẩm theo doanh thu
        """
        product_cols = [col for col in self.df.columns if 'product' in col.lower() or 'name' in col.lower()]
        revenue_cols = [col for col in self.df.columns if 'revenue' in col.lower()]

        # Nếu không có cột Revenue, tính từ Quantity * Price
        if not revenue_cols:
            qty_cols = [col for col in self.df.columns if 'quantity' in col.lower()]
            price_cols = [col for col in self.df.columns if 'price' in col.lower() and 'unit' in col.lower()]

            if qty_cols and price_cols:
                df = self.df.copy()
                df['revenue'] = df[qty_cols[0]] * df[price_cols[0]]
                revenue_cols = ['revenue']
            else:
                return pd.DataFrame()
        else:
            df = self.df

        if not product_cols:
            return pd.DataFrame()

        result = df.groupby(product_cols[0])[revenue_cols[0]].sum().reset_index()
        result.columns = ['Product', 'Revenue']
        result = result.sort_values('Revenue', ascending=False).head(top_n)

        return result

    def products_by_category(self) -> pd.DataFrame:
        """Phân tích số sản phẩm theo danh mục"""
        cat_cols = [col for col in self.df.columns if 'category' in col.lower()]
        qty_cols = [col for col in self.df.columns if 'quantity' in col.lower()]

        if not cat_cols or not qty_cols:
            return pd.DataFrame()

        result = self.df.groupby(cat_cols[0])[qty_cols[0]].sum().reset_index()
        result.columns = ['Category', 'Total_Quantity']
        result = result.sort_values('Total_Quantity', ascending=False)

        return result

    def average_product_price(self) -> float:
        """Tính giá trung bình của sản phẩm"""
        price_cols = [col for col in self.df.columns if 'price' in col.lower() and 'unit' in col.lower()]

        if price_cols:
            return self.df[price_cols[0]].mean()

        return 0

    def product_count(self) -> int:
        """Đếm số lượng sản phẩm độc lập"""
        product_cols = [col for col in self.df.columns if 'product' in col.lower() or 'name' in col.lower()]

        if product_cols:
            return self.df[product_cols[0]].nunique()

        return 0

    def sales_by_status(self) -> pd.DataFrame:
        """Phân tích doanh số theo trạng thái đơn hàng"""
        status_cols = [col for col in self.df.columns if 'status' in col.lower()]
        qty_cols = [col for col in self.df.columns if 'quantity' in col.lower()]

        if not status_cols or not qty_cols:
            return pd.DataFrame()

        result = self.df.groupby(status_cols[0])[qty_cols[0]].sum().reset_index()
        result.columns = ['Status', 'Total_Quantity']

        return result

    def average_rating_by_product(self) -> pd.DataFrame:
        """Tính average rating theo sản phẩm (nếu có dữ liệu rating)"""
        product_cols = [col for col in self.df.columns if 'product' in col.lower() or 'name' in col.lower()]
        rating_cols = [col for col in self.df.columns if 'rating' in col.lower() or 'star' in col.lower()]

        if not product_cols or not rating_cols:
            return pd.DataFrame()

        result = self.df.groupby(product_cols[0])[rating_cols[0]].mean().reset_index()
        result.columns = ['Product', 'Average_Rating']
        result = result.sort_values('Average_Rating', ascending=False)

        return result


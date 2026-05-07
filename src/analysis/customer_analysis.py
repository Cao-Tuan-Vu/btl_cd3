"""
Module để phân tích khách hàng
"""
import pandas as pd
import numpy as np


class CustomerAnalysis:
    """Lớp để phân tích khách hàng"""

    def __init__(self, df: pd.DataFrame):
        """
        Khởi tạo CustomerAnalysis

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame chứa dữ liệu đơn hàng
        """
        self.df = df.copy()

    def total_customers(self) -> int:
        """Đếm tổng số khách hàng"""
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower()]

        if customer_cols:
            return self.df[customer_cols[0]].nunique()

        return len(self.df)

    def customer_per_region(self) -> pd.DataFrame:
        """Phân tích số khách hàng theo khu vực"""
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower()]
        region_cols = [col for col in self.df.columns if 'region' in col.lower()]

        if not customer_cols or not region_cols:
            return pd.DataFrame()

        result = self.df.groupby(region_cols[0])[customer_cols[0]].nunique().reset_index()
        result.columns = ['Region', 'Customer_Count']
        result = result.sort_values('Customer_Count', ascending=False)

        return result

    def repeat_customers(self) -> int:
        """Đếm số khách hàng mua lại"""
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower()]

        if not customer_cols:
            return 0

        customer_counts = self.df[customer_cols[0]].value_counts()
        return (customer_counts > 1).sum()

    def customer_lifetime_value(self) -> float:
        """Tính giá trị vòng đời trung bình của khách hàng"""
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower()]
        revenue_cols = [col for col in self.df.columns if 'revenue' in col.lower()]

        if not customer_cols or not revenue_cols:
            return 0

        customer_revenue = self.df.groupby(customer_cols[0])[revenue_cols[0]].sum()
        return customer_revenue.mean()

    def orders_per_customer(self) -> float:
        """Tính số đơn hàng trung bình trên mỗi khách hàng"""
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower()]

        if not customer_cols:
            return 0

        total_orders = len(self.df)
        total_customers = self.df[customer_cols[0]].nunique()

        return total_orders / total_customers if total_customers > 0 else 0

    def customers_by_category_preference(self) -> pd.DataFrame:
        """Phân tích sở thích danh mục của khách hàng"""
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower()]
        cat_cols = [col for col in self.df.columns if 'category' in col.lower()]

        if not customer_cols or not cat_cols:
            return pd.DataFrame()

        result = self.df.groupby([customer_cols[0], cat_cols[0]]).size().reset_index(name='Purchase_Count')
        result = result.sort_values(['Purchase_Count'], ascending=False).head(20)

        return result

    def top_customers_by_spending(self, top_n: int = 10) -> pd.DataFrame:
        """Lấy Top N khách hàng chi tiêu nhiều nhất"""
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower()]
        revenue_cols = [col for col in self.df.columns if 'revenue' in col.lower()]

        if not customer_cols or not revenue_cols:
            return pd.DataFrame()

        result = self.df.groupby(customer_cols[0])[revenue_cols[0]].sum().reset_index()
        result.columns = ['Customer', 'Total_Spending']
        result = result.sort_values('Total_Spending', ascending=False).head(top_n)

        return result

    def customer_acquisition_trend(self) -> pd.DataFrame:
        """Phân tích xu hướng thu hoạch khách hàng mới"""
        customer_cols = [col for col in self.df.columns if 'customer' in col.lower()]
        date_cols = [col for col in self.df.columns if 'date' in col.lower()]

        if not customer_cols or not date_cols:
            return pd.DataFrame()

        # Tính khách hàng mới theo ngày (khách hàng lần đầu tiên xuất hiện)
        df = self.df.copy()
        df['date'] = pd.to_datetime(df[date_cols[0]]).dt.date
        df = df.sort_values('date')

        # Tìm ngày đầu tiên của mỗi khách hàng
        first_purchase = df.groupby(customer_cols[0])['date'].min().reset_index()

        result = first_purchase.groupby('date').size().reset_index(name='New_Customers')
        result.columns = ['Date', 'New_Customers']

        return result


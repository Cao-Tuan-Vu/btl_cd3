"""
Module để dự báo doanh thu và số đơn hàng bằng Prophet
"""
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.plot import plot_components_plotly
import warnings
warnings.filterwarnings('ignore')


class DataForecaster:
    """Lớp để dự báo dữ liệu bằng Prophet"""

    def __init__(self, df: pd.DataFrame, date_column: str, value_column: str):
        """
        Khởi tạo Forecaster

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame chứa dữ liệu
        date_column : str
            Tên cột ngày
        value_column : str
            Tên cột giá trị cần dự báo
        """
        self.df = df.copy()
        self.date_column = date_column
        self.value_column = value_column
        self.model = None
        self.forecast = None

    def prepare_data(self) -> pd.DataFrame:
        """Chuẩn bị dữ liệu cho Prophet"""
        # Nhóm dữ liệu theo ngày và tính tổng
        working_df = self.df.copy()
        working_df[self.date_column] = pd.to_datetime(working_df[self.date_column], errors='coerce')
        working_df[self.value_column] = pd.to_numeric(working_df[self.value_column], errors='coerce')
        working_df = working_df.dropna(subset=[self.date_column, self.value_column])
        prepared = working_df.groupby(self.date_column)[self.value_column].sum().reset_index()
        prepared.columns = ['ds', 'y']
        prepared['ds'] = pd.to_datetime(prepared['ds'])
        prepared = prepared.sort_values('ds')

        return prepared

    def train(self):
        """Huấn luyện mô hình Prophet"""
        try:
            prepared_data = self.prepare_data()
            if len(prepared_data) < 10:
                raise ValueError("Dữ liệu quá ít để huấn luyện Prophet (cần >= 10 mốc thời gian).")

            # Tạo và huấn luyện mô hình
            self.model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=True,
                daily_seasonality=False,
                interval_width=0.95
            )

            self.model.fit(prepared_data)
            return True
        except Exception as e:
            print(f"Lỗi khi huấn luyện mô hình: {str(e)}")
            return False

    def forecast_days(self, periods: int = 30) -> pd.DataFrame:
        """
        Dự báo cho N ngày tiếp theo

        Parameters:
        -----------
        periods : int
            Số ngày cần dự báo

        Returns:
        --------
        pd.DataFrame
            Dữ liệu dự báo
        """
        if self.model is None:
            self.train()

        future = self.model.make_future_dataframe(periods=periods)
        self.forecast = self.model.predict(future)

        return self.forecast

    def forecast_months(self, periods: int = 12) -> pd.DataFrame:
        """
        Dự báo cho N tháng tiếp theo

        Parameters:
        -----------
        periods : int
            Số tháng cần dự báo

        Returns:
        --------
        pd.DataFrame
            Dữ liệu dự báo
        """
        if self.model is None:
            self.train()

        future = self.model.make_future_dataframe(periods=periods, freq='MS')
        self.forecast = self.model.predict(future)
        return self.forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    def get_components(self):
        """
        Lấy các thành phần của mô hình (trend, seasonality, etc.)

        Returns:
        --------
        dict
            Các thành phần
        """
        if self.model is None or self.forecast is None:
            return None

        return plot_components_plotly(self.model, self.forecast)

    def get_metrics(self) -> dict:
        """Lấy các chỉ số hiệu quả của mô hình"""
        if self.forecast is None:
            return {}

        # Tính MAPE (Mean Absolute Percentage Error)
        prepared = self.prepare_data()

        # Chỉ tính trên dữ liệu gốc (không phải dự báo)
        forecast_train = self.forecast[self.forecast['ds'].isin(prepared['ds'])]

        if len(forecast_train) > 0:
            actual = prepared['y'].values
            predicted = forecast_train['yhat'].values
            non_zero_mask = actual != 0
            if non_zero_mask.any():
                mape = np.mean(np.abs((actual[non_zero_mask] - predicted[non_zero_mask]) / actual[non_zero_mask])) * 100
            else:
                mape = 0
        else:
            mape = 0

        return {
            'mape': mape,
            'data_points': len(prepared)
        }


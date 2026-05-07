"""
Module để làm sạch dữ liệu
"""
import pandas as pd
import numpy as np
from datetime import datetime


class DataCleaner:
    """Lớp để làm sạch dữ liệu tự động"""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_rows = len(df)
        self.cleaning_report = {}
        self.date_columns = []

    @staticmethod
    def _parse_numeric_series(series: pd.Series) -> pd.Series:
        """Chuẩn hóa text số (có dấu phẩy, ký hiệu tiền) thành numeric."""
        if pd.api.types.is_numeric_dtype(series):
            return pd.to_numeric(series, errors='coerce')

        cleaned = (
            series.astype(str)
            .str.replace(r'[^\d\-\.,]', '', regex=True)
            .str.replace(',', '', regex=False)
            .replace({'': np.nan, 'nan': np.nan, 'None': np.nan})
        )
        return pd.to_numeric(cleaned, errors='coerce')

    def clean(self) -> pd.DataFrame:
        """
        Thực hiện các bước làm sạch dữ liệu

        Returns:
        --------
        pd.DataFrame
            DataFrame sau khi được làm sạch
        """
        self.remove_duplicates()
        self.handle_missing_values()
        self.standardize_datetime()
        self.convert_numeric_types()
        self.remove_invalid_data()

        return self.df

    def remove_duplicates(self):
        """Xóa các dòng trùng lặp"""
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        removed = initial_rows - len(self.df)
        self.cleaning_report['duplicates_removed'] = removed

    def handle_missing_values(self):
        """Xử lý các giá trị NULL/NaN"""
        initial_missing = self.df.isnull().sum().sum()

        for col in self.df.columns:
            if pd.api.types.is_numeric_dtype(self.df[col]):
                if self.df[col].isnull().sum() > 0:
                    self.df[col] = self.df[col].fillna(self.df[col].median())
            elif pd.api.types.is_datetime64_any_dtype(self.df[col]):
                # Cột ngày sẽ xử lý riêng ở remove_invalid_data.
                continue
            else:
                self.df[col] = self.df[col].fillna('Unknown')
                self.df[col] = self.df[col].replace({'': 'Unknown', 'nan': 'Unknown', 'None': 'Unknown'})

        self.cleaning_report['null_values_filled'] = initial_missing

    def standardize_datetime(self):
        """Chuẩn hóa các cột ngày tháng"""
        standardized_cols = 0
        for col in self.df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                    self.date_columns.append(col)
                    standardized_cols += 1
                except Exception:
                    pass

        self.cleaning_report['datetime_standardized_columns'] = standardized_cols

    def convert_numeric_types(self):
        """Chuyển đổi kiểu dữ liệu số"""
        converted_cols = 0
        for col in self.df.columns:
            # Cố gắng chuyển đổi sang kiểu số nếu có thể
            if any(key in col.lower() for key in ['price', 'cost', 'revenue', 'profit', 'amount', 'discount']):
                try:
                    self.df[col] = self._parse_numeric_series(self.df[col])
                    converted_cols += 1
                except Exception:
                    pass

            if 'quantity' in col.lower() or 'count' in col.lower():
                try:
                    parsed = self._parse_numeric_series(self.df[col]).fillna(0)
                    self.df[col] = parsed.clip(lower=0).round().astype(int)
                    converted_cols += 1
                except Exception:
                    pass

        self.cleaning_report['numeric_converted_columns'] = converted_cols

    def remove_invalid_data(self):
        """Loại bỏ dữ liệu lỗi"""
        initial_rows = len(self.df)

        # Loại bỏ dòng có ngày không hợp lệ sau chuẩn hóa.
        for date_col in self.date_columns:
            self.df = self.df[self.df[date_col].notna()]

        # Loại bỏ các dòng có số tiền âm
        for col in self.df.columns:
            if any(word in col.lower() for word in ['price', 'cost', 'revenue', 'profit']):
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df = self.df[self.df[col] >= 0]

        # Loại bỏ các dòng có số lượng âm
        for col in self.df.columns:
            if 'quantity' in col.lower():
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    self.df = self.df[self.df[col] > 0]

        removed = initial_rows - len(self.df)
        self.cleaning_report['invalid_rows_removed'] = removed

    def get_report(self) -> dict:
        """Lấy thông tin chi tiết về quá trình làm sạch"""
        return {
            **self.cleaning_report,
            'original_rows': self.original_rows,
            'final_rows': len(self.df),
            'total_rows_removed': self.original_rows - len(self.df)
        }


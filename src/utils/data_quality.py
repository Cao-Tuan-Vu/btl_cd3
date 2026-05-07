"""
Module để đánh giá chất lượng dữ liệu
"""
import pandas as pd
import numpy as np


class DataQualityAssessment:
    """Lớp để đánh giá chất lượng dữ liệu"""

    def __init__(self, df: pd.DataFrame):
        """
        Khởi tạo DataQualityAssessment

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame chứa dữ liệu
        """
        self.df = df.copy()

    def get_overall_quality_score(self) -> float:
        """
        Tính điểm chất lượng dữ liệu tổng thể (0-100)

        Returns:
        --------
        float
            Điểm chất lượng (0-100)
        """
        scores = []

        # 1. Tỷ lệ dữ liệu đầy đủ
        completeness = (1 - self.df.isnull().sum().sum() / (len(self.df) * len(self.df.columns))) * 100
        scores.append(completeness * 0.3)

        # 2. Tỷ lệ bản ghi không trùng lặp
        duplicate_ratio = (1 - (len(self.df) - len(self.df.drop_duplicates())) / len(self.df)) * 100
        scores.append(duplicate_ratio * 0.3)

        # 3. Kiểm tra kiểu dữ liệu hợp lý
        type_score = self._check_data_types_validity() * 100
        scores.append(type_score * 0.4)

        return min(100, sum(scores))

    def _check_data_types_validity(self) -> float:
        """Kiểm tra tỷ lệ dữ liệu có kiểu hợp lý"""
        valid_count = 0

        for col in self.df.columns:
            # Kiểm tra số cột
            if any(key in col.lower() for key in ['price', 'cost', 'revenue', 'profit', 'quantity']):
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    valid_count += 1
                else:
                    # Thử chuyển đổi
                    try:
                        pd.to_numeric(self.df[col], errors='coerce')
                        valid_count += 0.8
                    except:
                        pass
            # Kiểm tra ngày cột
            elif any(key in col.lower() for key in ['date', 'time']):
                if pd.api.types.is_datetime64_any_dtype(self.df[col]):
                    valid_count += 1
                else:
                    try:
                        pd.to_datetime(self.df[col], errors='coerce')
                        valid_count += 0.8
                    except:
                        pass
            else:
                valid_count += 1

        return valid_count / len(self.df.columns) if len(self.df.columns) > 0 else 0

    def get_completeness_report(self) -> pd.DataFrame:
        """
        Lấy báo cáo tỷ lệ dữ liệu đầy đủ theo cột

        Returns:
        --------
        pd.DataFrame
            Báo cáo completeness
        """
        missing_data = self.df.isnull().sum()
        total_rows = len(self.df)

        report = pd.DataFrame({
            'Cột': self.df.columns,
            'Giá Trị Thiếu': missing_data.values,
            'Tỷ Lệ Thiếu (%)': (missing_data.values / total_rows * 100).round(2),
            'Tỷ Lệ Đầy Đủ (%)': ((total_rows - missing_data.values) / total_rows * 100).round(2)
        })

        return report.sort_values('Tỷ Lệ Thiếu (%)', ascending=False)

    def get_duplicates_report(self) -> dict:
        """
        Lấy báo cáo về bản ghi trùng lặp

        Returns:
        --------
        dict
            Báo cáo trùng lặp
        """
        total_rows = len(self.df)
        duplicate_rows = len(self.df) - len(self.df.drop_duplicates())
        duplicate_percentage = (duplicate_rows / total_rows * 100) if total_rows > 0 else 0

        # Kiểm tra trùng lặp theo cột
        column_duplicates = {}
        for col in self.df.columns:
            dup_count = total_rows - self.df[col].nunique()
            if dup_count > 0:
                column_duplicates[col] = {
                    'Trùng Lặp': dup_count,
                    'Tỷ Lệ (%)': round(dup_count / total_rows * 100, 2)
                }

        return {
            'Tổng Bản Ghi Trùng Lặp': duplicate_rows,
            'Tỷ Lệ Trùng Lặp (%)': round(duplicate_percentage, 2),
            'Chi Tiết Theo Cột': column_duplicates
        }

    def get_outliers_report(self) -> pd.DataFrame:
        """
        Lấy báo cáo về giá trị ngoại lệ (outliers)

        Returns:
        --------
        pd.DataFrame
            Báo cáo ngoại lệ
        """
        outlier_report = []

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outlier_count = len(self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)])
            outlier_percentage = (outlier_count / len(self.df) * 100) if len(self.df) > 0 else 0

            if outlier_count > 0:
                outlier_report.append({
                    'Cột': col,
                    'Số Ngoại Lệ': outlier_count,
                    'Tỷ Lệ (%)': round(outlier_percentage, 2),
                    'Min': self.df[col].min(),
                    'Max': self.df[col].max(),
                    'Trung Bình': round(self.df[col].mean(), 2)
                })

        if outlier_report:
            return pd.DataFrame(outlier_report).sort_values('Tỷ Lệ (%)', ascending=False)
        else:
            return pd.DataFrame()

    def get_statistical_summary(self) -> pd.DataFrame:
        """
        Lấy thống kê mô tả dữ liệu

        Returns:
        --------
        pd.DataFrame
            Thống kê mô tả
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns

        if len(numeric_cols) == 0:
            return pd.DataFrame()

        summary = self.df[numeric_cols].describe().T
        summary['Không Null'] = self.df[numeric_cols].notna().sum().values
        summary['Null Count'] = self.df[numeric_cols].isnull().sum().values

        return summary

    def get_value_distribution(self, column: str, top_n: int = 10) -> pd.DataFrame:
        """
        Lấy phân phối giá trị của một cột

        Parameters:
        -----------
        column : str
            Tên cột
        top_n : int
            Số giá trị top

        Returns:
        --------
        pd.DataFrame
            Phân phối giá trị
        """
        if column not in self.df.columns:
            return pd.DataFrame()

        value_counts = self.df[column].value_counts().head(top_n)
        total = len(self.df)

        distribution = pd.DataFrame({
            'Giá Trị': value_counts.index,
            'Số Lần': value_counts.values,
            'Tỷ Lệ (%)': (value_counts.values / total * 100).round(2)
        }).reset_index(drop=True)

        return distribution

    def get_data_quality_metrics(self) -> dict:
        """
        Lấy tất cả các chỉ số chất lượng dữ liệu

        Returns:
        --------
        dict
            Các chỉ số chất lượng
        """
        total_rows = len(self.df)
        total_cols = len(self.df.columns)
        total_cells = total_rows * total_cols

        missing_cells = self.df.isnull().sum().sum()
        missing_percentage = (missing_cells / total_cells * 100) if total_cells > 0 else 0

        duplicate_rows = len(self.df) - len(self.df.drop_duplicates())

        return {
            'Tổng Dòng': total_rows,
            'Tổng Cột': total_cols,
            'Tổng Ô Dữ Liệu': total_cells,
            'Ô Thiếu Dữ Liệu': missing_cells,
            'Tỷ Lệ Thiếu (%)': round(missing_percentage, 2),
            'Bản Ghi Trùng Lặp': duplicate_rows,
            'Tỷ Lệ Trùng Lặp (%)': round((duplicate_rows / total_rows * 100) if total_rows > 0 else 0, 2),
            'Điểm Chất Lượng': round(self.get_overall_quality_score(), 2)
        }

    def get_detailed_quality_assessment(self) -> dict:
        """
        Lấy báo cáo đánh giá chất lượng chi tiết

        Returns:
        --------
        dict
            Báo cáo chi tiết
        """
        return {
            'Overall Metrics': self.get_data_quality_metrics(),
            'Completeness': self.get_completeness_report(),
            'Duplicates': self.get_duplicates_report(),
            'Outliers': self.get_outliers_report(),
            'Statistics': self.get_statistical_summary()
        }


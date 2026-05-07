"""
Module để đọc và xử lý dữ liệu từ CSV/Excel
"""
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


class DataLoader:
    """Lớp để đọc dữ liệu từ file CSV/Excel"""

    @staticmethod
    def load_file(file) -> pd.DataFrame:
        """
        Đọc dữ liệu từ file CSV hoặc Excel

        Parameters:
        -----------
        file : UploadedFile
            File được upload

        Returns:
        --------
        pd.DataFrame
            DataFrame chứa dữ liệu
        """
        try:
            if file is None:
                st.error("❌ Chưa có file được upload")
                return None

            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                st.error("❌ Định dạng file không được hỗ trợ. Vui lòng upload CSV hoặc XLSX")
                return None

            if df.empty:
                st.error("❌ File dữ liệu rỗng")
                return None

            # Chuẩn hóa tên cột để tránh lỗi do khoảng trắng thừa.
            df.columns = [str(col).strip() for col in df.columns]

            if len(df.columns) != len(set(df.columns)):
                st.error("❌ File có tên cột bị trùng lặp. Vui lòng kiểm tra lại.")
                return None

            return df
        except Exception as e:
            st.error(f"❌ Lỗi khi đọc file: {str(e)}")
            return None

    @staticmethod
    def get_file_info(df: pd.DataFrame) -> dict:
        """
        Lấy thông tin chi tiết về file

        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame

        Returns:
        --------
        dict
            Thông tin về file (số dòng, cột, kiểu dữ liệu, etc.)
        """
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
        }


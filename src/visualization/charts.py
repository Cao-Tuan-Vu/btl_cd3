"""
Module để tạo các biểu đồ visualizations
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


class ChartGenerator:
    """Lớp để tạo các biểu đồ"""

    @staticmethod
    def bar_chart(data: pd.DataFrame, x: str, y: str, title: str, color: str = None):
        """Tạo biểu đồ cột"""
        fig = px.bar(
            data,
            x=x,
            y=y,
            title=title,
            color=color,
            template='plotly_white'
        )
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16,
            hovermode='x unified'
        )
        return fig

    @staticmethod
    def line_chart(data: pd.DataFrame, x: str, y: str, title: str):
        """Tạo biểu đồ đường"""
        fig = px.line(
            data,
            x=x,
            y=y,
            title=title,
            template='plotly_white',
            markers=True
        )
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16,
            hovermode='x unified'
        )
        return fig

    @staticmethod
    def pie_chart(data: pd.DataFrame, values: str, names: str, title: str):
        """Tạo biểu đồ tròn"""
        fig = px.pie(
            data,
            values=values,
            names=names,
            title=title,
            template='plotly_white'
        )
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16
        )
        return fig

    @staticmethod
    def scatter_chart(data: pd.DataFrame, x: str, y: str, size: str = None,
                     color: str = None, title: str = "Scatter Plot"):
        """Tạo biểu đồ scatter"""
        fig = px.scatter(
            data,
            x=x,
            y=y,
            size=size,
            color=color,
            title=title,
            template='plotly_white'
        )
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16,
            hovermode='closest'
        )
        return fig

    @staticmethod
    def area_chart(data: pd.DataFrame, x: str, y: str, title: str):
        """Tạo biểu đồ diện tích"""
        fig = px.area(
            data,
            x=x,
            y=y,
            title=title,
            template='plotly_white'
        )
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16,
            hovermode='x unified'
        )
        return fig

    @staticmethod
    def heatmap_chart(data: pd.DataFrame, title: str = "Heatmap"):
        """Tạo biểu đồ heatmap"""
        # Tính correlation matrix
        numeric_data = data.select_dtypes(include=[np.number])
        corr_matrix = numeric_data.corr()

        fig = px.imshow(
            corr_matrix,
            labels=dict(x="Features", y="Features", color="Correlation"),
            title=title,
            color_continuous_scale='RdBu',
            zmin=-1, zmax=1
        )
        fig.update_layout(
            height=600,
            font=dict(size=12),
            title_font_size=16
        )
        return fig

    @staticmethod
    def histogram_chart(data: pd.DataFrame, x: str, title: str, nbins: int = 30):
        """Tạo biểu đồ histogram"""
        fig = px.histogram(
            data,
            x=x,
            title=title,
            nbins=nbins,
            template='plotly_white'
        )
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16,
            hovermode='x unified'
        )
        return fig

    @staticmethod
    def box_plot(data: pd.DataFrame, x: str, y: str, title: str):
        """Tạo biểu đồ box plot"""
        fig = px.box(
            data,
            x=x,
            y=y,
            title=title,
            template='plotly_white'
        )
        fig.update_layout(
            height=500,
            font=dict(size=12),
            title_font_size=16
        )
        return fig

    @staticmethod
    def sunburst_chart(data: pd.DataFrame, labels: str, parents: str,
                       values: str, title: str):
        """Tạo biểu đồ sunburst"""
        fig = px.sunburst(
            data,
            labels=labels,
            parents=parents,
            values=values,
            title=title,
            template='plotly_white'
        )
        fig.update_layout(
            height=600,
            font=dict(size=12),
            title_font_size=16
        )
        return fig

    @staticmethod
    def multi_line_chart(data: pd.DataFrame, x: str, y: list, title: str):
        """Tạo biểu đồ đường với nhiều đường"""
        fig = go.Figure()

        for col in y:
            fig.add_trace(go.Scatter(
                x=data[x],
                y=data[col],
                mode='lines+markers',
                name=col
            ))

        fig.update_layout(
            title=title,
            xaxis_title=x,
            yaxis_title="Value",
            height=500,
            template='plotly_white',
            hovermode='x unified',
            font=dict(size=12),
            title_font_size=16
        )

        return fig


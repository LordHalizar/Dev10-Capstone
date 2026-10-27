import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

from dash import dcc


class Graphs:
    def __init__(self, df: pd.DataFrame, region_mapping: dict[str, tuple[str, str]], x_column, x_label):
        self.df = df 
        self.region_mapping = region_mapping
    def multi_region_dropdown_graph(
            self, 
            selected_multi: list[str],
            selected_region: list[str], 
            multi_mapping: dict[str, str],
            title_context: str
    ) -> dcc.Figure:

        if not selected_multi:
            return px.line(title=f"Select at least one {multi_mapping['context']}.")

        column, label = self.region_mapping.get(selected_region, (None, None))

        if column is None:
            return px.line(title="Select a valid region.")

        data = self.df[
            self.df[multi_mapping['option']].isin(selected_multi)
        ]

        fig = px.line(
            data_frame=data,
            x=x_axis_mapping['column'],
            y=column,
            color=multi_mapping['option'],
            labels={
                x_axis_mapping['column']: x_axis_mapping['label'],
                column: label,
                multi_mapping['option']: multi_mapping['option'].replace('_', ' ').title(),
            },
            title=f"{label} {title_context}"
        )

        return fig
    
    def update_combined_layout(self):
        pass
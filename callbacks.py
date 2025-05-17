from dash import Input, Output, dcc
import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'x': list(range(1, 11)),
    'y': [2, 5, 1, 6, 9, 4, 7, 3, 8, 10],
    'category': ['A', 'B'] * 5
})

def register_callbacks(app):

    @app.callback(
        Output('text-output', 'children'),
        Input('user-input', 'value')
    )
    def update_text_output(value):
        if value:
            return f"Plot title will be: {value}"
        return "Plot title will use the default."

    @app.callback(
        Output('plots-container', 'children'),
        Input('plot-selector', 'value'),
        Input('user-input', 'value')
    )
    def update_plots(plot_type, title_input):
        plot_title = title_input if title_input else "Default Plot Title"

        if plot_type == 'line':
            main_fig = px.line(df, x='x', y='y', title=plot_title)
        elif plot_type == 'bar':
            main_fig = px.bar(df, x='x', y='y', title=plot_title)
        elif plot_type in ['scatter', 'scatter_with_extra']:
            main_fig = px.scatter(df, x='x', y='y', color='category', title=plot_title)
        else:
            main_fig = {}

        children = [dcc.Graph(figure=main_fig, id='main-graph')]

        if plot_type == 'scatter_with_extra':
            extra_fig = px.bar(df, x='category', y='y', title=f"{plot_title} - Extra Plot")
            children.append(dcc.Graph(figure=extra_fig, id='extra-graph'))

        return children

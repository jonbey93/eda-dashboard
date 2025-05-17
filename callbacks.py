from dash import Input, Output, State, html, dcc
import plotly.express as px
import pandas as pd
from utils.parse import parse_csv

df_global = pd.DataFrame()

# Sample DataFrame for testing
df_test = pd.DataFrame({
        'x': list(range(1, 11)),
        'y': [2, 5, 1, 6, 9, 4, 7, 3, 8, 10],
        'category': ['A', 'B'] * 5
})

def register_callbacks(app):

    # Callback for the textarea input
    @app.callback(
        Output('text-output', 'children'),
        Input('run-query', 'n_clicks'),
        State('user-prompt', 'value')
    )
    def update_text_output(n_clicks, value):
        if n_clicks > 0 and value:
            return f"You typed: \"{value}\""
        return "Type something..."

    # Callback for the upload component
    @app.callback(
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents')
    )
    def update_upload(contents):
        global df_global
        if contents:
            df_global = parse_csv(contents)
            columns_list = [html.Li(col) for col in df_global.columns]
            return html.Div([
                html.H5("Registred Features:"),
                html.Ul(columns_list)
            ])

    # Callback for the plot type dropdown and user input
    @app.callback(
        Output('plots-container', 'children'),
        Input('plot-selector', 'value'),
    )
    def update_plots(plot_type):
        if plot_type == 'line':
            main_fig = px.line(df_test, x='x', y='y')
        elif plot_type == 'bar':
            main_fig = px.bar(df_test, x='x', y='y')
        elif plot_type in ['scatter', 'scatter_with_extra']:
            main_fig = px.scatter(df_test, x='x', y='y', color='category')
        else:
            main_fig = {}

        children = [dcc.Graph(figure=main_fig, id='main-graph')]

        if plot_type == 'scatter_with_extra':
            extra_fig = px.bar(df_test, x='category', y='y')
            children.append(dcc.Graph(figure=extra_fig, id='extra-graph'))

        return children

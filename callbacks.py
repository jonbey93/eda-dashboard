from dash import Input, Output, State, html, dcc
import plotly.express as px
import pandas as pd
from utils.parse import parse_csv
from utils.llm import query_llm

df_global = pd.DataFrame()
columns_list_global = []

# Sample DataFrame for testing
df_test = pd.DataFrame({
        'x': list(range(1, 11)),
        'y': [2, 5, 1, 6, 9, 4, 7, 3, 8, 10],
        'category': ['A', 'B'] * 5
})

def register_callbacks(app):

    # Callback for the LLM-Textarea input
    @app.callback(
        Output('llm-response', 'value'),
        Input('run-query', 'n_clicks'),
        State('user-prompt', 'value'),
        State('columns-store', 'data'),
        State('data-sample-store', 'data'),
    )
    def run_llm_query(n_clicks, user_message, columns, data_sample):
        if n_clicks > 0 and user_message:
            response = query_llm(user_message, columns, data_sample)
            if response:
                return response
            else:
                return "Error: No response from LLM."

    # Callback for the copy button
    app.clientside_callback(
        """
        function(n_clicks) {
            if (n_clicks > 0) {
                const textarea = document.getElementById('llm-response');
                if (textarea) {
                    textarea.select();
                    document.execCommand('copy');
                }
            }
            return '';
        }
        """,
        Output('dummy-output', 'children'),
        Input('copy-button', 'n_clicks')
    )
    @app.callback(
    Output('copy-feedback', 'children'),
    Input('copy-button', 'n_clicks'),
    prevent_initial_call=True
    )
    def show_copy_feedback(n):
        return "Copied!"

    # Callback for the upload component
    @app.callback(
        Output('columns-store', 'data'),
        Output('data-sample-store', 'data'),
        Output('output-data-upload', 'children'),
        Input('upload-data', 'contents')
    )
    def update_upload(contents):
        global df_global, columns_list_global
        if contents:
            df_global = parse_csv(contents)
            columns_list_global = df_global.columns.tolist()
            sample_row = df_global.iloc[0].to_dict()
            
            columns_list_html = [html.Li(col) for col in columns_list_global]
            data_sample = str({
                col: f"{sample_row[col]}, dtype={df_global[col].dtype}"
                for col in columns_list_global
                })

            return columns_list_global, data_sample, html.Div([
                html.H5("Registred Features:"),
                html.Ul(columns_list_html)
            ])
        
        columns_list_global = ['colA', 'colB', 'colC']
        data_sample = str({
            'colA': '2, dtype=int32',
            'colB': '3, dtype=int32',
            'colC': '4, dtype=int32'
        })
        
        columns_list_html = [html.Li(col) for col in columns_list_global]

        return columns_list_global, data_sample, html.Div([
            html.H5("Registred Features:"),
            html.Ul(columns_list_html)
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

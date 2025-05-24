import uuid
from dash import no_update, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.parse import parse_csv
from utils.llm import query_llm

df_global = pd.DataFrame()
columns_list_global = []

def register_callbacks(app):

    # Callback for the user input field
    @app.callback(
        Output('plots-store', 'data'),
        Output('llm-response', 'value'),
        Input('run-query', 'n_clicks'),
        State('user-prompt', 'value'),
        State('columns-store', 'data'),
        State('data-sample-store', 'data'),
        State('plots-store', 'data'),
        prevent_initial_call=True
    )
    def run_llm_query(n_clicks,
                      user_message,
                      columns,
                      data_sample,
                      existing_plots):
        if not user_message:
            return no_update, "Error: No user message provided."
        response = query_llm(user_message, columns, data_sample)
        if not response:
            return no_update, "Error: No response from LLM."    

        local_context = {}
        global_context = {'plt': plt,
                          'pd': pd,
                          'px': px,
                          'go': go,
                          'df_global': df_global}
        try:    # Execute the LLM response
            exec(response, global_context, local_context)
            fig = local_context.get("fig")
            if fig is None:
                return no_update, "Error: LLM did not return a figure." + "\n\nGenerated Code:\n" + response
            try:    # Convert fig to JSON-serializable dict
                fig_dict = fig.to_dict()
                plot_id = str(uuid.uuid4())
                new_plot = {'id': plot_id,
                            'figure': fig_dict,
                            'code': response,
                            'pinned': False}
            except Exception as e:
                return no_update, f"Error: Failed to convert figure to JSON. {str(e)}"
            return [new_plot] + existing_plots, f"Success! Plot generated. \n\n{response}"
        except Exception as e:
            return no_update, f"Execution error: \n\n{str(e)}\n\n{response}"

    # Callback for the plots container
    @app.callback(
    Output('plots-container', 'children'),
    Input('plots-store', 'data')
    )
    def render_plots(plots):
        if not plots:
            return html.Div("No plots yet.")

        return [
            html.Div([
                dcc.Graph(figure=go.Figure(plot['figure']), id=f"plot-{plot['id']}"),
                html.Button("Pin", id={'type': 'pin-btn', 'index': plot['id']}),
                html.Hr()
            ], style={'marginBottom': '20px'}) for plot in plots
        ]

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

    # Callback for handling data upload, including features table
    @app.callback(
        Output('columns-store', 'data'),
        Output('data-sample-store', 'data'),
        Output('features-table', 'children'),
        Output('upload-status', 'data'),
        Input('upload-data', 'contents')
    )
    def update_upload(contents):
        global df_global, columns_list_global
        if contents:
            df_global = parse_csv(contents)
            columns_list_global = df_global.columns.tolist()
            sample_row = df_global.iloc[0]

            # Prepare data rows for the table: column name and dtype
            table_rows = []
            for col in columns_list_global:
                dtype = df_global[col].dtype
                table_rows.append(html.Tr([
                    html.Td(col),
                    html.Td(str(dtype))
                ]))

            table = dbc.Table(
                # Header row
                [html.Thead(html.Tr([html.Th("Feature"), html.Th("Dtype")]))] +
                [html.Tbody(table_rows)],
                bordered=True,
                hover=True,
                responsive=True,
                striped=True,
                size='sm',
                style={'marginTop': '20px'}
            )

            return columns_list_global, str(sample_row.to_dict()), html.Div([table]), True

        # Default case: show some dummy data as table
        columns_list_global = ['colA', 'colB', 'colC']
        dummy_data = {
            'A': (2, '--'),
            'B': (3, '--'),
            'C': (4, '--')
        }

        table_rows = [html.Tr([html.Td(k), html.Td(v[1])]) for k, v in dummy_data.items()]

        table = dbc.Table(
            [html.Thead(html.Tr([html.Th("Feature"), html.Th("Dtype")]))] +
            [html.Tbody(table_rows)],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            size='sm',
            style={'marginTop': '20px'}
        )

        data_sample = str({k: f"{v[0]}, dtype={v[1]}" for k, v in dummy_data.items()})

        return columns_list_global, data_sample, html.Div([table]), False

    # Callback for updating upload box style
    @app.callback(
    Output('upload-prompt', 'children'),
    Output('upload-data', 'style'),
    Input('upload-status', 'data'),
    State('upload-data', 'filename'),
    )
    def update_upload_ui(succes, filename):
        if succes:
            return [f'{filename}'], {
                'width': '100%', 'height': '100px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center',
                'backgroundColor': "#def3e3",
                'color': "#000000",
                'cursor': 'pointer'
            }
        return [html.A('Select CSV File')], {
        'width': '100%', 'height': '100px', 'lineHeight': '60px',
        'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
        'textAlign': 'center',
        'cursor': 'pointer'
        }
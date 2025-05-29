import uuid
from dash import no_update, html, ctx, ALL
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.logging import write_to_log
from utils.parse import parse_csv
from utils.llm import *
from components import *

df_global = pd.DataFrame()

def register_callbacks(app):
    # LLM interaction
    @app.callback(
        Output('openai-connect', 'data'),
        Input('startup-check', 'n_intervals')
    )
    def check_connection(_):
        setup_llm_client()
        return is_openai_connected()

    @app.callback(
        Output('llm-plot-store', 'data'),
        Output('llm-response', 'value'),
        Input('run-query', 'n_clicks'),
        State('user-prompt', 'value'),
        State('features-store', 'data'),
        State('data-sample-store', 'data'),
        prevent_initial_call=True,
    )
    def run_llm_query(n_clicks,
                      user_message,
                      features,
                      data_sample):
        if not user_message:
            return no_update, "Error: No user message provided."
        response = query_llm(user_message, features, data_sample)
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
                            'code': response}
            except Exception as e:
                return no_update, f"Error: Failed to convert figure to JSON. {str(e)}"
            return new_plot, f"Success! Plot generated. \n\n{response}"
        except Exception as e:
            return no_update, f"Execution error: \n\n{str(e)}\n\n{response}"

    @app.callback(
    Output('user-prompt', 'placeholder'),
    Output('user-prompt', 'disabled'),
    Output('run-query', 'disabled'),
    Output('llm-response', 'disabled'),
    Input('openai-connect', 'data'),
    )
    def toggle_chat_availability(openai_connected):
        if openai_connected:
            return 'Ask a question...', False, False, False
        return '⚠️ OpenAI connection not established.', True, True, True

    # Plot-store management
    @app.callback(
        Output('plots-store', 'data'),
        Input('llm-plot-store', 'data'),
        Input({'type': 'clear-btn', 'index': ALL}, 'n_clicks'),
        #Input({'type': 'view-code-btn', 'index': ALL}, 'n_clicks'),
        State('plots-store', 'data'),
        prevent_initial_call=True,
    )
    def manage_plots(new_plot, clear_clicks, existing_plots):
        trigger = ctx.triggered_id
        # Handle clear button clicks
        if isinstance(trigger, dict) and trigger['type'] == 'clear-btn':
            plot_id = trigger['index']
            updated_plots = [plot for plot in existing_plots if plot['id'] != plot_id]
            return updated_plots

        if not new_plot:
            return existing_plots
        return [new_plot] + existing_plots

    # Plot renderer
    @app.callback(
    Output('plots-container', 'children'),
    Input('plots-store', 'data'),
    )
    def render_plots(plots):
        if not plots:
            return html.Div("No plots yet.")
        write_to_log(f"{[plot['code'] for plot in plots]}")
        return [generate_plot_component(plot) for plot in plots]
    
    # View-code-button
    @app.callback(
        Output({'type': 'view-code-box-container', 'index': ALL}, 'style'),
        Input({'type': 'view-code-btn', 'index': ALL}, 'n_clicks'),
        State({'type': 'view-code-box-container', 'index': ALL}, 'style'),
        prevent_initial_call=True
    )
    def toggle_note_boxes(note_clicks, current_styles):
        new_styles = []
        for clicks, style in zip(note_clicks, current_styles):
            if clicks and clicks % 2 == 1:
                new_style = style.copy()
                new_style['display'] = 'block'
                new_styles.append(new_style)
            else:
                new_style = style.copy()
                new_style['display'] = 'none'
                new_styles.append(new_style)
        return new_styles

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
        Output('features-store', 'data'),
        Output('data-sample-store', 'data'),
        Output('features-table', 'children'),
        Output('upload-status', 'data'),
        Input('upload-data', 'contents')
    )
    def update_upload(contents):
        global df_global, feature_list_global
        if contents:
            df_global = parse_csv(contents)
            feature_list_global = df_global.columns.tolist()
            data_sample = str({col: (val, 'dtype: '+str(type(val).__name__)) for col, val in df_global.iloc[0].items()})
            table = generate_features_table(df_global)
            return feature_list_global, data_sample, html.Div([table]), True

        df_global = pd.DataFrame([{'A': 2, 'B': 3, 'C': 4}])
        feature_list_global = df_global.columns.tolist()
        data_sample = str({col: (val, 'dtype: '+str(type(val).__name__)) for col, val in df_global.iloc[0].items()})
        table = generate_features_table(df_global)
        return feature_list_global, data_sample, html.Div([table]), False

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
                'borderWidth': '1px', 'borderStyle': 'none', 'borderRadius': '5px',
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
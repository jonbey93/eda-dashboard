from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

def generate_plot_component(plot):
    return html.Div([
        dcc.Graph(figure=go.Figure(plot['figure']), id=f"plot-{plot['id']}"),
        html.Div([
            html.Button("*View Code*", id={'type': 'view-code-btn', 'index': plot['id']}),
            html.Button("Clear", id={'type': 'clear-btn', 'index': plot['id']}, style={'marginLeft': 'auto'}),
        ], style={'display': 'flex', 'marginTop': '10px'}),
        #html.Button("Clear", id={'type': 'clear-btn', 'index': plot['id']}, style={'marginLeft': '10px'}),
        #html.Button("View Code", id={'type': 'view-code-btn', 'index': plot['id']}, style={'marginLeft': '10px'}),
        html.Div([
            dcc.Textarea(
                id={'type': 'view-code-box', 'index': plot['id']},
                value=plot['code'],
                style={
                    'width': '100%',
                    'height': '80px',
                    'resize': 'vertical',
                    'padding': '10px',
                    'border': '1px solid #ccc',
                    'borderRadius': '8px',
                    'boxShadow': '0px 4px 10px rgba(0,0,0,0.1)',
                    'fontSize': '14px',
                    'backgroundColor': '#fefefe'
                },
                readOnly=True
            ),
            html.Button("**Copy**", id={'type': 'copy-code-btn', 'index': plot['id']},
                        style={'marginTop': '5px', 'float': 'right'}),
        ],
        id={'type': 'view-code-box-container', 'index': plot['id']},
        style={
            'position': 'absolute',
            'top': '40px',
            'right': '20px',
            'width': '400px',
            'display': 'none',
            'zIndex': 10,
            'backgroundColor': '#fff',
            'padding': '10px',
            'borderRadius': '10px',
            'boxShadow': '0 2px 12px rgba(0,0,0,0.15)'
        }),

        html.Hr()
    ], style={'marginBottom': '20px'})

def generate_features_table(df):
    columns = df.columns.tolist()
    dtypes = df.dtypes.astype(str).tolist()
    rows = [html.Tr([html.Td(col), html.Td(dtype)]) for col, dtype in zip(columns, dtypes)]
    return dbc.Table(
        [html.Thead(html.Tr([html.Th("Feature"), html.Th("dtype")]))] +
        [html.Tbody(rows)],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        size='sm',
        style={'marginTop': '20px'}
    )
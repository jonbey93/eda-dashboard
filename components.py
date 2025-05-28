from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

def generate_plot_component(plot):
    return html.Div([
        dcc.Graph(figure=go.Figure(plot['figure']), id=f"plot-{plot['id']}"),
        html.Button("Pin", id={'type': 'pin-btn', 'index': plot['id']}),
        html.Button("Clear", id={'type': 'clear-btn', 'index': plot['id']}, style={'marginLeft': '10px'}),
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
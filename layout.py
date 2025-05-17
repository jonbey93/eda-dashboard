from dash import html, dcc

def get_layout():
    return html.Div(style={'padding': '2rem', 'fontFamily': 'Arial'}, children=[
        html.H2("Dashboard with Dynamic Plot Titles"),

        html.Div([
            html.Label("Enter plot title:"),
            dcc.Input(
                id='user-input',
                type='text',
                placeholder='Type plot title here...',
                style={'marginLeft': '0.5rem', 'marginBottom': '1rem', 'width': '50%'}
            ),
            html.Div(id='text-output', style={'fontSize': '1.2rem', 'color': 'blue'})
        ]),

        html.Label("Select plot type:"),
        dcc.Dropdown(
            id='plot-selector',
            options=[
                {'label': 'Line Plot', 'value': 'line'},
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Scatter Plot', 'value': 'scatter'},
                {'label': 'Scatter + Extra Plot', 'value': 'scatter_with_extra'}
            ],
            value='line',
            style={'width': '50%', 'marginBottom': '2rem'}
        ),

        html.Div(id='plots-container')
    ])

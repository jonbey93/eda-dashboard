import dash_bootstrap_components as dbc
from dash import html, dcc

def main_layout():
    return dbc.Container(fluid=True, style={'padding': '2rem', 'maxWidth': '1800px'}, children=[

        dbc.Row(dbc.Col(html.H1("EDA Dashboard", className="text-center mb-4"))),

        # User Input Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Upload CSV Data"),
                    dbc.CardBody([
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div(id='upload-prompt',
                                style={
                                'display': 'flex',
                                'justifyContent': 'center',
                                'alignItems': 'center',
                                'height': '100%',
                                'width': '100%',
                                }),
                            multiple=False,
                        ), 
                        html.Div(id='features-table', className='mt-3'),
                        dcc.Store(id='upload-status'),
                    ])
                ], className='mb-4'),            
            ], width=2),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Ask a Question"),
                    dbc.CardBody([
                        dcc.Textarea(
                            id='user-prompt',
                            style={'width': '100%', 'height': 100},
                            disabled=True
                        ),
                        dbc.Row([
                            dbc.Col(
                                dbc.Button("Run Query", id='run-query', color='primary', className='mt-3', disabled=True),
                                width='auto'
                            ),
                        ], className='g-2'),
                        html.Div(id='text-output', className='text-primary mt-3', style={'fontSize': '1.2rem'})
                    ])
                ]),

                dbc.Card([
                    dbc.CardHeader("LLM Response"),
                    dbc.CardBody([
                        dcc.Loading(
                            id="loading-llm-response",
                            type="default",  # options: "default", "circle", "dot"
                            children=[
                                dcc.Textarea(
                                    id='llm-response',
                                    placeholder='',
                                    style={'width': '100%', 'height': 100},
                                    readOnly=True,
                                    disabled=True
                                ),
                                html.Div(id='copy-feedback', className='text-success mt-2')
                            ]
                        ),
                        dbc.Button("Copy to Clipboard", id='copy-button', color='success', className='mt-3'),
                        html.Div(id='dummy-output', style={'display': 'none'})
                    ])
                ], className='mb-4'),
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Plots"),
                    dbc.CardBody(html.Div(id='plots-container'))
                ], className='mb-4'),
            ], width=6),
        ]),

        dcc.Interval(id='startup-check', interval=500, n_intervals=0, max_intervals=1),
        dcc.Store(id='openai-connect', data=False),
        dcc.Store(id='features-store'),
        dcc.Store(id='data-sample-store'),
        dcc.Store(id='llm-plot-store'),
        dcc.Store(id='plots-store', data=[]),
    ])

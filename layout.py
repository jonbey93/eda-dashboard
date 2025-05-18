from dash import html, dcc
from callbacks import columns_list_global

def main_layout():
    return html.Div(style={'padding': '2rem', 'fontFamily': 'Arial'}, children=[
        html.H1("EDA Dashboard"),

        # Textarea for user input
        html.Div([
            dcc.Textarea(id='user-prompt',
                         placeholder='Ask a question...',
                         style={'width': '100%', 'height': 100}),
            html.Button("Run Query",
                        id='run-query',
                        n_clicks=0,
                        style={'marginTop': '1rem'}),
            html.Div(id='text-output',
                     style={'fontSize': '1.2rem', 'color': 'blue'}),
        ]),

        # Textarea for llm response
        html.Div([
            dcc.Textarea(id='llm-response',
                         placeholder='LLM response will appear here...',
                         style={'width': '100%', 'height': 100},
                         readOnly=True),
            html.Button("Copy to Clipboard",
                        id='copy-button',
                        n_clicks=0,
                        style={'marginTop': '1rem'}),
            html.Div(id='dummy-output', style={'display': 'none'}),
            html.Div(id='copy-feedback', style={'color': 'green'})
        ]),

        # Data upload component
        dcc.Upload(
            id='upload-data',
            children=html.Div(['Drag and Drop or ', html.A('Select CSV File')]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'
            },
            multiple=False,
        ),
        html.Div(id='output-data-upload'),
        dcc.Store(id='columns-store'),
        dcc.Store(id='data-sample-store'),

        # Container for plots
        dcc.Store(id='plots-store', data=[]),
        html.Div(id='plots-container')
    ])

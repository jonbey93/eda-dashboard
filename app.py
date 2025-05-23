from dash import Dash
import dash_bootstrap_components as dbc
from layout import main_layout
from utils.logging import setup_logging
import callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.title = "EDA Dashboard"

app.layout = main_layout()

callbacks.register_callbacks(app)
setup_logging()

if __name__ == '__main__':
    app.run(debug=True)

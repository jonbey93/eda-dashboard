import logging
from dash import Dash
from layout import main_layout
import callbacks

logging.basicConfig(
    level=logging.WARNING,
    filename='debugging.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Dash(__name__)
app.title = "EDA Dashboard"

app.layout = main_layout()

callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)

from dash import Dash
from layout import get_layout
import callbacks

app = Dash(__name__)

app.layout = get_layout()

callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)

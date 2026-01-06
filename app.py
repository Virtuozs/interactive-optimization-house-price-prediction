import dash
from dash import html, dcc, Output, State, Input
from callbacks import register_callbacks
from dotenv import load_dotenv
import os

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "production").lower()
DEBUG = os.getenv("APP_DEBUG", "False") == "True"
PORT = int(os.getenv("APP_PORT", 8050))

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True
)

server = app.server

app.clientside_callback(
    """
    function(n_intervals, step, store) {
        if (!store || !store.history) {
            return step || 0;
        }

        const maxStep = store.history.length - 1;

        if (step === null || step === undefined) {
            return 0;
        }

        return Math.min(step + 1, maxStep);
    }
    """,
    Output("step-store", "data"),
    Input("timer", "n_intervals"),
    State("step-store", "data"),
    State("history-store", "data"),
)


app.layout = html.Div([
    dcc.Store(id="history-store", storage_type="session"),
    dcc.Store(id="data-store", storage_type="session"),
    dcc.Store(id="step-store", data=0, storage_type="session"),
    dcc.Interval(id="timer", interval=300, disabled=True),
    html.Nav(
        className="navbar",
        children=[
            html.A("Training", href="/", className="nav-link"),
            html.A("Prediction", href="/predict", className="nav-link"),
        ]
    ),

    dash.page_container
])

register_callbacks(app)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=DEBUG
    )

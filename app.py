import dash
from dash import html, dcc
from callbacks import register_callbacks

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True
)

server = app.server

app.layout = html.Div([
    dcc.Store(id="history-store", storage_type="session"),
    dcc.Store(id="data-store", storage_type="session"),
    dcc.Store(id="step-store", data=0, storage_type="session"),
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
    app.run(debug=True)

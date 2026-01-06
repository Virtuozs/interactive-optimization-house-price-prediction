import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/predict",
    name="Prediction"
)

layout = html.Div([

    html.H2("House Price Prediction"),

    html.Div([
        html.Label("House Size (m²)", className="control-label"),
        dcc.Input(
            id="predict-size",
            type="number",
            placeholder="e.g. 120",
            min=1
        ),
    ], className="control-group"),

    html.Button("Predict Price", id="predict-btn"),

    html.Div(
        id="prediction-output",
        className="prediction-output"
    )
])

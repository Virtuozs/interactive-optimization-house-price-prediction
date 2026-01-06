import dash 
from dash import dcc, html, dash_table
from figures import empty_dark_figure

dash.register_page(
    __name__,
    path="/",
    name="Training"
)

layout = html.Div([

    html.H2("House Price Prediction — Optimization Visualization"),

    html.Div([
        dcc.Input(id="size-input", type="number", placeholder="House Size (m²)"),
        dcc.Input(id="price-input", type="number", placeholder="House Price (Rp)"),
        html.Button("Add Data", id="add-data"),
        html.Button("Add 10 Random Houses", id="random-data"),
    ], style={"marginBottom": "10px"}),

    dash_table.DataTable(
        id="data-table",
        columns=[
            {"name": "Size (m²)", "id": "Size"},
            {"name": "Price (Rp)", "id": "Price"},
        ],
        page_size=8,
        style_table={
        "backgroundColor": "#0f1117",
        "border": "1px solid #30363d",
        "overflowX": "auto",
        },
        style_header={
            "backgroundColor": "#161b22",
            "color": "#ffffff",
            "fontWeight": "bold",
            "border": "1px solid #30363d",
        },

        style_cell={
            "backgroundColor": "#0f1117",
            "color": "#e6e6e6",
            "border": "1px solid #30363d",
            "padding": "8px",
            "fontFamily": "Segoe UI",
            "fontSize": "14px",
            "textAlign": "right",
        },

        style_data_conditional=[
            {
                "if": {"row_index": "odd"},
                "backgroundColor": "#161b22",
            }
        ],
    ),

    html.Hr(),

    # Controls
    html.Div([

        html.Div([
            html.Label("Optimization Method", className="control-label"),
            dcc.Dropdown(
                id="method",
                options=[
                    {"label": "Gradient Descent", "value": "gd"},
                    {"label": "Quasi-Newton (BFGS)", "value": "bfgs"},
                ],
                value="gd",
                clearable=False
            ),
        ], className="control-group"),

        html.Div([
            html.Label("Learning Rate (α)", className="control-label"),
            dcc.Slider(
                id="lr",
                min=0.1,
                max=1.0,
                step=0.1,
                value=0.1,
                marks={
                    0.1: "0.1",
                    0.2: "0.2",
                    0.3: "0.3",
                    0.4: "0.4",
                    0.5: "0.5",
                    0.6: "0.6",
                    0.7: "0.7",
                    0.8: "0.8",
                    0.9: "0.5",
                    1.0: "1.0"
                }
            ),
        ], className="control-group"),

        html.Div([
            html.Label("Number of Iterations", className="control-label"),
            dcc.Slider(
                id="iters",
                min=10,
                max=200,
                step=10,
                value=30,
                marks={
                    10: "10",
                    20: "20",
                    30: "30",
                    40: "40",
                    50: "50",
                    60: "60",
                    790: "70",
                    80: "80",
                    90: "90",
                    100: "100",
                    110: "110",
                    120: "120",
                    130: "130",
                    140: "140",
                    150: "150",
                    160: "160",
                    170: "170",
                    180: "180",
                    190: "190",
                    200: "200"
                }
            ),
        ], className="control-group"),

    ], className="controls"),


    html.Br(),

    html.Button("▶ Play", id="play"),
    html.Button("⏸ Pause", id="pause"),
    
    dcc.Graph(
        id="regression",
        figure=empty_dark_figure(height=350),
        style={"height": "350px"}
    ),

    dcc.Graph(
        id="loss", 
        figure=empty_dark_figure(height=350),
        style={"height": "300px"}),
    dcc.Graph(
        id="trajectory",
        figure=empty_dark_figure(height=350),
        style={"height": "300px"}),
])

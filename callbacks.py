import dash
from dash import Input, Output, State, callback_context, no_update, html
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from model.linear_regression import LinearRegressionModel
from optimizer.gradient_descent import gradient_descent
from optimizer.quasi_newton import quasi_newton_bfgs
from figures import empty_dark_figure

def dark_figure(fig, height=350):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        font=dict(color="#e6e6e6"),
        height=height,
        margin=dict(l=40, r=20, t=40, b=40),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#30363d",
        zeroline=False
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="#30363d",
        zeroline=False
    )

    return fig

def register_callbacks(app):

    @app.callback(
        Output("data-store", "data"),
        Input("add-data", "n_clicks", allow_optional=True),
        Input("random-data", "n_clicks", allow_optional=True),
        State("size-input", "value"),
        State("price-input", "value"),
        State("data-store", "data"),
        prevent_initial_call=True
    )
    def update_data(add, random_add, size, price, data):
        df = pd.DataFrame(data)

        trigger = dash.callback_context.triggered_id

        if trigger == "add-data" and size and price:
            df = pd.concat(
                [df, pd.DataFrame([[size, price]], columns=["Size", "Price"])]
            )

        elif trigger == "random-data":
            sizes = np.random.uniform(30, 200, 10)
            prices = 5_000_000 * sizes + 100_000_000 + np.random.normal(0, 30_000_000, 10)
            df = pd.concat(
                [df, pd.DataFrame({"Size": sizes, "Price": prices})]
            )

        return df.to_dict("records")
    
    @app.callback(
        Output("data-table", "data"),
        Input("data-store", "data", allow_optional=True)
    )
    def update_table(data):
        return data

    @app.callback(
        Output("history-store", "data"),
        Input("data-store", "data", allow_optional=True),
        Input("method", "value", allow_optional=True),
        Input("lr", "value", allow_optional=True),
        Input("iters", "value", allow_optional=True),
    )
    def run_optimization(data, method, lr, iters):
        ctx = callback_context

        if ctx.triggered_id not in {"data-store", "method", "lr", "iters"}:
            return no_update
        
        if method is None or lr is None or iters is None:
            return no_update

        if not data or len(data) < 3 or lr is None or iters is None:
            return no_update

        df = pd.DataFrame(data)
        x_raw = df["Size"].values
        y_raw = df["Price"].values

        x = (x_raw - x_raw.mean()) / x_raw.std()
        y = (y_raw - y_raw.mean()) / y_raw.std()

        model = LinearRegressionModel()

        iters = int(iters)
        lr = float(lr)

        history = (
            gradient_descent(model, x, y, lr, iters)
            if method == "gd"
            else quasi_newton_bfgs(model, x, y, lr, iters)
        )

        return {
            "history": history,
            "x_mean": float(x_raw.mean()),
            "x_std": float(x_raw.std()),
            "y_mean": float(y_raw.mean()),
            "y_std": float(y_raw.std()),
        }

    @app.callback(
        Output("step-store", "data"),
        Input("timer", "n_intervals", allow_optional=True),
        Input("method", "value", allow_optional=True),
        Input("lr", "value", allow_optional=True),
        Input("iters", "value", allow_optional=True),
        State("step-store", "data"),
        State("history-store", "data"),
    )
    def control_step(n_intervals, method, lr, iters, step, history):

        ctx = callback_context
        if not ctx.triggered:
            return 0

        trigger = ctx.triggered_id

        if trigger in {"method", "lr", "iters"}:
            return 0

        if trigger == "timer" and history and "history" in history:
            return min(step + 1, len(history["history"]) - 1)
        
        return step

    @app.callback(
        Output("regression", "figure"),
        Output("loss", "figure"),
        Output("trajectory", "figure"),
        Input("step-store", "data", allow_optional=True),
        State("history-store", "data"),
        State("data-store", "data"),
    )
    def update_graphs(step, history, data):
        if not history or not data:
            return (
            empty_dark_figure(height=350),
            empty_dark_figure(height=300),
            empty_dark_figure(height=300),
            )

        df = pd.DataFrame(data)
        x_raw, y_raw = df["Size"].values, df["Price"].values

        x = (x_raw - x_raw.mean()) / x_raw.std()
        y = (y_raw - y_raw.mean()) / y_raw.std()

        hist = history["history"]
        w, b = hist[step]["w"], hist[step]["b"]
        y_pred = (w * x + b) * y_raw.std() + y_raw.mean()

        fig_reg = go.Figure([
            go.Scatter(x=x_raw, y=y_raw, mode="markers", name="Data"),
            go.Scatter(x=x_raw, y=y_pred, mode="lines", name=f"Iter {step}")
        ])
        
        fig_reg.update_layout(
            title=f"Regression Fit (Iteration {step})",
            xaxis_title="House Size (m²)",
            yaxis_title="House Price (Rupiah)",
            legend_title="Legend",
            template="plotly_dark",
            paper_bgcolor="#0f1117",
            plot_bgcolor="#0f1117",
            font=dict(color="#e6e6e6"),
            margin=dict(l=40, r=20, t=40, b=40),
            height=350
        )
        
        fig_reg.update_traces(
            selector=dict(mode="markers"),
            name="Observed Data"
        )
        fig_reg.update_traces(
            selector=dict(mode="lines"),
            name="Regression Line"
        )
        
        fig_reg.add_annotation(
            text=f"y = {w:.3f}·x + {b:.3f}",
            xref="paper",
            yref="paper",
            x=0.02,
            y=0.98,
            showarrow=False,
            font=dict(size=14, color="#e6e6e6"),
            bgcolor="#161b22",
            bordercolor="#30363d",
            borderwidth=1
        )


        fig_loss = go.Figure([
            go.Scatter(
                y=[h["loss"] for h in hist[: step + 1]],
                mode="lines+markers"
            )
        ])
        
        fig_loss.update_layout(
            title="Loss Convergence",
            xaxis_title="Iteration",
            yaxis_title="Mean Squared Error (MSE)",
            template="plotly_dark",
            paper_bgcolor="#0f1117",
            plot_bgcolor="#0f1117",
            font=dict(color="#e6e6e6"),
            margin=dict(l=40, r=20, t=40, b=40),
            height=350
        )
        
        fig_loss.add_annotation(
            text="Lower is better",
            xref="paper",
            yref="paper",
            x=0.02,
            y=0.95,
            showarrow=False,
            font=dict(color="#8b949e")
        )

        fig_traj = go.Figure([
            go.Scatter(
                x=[h["w"] for h in hist[: step + 1]],
                y=[h["b"] for h in hist[: step + 1]],
                mode="lines+markers"
            )
        ])
        
        fig_traj.update_layout(
            title="Parameter Update Trajectory",
            xaxis_title="Weight (w)",
            yaxis_title="Bias (b)",
            template="plotly_dark",
            paper_bgcolor="#0f1117",
            plot_bgcolor="#0f1117",
            font=dict(color="#e6e6e6"),
            margin=dict(l=40, r=20, t=40, b=40),
            height=350
        )
        
        fig_traj.add_trace(
            go.Scatter(
                x=[hist[0]["w"]],
                y=[hist[0]["b"]],
                mode="markers",
                marker=dict(size=10, color="green"),
                name="Start"
            )
        )

        fig_traj.add_trace(
            go.Scatter(
                x=[hist[step]["w"]],
                y=[hist[step]["b"]],
                mode="markers",
                marker=dict(size=10, color="red"),
                name=f"Iteration {step}"
            )
        )


        return (
            dark_figure(fig_reg, 350),
            dark_figure(fig_loss, 300),
            dark_figure(fig_traj, 300),
        )
    
    @app.callback(
        Output("timer", "disabled"),
        Input("play", "n_clicks", allow_optional=True),
        Input("pause", "n_clicks", allow_optional=True),
        Input("method", "value", allow_optional=True),
        Input("lr", "value", allow_optional=True),
        Input("iters", "value", allow_optional=True),
    )
    def control_timer(play, pause, method, lr, iters):

        ctx = callback_context
        if not ctx.triggered:
            return True

        trigger = ctx.triggered_id

        if trigger == "play":
            return False

        if trigger in {"pause", "method", "lr", "iters"}:
            return True

        return True
    
    # PREDICTION CALLBACK
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-btn", "n_clicks", allow_optional=True),
        State("predict-size", "value"),
        State("history-store", "data"),
        prevent_initial_call=True
    )
    def predict_price(n_clicks, size, store):

        if not store:
            return html.Div("Train the model first on the Training page.")

        if size is None:
            return html.Div("Please enter a house size.")

        # Unpack stored data
        history = store["history"]
        x_mean = store["x_mean"]
        x_std = store["x_std"]
        y_mean = store["y_mean"]
        y_std = store["y_std"]

        # Normalize input
        x_norm = (size - x_mean) / x_std

        # Final trained parameters
        w = history[-1]["w"]
        b = history[-1]["b"]

        # Predictions
        y_norm = w * x_norm + b           
        y_real = y_norm * y_std + y_mean     

        return html.Div([

            html.Div([
                html.Span("Normalized Prediction: "),
                html.Strong(f"{y_norm:.3f}")
            ], className="prediction-line"),

            html.Div([
                html.Span("Predicted House Price: "),
                html.Strong(f"Rp {y_real:,.0f}")
            ], className="prediction-line"),

        ])

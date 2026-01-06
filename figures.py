import plotly.graph_objects as go

def empty_dark_figure(height=300):
    fig = go.Figure()

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f1117",
        plot_bgcolor="#0f1117",
        height=height,
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False
        ),
        annotations=[
            dict(
                text="Waiting for data...",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16, color="#8b949e")
            )
        ]
    )

    return fig

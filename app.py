from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objs as go

app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

colors = {
    "fg": "#2cfec1",
    "bg": "#1f2630"
}

default_fig = dict(
    data=[dict(x=0, y=0)],
    layout=dict(
        title="Search for GitHub Username",
        paper_bgcolor=colors["bg"],
        plot_bgcolor=colors["bg"],
        font=dict(color=colors["fg"]),
        margin=dict(t=75, r=50, b=100, l=75)
    )
)

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H1(
                    children="GitHub Contribution Stats",
                    style={"textAlign": "center"}
                )
            ]
        ),
        html.Div(
            id="app-container",
            children=[
                html.Div(
                    id="left-column",
                    children=[
                        html.Div(
                            id="search-container",
                            children=[
                                dcc.Input(
                                    id="input-username",
                                    type="text",
                                    placeholder="username"
                                ),
                                html.Button(
                                    "Search",
                                    id="submit-val"
                                )
                            ]
                        ),
                        html.Div(
                            id="stats-container",
                            children=[
                                html.P(
                                    "User Stats Here..."
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    id="graph-container",
                    children=[
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": "Bar Chart",
                                    "value": "bar"
                                },
                                {
                                    "label": "Line Chart",
                                    "value": "line"
                                },
                                {
                                    "label": "Scatter Chart",
                                    "value": "scatter"
                                }
                            ],
                            value="bar",
                            id="chart-dropdown"
                        ),
                        dcc.Graph(
                            id="selected-data",
                            figure=default_fig
                        ),
                        dcc.Slider(
                            0,
                            12,
                            id="months-slider",
                            step=None,
                            marks={
                                0: "Apr",
                                1: "May",
                                2: "Jun",
                                3: "Jul"
                            },
                            value=3
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    Output("selected-data", "figure"),
    [
        Input("input-username", "value"),
        Input("chart-dropdown", "value")
    ]
)
def update_graph(username, selected_chart):
    if not username:
        return default_fig

    if selected_chart == "bar":
        df = px.data.gapminder().query("country == 'Canada'")
        return px.bar(df, x="year", y="pop",
             hover_data=["lifeExp", "gdpPercap"], color="lifeExp",
             labels={"pop":"population of Canada"}, height=400)
    elif selected_chart == "line":
        return go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
    elif selected_chart == "scatter":
        df = px.data.iris()
        return px.scatter(df, x="sepal_width", y="sepal_length")


if __name__ == "__main__":
    app.run_server(debug=True)

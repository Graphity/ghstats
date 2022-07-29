from ghcc import GHCC

from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import pandas as pd

app = Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"]
)

server = app.server

colors = {
    "fg": "#c9d1d9",
    "bg": "#0d1117",
    "gray": "#171b22",
}

default_fig = dict(
    data=[dict(x=0, y=0)],
    layout=dict(
        title="Search for GitHub Username",
        paper_bgcolor=colors["bg"],
        plot_bgcolor=colors["bg"],
        font=dict(color=colors["fg"])
    )
)

app.layout = html.Div([
    html.Div(id="top-container", children=[
        html.H1("GitHub Contribution Stats"),
        html.Div(id="search-container", children=[
            dcc.Input(id="search-input", type="text",
                      debounce=True, placeholder="Search..."),
            html.Button(id="search-button", n_clicks=0,
                        className="fa fa-search")
        ]),
        dcc.Dropdown(id="dropdown", value="bar",
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
                             "label": "Area Chart",
                             "value": "area"
                         },
                         {
                             "label": "Scatter Chart",
                             "value": "scatter"
                         },
                         {
                             "label": "3D Scatter Chart",
                             "value": "3d-scatter"
                         }
                     ])
    ]),
    dcc.Graph(id="graph", figure=default_fig),
    html.Div(id="slider-container", children=[
        html.P("Drag slider to change the range"),
        dcc.RangeSlider(0, 12, id="slider", step=None, value=[0, 12])
    ])
])

@app.callback(
    [
        Output("slider", "max"),
        Output("slider", "value"),
        Output("slider", "marks")
    ],
    Input("search-input", "value")
)
def update_slider(username):
    try:
        user = GHCC(username)
        months = [month['name'] for month in user.months]
        _max = len(months) - 1
        return _max, [0, _max], dict(enumerate(months))
    except ValueError:
        return 12, [0, 12], {}

@app.callback(
    Output("graph", "figure"),
    [
        Input("search-input", "value"),
        Input("dropdown", "value"),
        Input("slider", "value")
    ],
    State("search-input", "value")
)
def update_graph(username, chart, month_range, username_submit):
    if not username or not chart:
        return default_fig

    if username_submit:
        username = username_submit

    try:
        user = GHCC(username)
    except ValueError:
        return default_fig

    a, b = month_range
    cal = []
    for month in user.months[a:b+1]:
        cal += month['days']
    df = pd.DataFrame(cal)
    
    if chart == "bar":
        fig = px.bar(df, x="date", y="count", hover_data=["level"],
                     labels={"count": "contributions"})
    elif chart == "line":
        fig = px.line(df, x="date", y="count", markers=True,
                      hover_data=["level"], labels={"count": "contributions"})
    elif chart == "area":
        fig = px.area(df, x="date", y="count", hover_data=["level"],
                      labels={"count": "contributions"})
    elif chart == "scatter":
        fig = px.scatter(df, x="date", y="count", size="level",
                         hover_data=["level"],
                         labels={"count": "contributions"})
    elif chart == "3d-scatter":
        fig =  px.scatter_3d(df, x="date", y="count", z="level",
                             size="level", hover_data=["level"],
                             labels={"count": "contributions"})

    fig["data"][0]["marker"]["line"]["width"] = 0

    fig.update_layout(
        plot_bgcolor=colors["bg"],
        paper_bgcolor=colors["bg"],
        font_color=colors["fg"],
        xaxis_gridcolor=colors["gray"],
        yaxis_gridcolor=colors["gray"]
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

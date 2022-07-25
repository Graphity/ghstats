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
        dcc.RangeSlider(0, 11, id="slider", step=None, value=[0, 11],
                        marks={
                            0: "Aug 2021",
                            1: "Sep 2021",
                            2: "Oct 2021",
                            3: "Nov 2021",
                            4: "Dec 2021",
                            5: "Jan 2022",
                            6: "Feb 2022",
                            7: "Mar 2022",
                            8: "Apr 2022",
                            9: "May 2022",
                            10: "Jun 2022",
                            11: "Jul 2022"
                        })
    ])
])

@app.callback(
    Output("graph", "figure"),
    [
        Input("search-input", "value"),
        Input("search-button", "n_clicks"),
        Input("dropdown", "value"),
        Input("slider", "value")
    ],
    State("search-input", "value")
)
def update_graph(username, n_clicks, chart, month_range, username_submit):
    if not username or not chart:
        return default_fig

    if username_submit:
        username = username_submit

    try:
        user = GHCC(username)
    except ValueError:
        return default_fig

    marks = {
        0: "21-Aug",
        1: "21-Sep",
        2: "21-Oct",
        3: "21-Nov",
        4: "21-Dec",
        5: "22-Jan",
        6: "22-Feb",
        7: "22-Mar",
        8: "22-Apr",
        9: "22-May",
        10: "22-Jun",
        11: "22-Jul"
    }
    cal = []
    x, y = month_range
    for i in range(x, y+1):
        for day in user.calendar[marks[i]]:
            cal.append(day)
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

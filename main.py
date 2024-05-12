from dash import Dash, html, dcc
from dash_table import DataTable
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.express as px

file = "Cleaned_Airbnb_Data.csv"
data = pd.read_csv(file)

# Convert 'host_response_rate' and 'review_scores_rating' to numeric values
data["host_response_rate"] = (
    data["host_response_rate"].str.rstrip("%").astype("float") / 100.0
)
data["review_scores_rating"] = pd.to_numeric(
    data["review_scores_rating"], errors="coerce"
)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Instead of defining the headers manually, get them directly from the DataFrame
headers = [
    header
    for header in data.columns.tolist()
    if header
    not in ["amenities", "first_review", "host_since", "last_review", "longitude"]
]

app.layout = html.Div(
    [
        html.Div(
            className="row",
            children="AirBnb Statistics",
            style={"textAlign": "center", "color": "blue", "fontSize": 30},
        ),
        html.Div(
            className="row",
            children=[
                dcc.RadioItems(
                    options=[
                        {"label": "Histogram", "value": "Histogram"},
                        {"label": "Line Chart", "value": "Line Chart"},
                        {"label": "Pie Chart", "value": "Pie Chart"},
                    ],
                    value=None,
                    id="chart-type",
                ),
                dcc.Dropdown(
                    options=[{"label": header, "value": header} for header in headers],
                    value=None,
                    id="data-type",
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                DataTable(
                    data=data.to_dict("records"),
                    page_size=11,
                    style_table={"overflowX": "auto"},
                )
            ],
        ),
        html.Div(
            className="row",
            children=[dcc.Graph(figure={}, id="chart")],
        ),
    ]
)


@app.callback(
    Output(component_id="chart", component_property="figure"),
    Input(component_id="chart-type", component_property="value"),
    Input(component_id="data-type", component_property="value"),
)
def update_graph(chart_type, data_type):
    if data_type is None:
        return {}
    if chart_type == "Histogram":
        fig = px.histogram(data, x=data_type)
    elif chart_type == "Line Chart":
        fig = px.line(data, x=data.index, y=data_type)
    elif chart_type == "Pie Chart":
        fig = px.pie(data, names=data_type)
    else:
        fig = {}

    return fig


@app.callback(
    Output(component_id="data-type", component_property="options"),
    Input(component_id="chart-type", component_property="value"),
)
def update_dropdown(chart_type):
    if chart_type == "Pie Chart":
        boolean_headers = [header for header in headers if data[header].dtype == "bool"]
        return [{"label": header, "value": header} for header in boolean_headers]
    elif chart_type in ["Histogram", "Line Chart"]:
        numeric_headers = [
            header for header in headers if pd.api.types.is_numeric_dtype(data[header])
        ]
        return [{"label": header, "value": header} for header in numeric_headers]
    else:
        return [{"label": header, "value": header} for header in headers]


if __name__ == "__main__":
    app.run_server(debug=True)

from dash import Dash, html, dcc
from dash_table import DataTable
from dash.dependencies import Output, Input, State
import pandas as pd
import plotly.express as px

file = "Airbnb_Data.csv"
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

# Define the headers
headers = [
    "id",
    "log_price",
    "property_type",
    "room_type",
    "amenities",
    "accommodates",
    "bathrooms",
    "bed_type",
    "cancellation_policy",
    "cleaning_fee",
    "city",
    "description",
    "first_review",
    "host_has_profile_pic",
    "host_identity_verified",
    "host_response_rate",
    "host_since",
    "instant_bookable",
    "last_review",
    "latitude",
    "longitude",
    "name",
    "neighbourhood",
    "number_of_reviews",
    "review_scores_rating",
    "zipcode",
    "bedrooms",
    "beds",
]

# Define the visualization types
viz_types = [
    "Bar chart",
    "Heat map",
    "Histogram",
    "Pie chart",
    "Scatter plot",
    "Line chart",
    "Stacked bar chart",
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
                        {"label": "Accommodation", "value": "accommodates"},
                        {"label": "Reviews", "value": "number_of_reviews"},
                        {"label": "Host Response Rate", "value": "host_response_rate"},
                        {
                            "label": "Review Scores Rating",
                            "value": "review_scores_rating",
                        },  # New radio button
                        {
                            "label": "Make a New Visualization",
                            "value": "new_viz",
                        },  # New radio button
                    ],
                    value="accommodates",
                    inline=True,
                    id="my-radio-buttons-final",
                )
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="six columns",
                    children=[
                        DataTable(
                            data=data.to_dict("records"),
                            page_size=11,
                            style_table={"overflowX": "auto"},
                        )
                    ],
                ),
                html.Div(
                    className="six columns",
                    children=[dcc.Graph(figure={}, id="histo-chart-final")],
                ),
            ],
        ),
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="six columns",
                    children=[
                        dcc.Checklist(
                            options=[],
                            id="header-checklist",
                        ),
                        dcc.Dropdown(
                            options=[],
                            id="viz-dropdown",
                        ),
                    ],
                ),
            ],
        ),
    ]
)


@app.callback(
    [Output("header-checklist", "options"), Output("viz-dropdown", "options")],
    [Input("my-radio-buttons-final", "value")],
)
def toggle_menu(value):
    if value == "new_viz":
        return [{"label": header, "value": header} for header in headers], [
            {"label": viz_type, "value": viz_type} for viz_type in viz_types
        ]
    else:
        return [], []


@app.callback(
    Output(component_id="histo-chart-final", component_property="figure"),
    Input(component_id="my-radio-buttons-final", component_property="value"),
)
def update_graph(col_chosen):
    if col_chosen == "review_scores_rating":
        # Create a distplot between 'review_scores_rating' and 'host_response_rate'
        fig = px.histogram(
            data, x="review_scores_rating", y="host_response_rate", histfunc="avg"
        )
    else:
        # Calculate the average for the selected option
        avg_value = data[col_chosen].mean()

        # Create a histogram of the selected column
        fig = px.histogram(data, x=col_chosen)

        # Add a vertical line to represent the average
        fig.add_shape(
            type="line",
            x0=avg_value,
            x1=avg_value,
            y0=0,
            y1=1,
            yref="paper",
            line=dict(color="red"),
        )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

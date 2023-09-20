import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import time

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Wood pyrolysis dynamics"
server = app.server

data = pd.read_csv('Res_rho_char.csv')

def time_slide(i):
    col_i = data.iloc[:, i]
    return col_i

app.layout = html.Div([
    html.Div([
        html.P(children=("🪵 🔥 🪵"), className="header-emoji",),
        html.H1('Wood pyrolysis dynamics, rho_char', className="header-title"),
        html.P(children=("We study de charcoal density with time."), className="header-description",),
    ], className="header"),
    html.Div([
    gif.GifPlayer(
        gif='assets/wood.gif',
        still='assets/still.png',)
    ]),
    html.Div(children=[
        dcc.Graph(
            id="rho-char",
            config={"displayModeBar": True},
            figure={
                "data": [
                    {
                        "x": list(range(0, int(len(data.columns) / 6))),
                        "y": list(time_slide(99)),
                        "type": "lines",
                        "hovertemplate": (
                            "$%{y:.3f}<extra></extra>"
                        ),
                    },
                ],
                "layout": {
                    "title": {
                        "text": "rho_char",
                        "x": 0.01,
                        "xanchor": "left",
                    },
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"fixedrange": True},
                    "colorway": ["#3fb817"],
                },
            },
        ),
    ]),
    html.Div([
        html.Button('Play', id='play-button'),
        dcc.Slider(
            id='my-slider',
            min=0,
            max=len(data.columns) - 1,
            step=1,
            value=0,
            marks={
                0: '0',
                100: '100',
                200: '200',
                300: '300',
                400: '400',
                500: '500',
                600: '600',
                700: '700',
                800: '800',
                900: '900',
                1000: '1000'
            },
        ),
        dcc.Interval(id='interval-component', interval=100, n_intervals=0),
    ]),
    html.Div([
        dcc.Graph(
            id='heatmap',
            figure={
                'data': [{
                    'z': data.values.tolist(),
                    'type': 'heatmap',
                    'colorscale': 'YlOrRd'
                }],
        "layout": {
            "title": {
                "text": "Heatmap of charcoal density x vs time",
                "x": 0.01,
                "xanchor": "left",
            },
            "xaxis": {"title": "x", "fixedrange": True,"range": [0, 200],},
            "yaxis": {"title": "Time [...] ", "fixedrange": True, "range": [0, 0.06],},
            #"colorway": ["#3fb817"],
        },
            },
        ),
    ]),
])

@app.callback(
    Output('my-slider', 'value'),
    Output('rho-char', 'figure'),
    Input('play-button', 'n_clicks'),
    Input('interval-component', 'n_intervals'),
    State('my-slider', 'value')
)
def update_slider_and_plot(n_clicks, n_intervals, current_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        prop_id = 'No inputs'
    else:
        prop_id = ctx.triggered[0]['prop_id']

    if prop_id == 'play-button.n_clicks':
        # Increment the slider value when the "Play" button is clicked
        next_value = current_value + 1
        if next_value >= len(data.columns):
            next_value = 0  # Reset to the beginning if we reach the end
    elif prop_id == 'interval-component.n_intervals':
        # Automatically increment the slider value at regular intervals
        next_value = current_value + 1
        if next_value >= len(data.columns):
            next_value = 0  # Reset to the beginning if we reach the end
    else:
        # Default value when the page loads
        next_value = 0

    # Update the y-values of the 'rho-char' plot
    updated_figure = {
        "data": [
            {
                "x": list(range(0, int(len(data.columns) /6))),
                "y": list(time_slide(next_value)),
                "type": "lines",
                "hovertemplate": "$%{y:.3f}<extra></extra>",
            }
        ],
        "layout": {
            "title": {
                "text": "Density of charcoal",
                "x": 0.01,
                "xanchor": "left",
            },
            "xaxis": {"title": "x", "fixedrange": True},
            "yaxis": {"title": "Density [kg/m^3]", "fixedrange": True, "range": [0, 0.06],},
            "colorway": ["#3fb817"],
        },
    }

    return next_value, updated_figure

if __name__ == '__main__':
    app.run_server(debug=True)

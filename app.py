import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
import pandas as pd
import plotly.graph_objs as go

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
server = app.server
app.title = "Wood pyrolysis dynamics" 

data_rho_char = pd.read_csv('Res_rho_char.csv')
data_R_kin = pd.read_csv('Res_R_kin.csv')

def time_slide_rho_char(i):
    col_i = data_rho_char.iloc[:,i]
    return col_i

def time_slide_r_kin(i):
    col_i = data_R_kin.iloc[:,i]
    return col_i


app.layout = html.Div([html.Div([
	html.P(children=("🪵 🔥 🪵"),className="header-emoji",),
    html.H1('Wood pyrolysis dynamics', className="header-title"),        
    html.P(children=("We simulate the dynamics of a wood stick in time."),className="header-description",), 
            ],className="header"), 
    
    html.P(children=[' We can select an specific value of time using the slider below the plots. '],className="body"),

    #Grafico 1 (izquierda)
    html.Div(
            children=[dcc.Graph(
            id="rho-char",
            config={"displayModeBar": True},
        ),
    ],style={'width': '50%', 'display': 'inline-block'} ,className="grafico"),
    #Grafico 2 (derecha)
    html.Div(
            children=[dcc.Graph(
            id="r-kin",
            config={"displayModeBar": True},
        ),
    ],style={'width': '50%', 'display': 'inline-block'} ,className="grafico"),
   
    html.P(children=['Select the desire time.'],className="body"),
    #Slider            
    html.Div([
        dcc.Slider(
            id='my-slider',
            min=0,
            max=1000,
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
            tooltip={"placement": "bottom", "always_visible": True}
        ),
    ]),

    html.P(children=[' We dynamically plot the evolution of the variables of interest for each slide of time. '],className="body"),

    html.Div([
    gif.GifPlayer(
        gif='assets/wood.gif',
        still='assets/still.png',)
    ],style={'width': '49%', 'display': 'inline-block'} ,className="grafico"),

    html.Div([
    gif.GifPlayer(
        gif='assets/wood.gif',
        still='assets/still.png',)
    ],style={'width': '49%', 'display': 'inline-block'} ,className="grafico"),    
   
    
   
   
    #html.Div([
    #    dcc.Graph(
    #        id='heatmap',
    #        figure={
    #            'data': [{
    #                'z': data.values.tolist(),
    #                'type': 'heatmap',
    #                'colorscale': 'Viridis'
    #            }],
    #        },
    #    ),
    #]),
]) 

@app.callback(
    dash.dependencies.Output('rho-char', 'figure'),
    [dash.dependencies.Input('my-slider', 'value')])
  
def update_rho_char1(value):
    rho_char1_figure = {
        'data': [{
            "x": list(range(0, int(len(data_rho_char.columns)/5))),
            "y": list(time_slide_rho_char(value)),
            "type": "lines",
        }],
        "layout": {
            "title": {
                "text": "Density of charcoal",
                "x": 0.01,
                "xanchor": "left",
            },
            "xaxis": {"title": "First 200 x's", "fixedrange": True},
            "yaxis": {"title": "Density [kg/m^3]", "fixedrange": True, "range": [0, 0.06],
            },
            "colorway": ["#3fb817"],
        },
    }
    return rho_char1_figure

@app.callback(
    dash.dependencies.Output('r-kin', 'figure'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_r_kin(value):
    r_kin_figure = {
        'data': [{
            "x": list(range(0, int(len(data_R_kin.columns)/5))),
            "y": list(time_slide_r_kin(value)),
            "type": "lines",
        }],
        "layout": {
            "title": {
                "text": "R kinetic",
                "x": 0.01,
                "xanchor": "left",
            },
            "xaxis": {"title": "First 200 x's", "fixedrange": True},
            "yaxis": {"title": "Arreglar unidades [kg/m^3]", "fixedrange": True, "range": [0, 0.000015],
            },
            "colorway": ["#3fb817"],
        },
    }    
    return r_kin_figure 

if __name__ == '__main__':
    app.run_server(debug=True)
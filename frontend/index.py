import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output, State
from app import app
from page1 import layout1
from page2 import layout2
from page1S import layout3

app.layout = app.layout= html.Div([

    dcc.Location(id="url",refresh=False),
    html.Div(id="body")
])

@app.callback(Output("url","pathname"), [Input("go","n_clicks")], [State("bnq_selector","value")])
def test(input_1, state):
    if input_1 is not None :
        return state  

@app.callback(Output("body","children"),[Input("url","pathname")])
def change_page(pathname):
    if pathname=="/bng":
        return layout2  
    if pathname=="/bnq":
        return layout1 
    if pathname=="/bnt":
        return layout3            
    return layout1

app.run_server(debug = True)


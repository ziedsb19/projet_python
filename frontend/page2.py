import dash
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output


layout2= html.Div(className="container-fluid", children= [
    dcc.Link("banque amerique ", href="/bnq"), 
    html.H1("ici Nahoulty <3", className="text-danger")
]
)

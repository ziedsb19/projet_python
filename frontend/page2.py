import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pickle
from pickle import load
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd


from app import app



with open ('../german.pckl','rb') as file:
    data = load(file)


layout2= html.Div(className="container-fluid", children= [

    html.Div(id='intermediate-value', style={'display': 'none'}),

    html.Div(className="jumbotron pt-4", children=[
        html.H1(className="display-6", children="Welcome to my App"),
        html.P("This is a simple hero unit, a simple jumbotron-style component for calling extra attention to featured content or information", className="lead"),

        html.Hr(className="my-4"),
        html.P("It uses utility classes for typography and spacing to space content out within the larger container."),
        html.Div(className="d-flex justify-content-between ",children=[
            html.Button("Learn more",className="btn btn-primary" ),
            html.Div(className="col-6", children=[
                html.Div(className="row", children=[
                    html.Div(className="col-6 offset-4",children=[
                        dcc.Dropdown(id="bnq_selector",options=[
                        {"label":"Banque amerique", "value":"/bnq"},
                        {"label":"Banque germany", "value":"/bng"},
                        {"label":"Banque taywan", "value":"/bnt"},
                        ])
                    ]),
                    html.Button(id="go", children="go to Bank", className="btn btn-outline-success")
                ])

            ])
        ])
        
    ]),

    #///////////////////////////////////////////////////////////////////////////////////////////////////////

    html.Div(className="row", children=[
        html.Div(id="divleft",className="col-6",children=[
            html.H3("scores d'accuracy pour chaque modele entrainé : ", className="col-11 offset-1 text-dark"),
            html.Hr(className="col-10 offset-1 mb-4"),
            html.Div(className="row",children=[
                html.Div(className="col-11 offset-1", children=[
                    html.Div(className="row", children=[
                        html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("XGB boost", className="text-muted"),
                    html.P(round(data[0][2],2),className="display-4 text-success" if round(data[0][2],2)>=0.75 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[0][1],2)), className="mb-0 mt-0 text-muted float-right")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("Naive Bayes", className="text-muted"),
                    html.P(round(data[1][2],2),className="display-4 text-success" if round(data[1][2],2)>=0.75 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[1][1],2)), className="mb-0 mt-0 text-muted float-right")
                ]),
                    html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("logistic regression", className="text-muted"),
                    html.P(round(data[2][2],2),className="display-4 text-success" if round(data[2][2],2)>=0.75 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[2][1],2)), className="mb-0 mt-0 text-muted float-right")
                ]),
                    html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("ADA boost", className="text-muted"),
                    html.P(round(data[3][2],2),className="display-4 text-success" if round(data[3][2],2)>=0.75 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[3][1],2)), className="mb-0 mt-0 text-muted float-right")
                ])
                
                ])
            ])
                
            ]),


        html.H3("Courbe ROC pour chaque Modele: ", className="col-11 offset-1 text-dark mt-4"),
        html.Hr(className="col-10 offset-1  mb-5"),
                html.Div(className="p-4 shadow col-10 offset-1", children=[
                dcc.Graph(
                
                id='roc',
                figure={
                    'data': [
                        {'x': data[0][3][0], 'y': data[0][3][1], 'type': 'scatter', 'name': 'XGBoost'},
                        {'x': data[1][3][0], 'y': data[1][3][1], 'type': 'scatter', 'name': 'Naive Bayes'},
                        {'x': data[2][3][0], 'y': data[2][3][1], 'type': 'scatter', 'name': 'Logistic Regression'},
                        {'x': data[3][3][0], 'y': data[3][3][1], 'type': 'scatter', 'name': 'ADAboost'}
                        ],
                    'layout': {
                        'title': 'ROC courbe'
                    }
                }
             )
            ]),

        ]), 

#//////////////////////// form ///////////////////////////

    html.Div(className="col-6",children=[
                html.H3(className="text-dark col-11 offset-1 mt-1", children="Formulaire à remplir :"),
                html.Hr(className="col-11 offset-1"),
                html.Div(className="p-5 ml-5 shadow",children=[
                html.Form([
                    html.Div(className="form-group col-6",children=[
                        html.Label("creditamount", htmlFor="creditamount"),
                        dcc.Input(type="number",id="creditamount", className="form-control", placeholder="enter the credit amount"),
                        html.Small("enter the credit amount", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("duration", htmlFor="duration"),
                        dcc.Input(type="number",id="duration",  className="form-control", placeholder="enter the duration"),
                        html.Small("enter the duration", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("installmentrate", htmlFor="installmentrate"),
                        dcc.Input(type="number",id="installmentrate",  className="form-control", placeholder="enter the installmentrate"),
                        html.Small("enter the installmentrate", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("residencesince", htmlFor="residencesince"),
                        dcc.Input(type="number",id="residencesince",  className="form-control", placeholder="enter the residencesince"),
                        html.Small("enter the residencesince", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("age", htmlFor="age"),
                        dcc.Input(type="number",id="age",  className="form-control", placeholder="enter the age"),
                        html.Small("enter the age", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("existingcredits", htmlFor="existingcredits"),
                        dcc.Input(type="number",id="existingcredits",  className="form-control", placeholder="enter the existingcredits"),
                        html.Small("enter the existingcredits", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("peopleliable", htmlFor="peopleliable"),
                        dcc.Input(type="number",id="peopleliable",  className="form-control", placeholder="enter the peopleliable"),
                        html.Small("enter the peopleliable", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("existingchecking", htmlFor="existingchecking"),
                        dcc.Dropdown(id="existingchecking",className="col-12 p-0", options=[
                            {'label':'A11', 'value':'A11'},
                            {'label':'A12', 'value':'A12'},
                            {'label':'A13', 'value':'A13'},
                            {'label':'A14', 'value':'A14'}
                        ]),
                        html.Small("select a existingchecking", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("credithistory", htmlFor="credithistory"),
                        dcc.Dropdown(id="credithistory",className="col-12 p-0", options=[
                            {'label':'A30', 'value':'A30'},
                            {'label':'A31', 'value':'A31'},
                            {'label':'A32', 'value':'A32'},
                            {'label':'A33', 'value':'A33'},
                            {'label':'A34', 'value':'A34'},
                        ]),
                        html.Small("select a credit history", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("purpose", htmlFor="purpose"),
                        dcc.Dropdown(id="purpose",className="col-12 p-0", options=[
                            {'label':'A40', 'value':'A40'},
                            {'label':'A41', 'value':'A41'},
                            {'label':'A42', 'value':'A42'},
                            {'label':'A43', 'value':'A43'},
                            {'label':'A44', 'value':'A44'},
                            {'label':'A45', 'value':'A45'},
                            {'label':'A46', 'value':'A46'},
                            {'label':'A47', 'value':'A47'},
                            {'label':'A48', 'value':'A48'},
                            {'label':'A49', 'value':'A49'},
                            {'label':'A410', 'value':'A410'}, 
                                                                                                                                                                                                                                
                        ]),
                        html.Small("select a purpose", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("savings", htmlFor="savings"),
                        dcc.Dropdown(id="savings",className="col-12 p-0", options=[
                            {'label':'A61', 'value':'A61'},
                            {'label':'A62', 'value':'A62'},
                            {'label':'A63', 'value':'A63'},
                            {'label':'A64', 'value':'A64'},
                            {'label':'A65', 'value':'A65'}                                                                                                                                                                         
                        ]),
                        html.Small("select a savings", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("employmentsince", htmlFor="employmentsince"),
                        dcc.Dropdown(id="employmentsince",className="col-12 p-0", options=[
                            {'label':'A71', 'value':'A71'},
                            {'label':'A72', 'value':'A72'},
                            {'label':'A73', 'value':'A73'},
                            {'label':'A74', 'value':'A74'},
                            {'label':'A75', 'value':'A75'}                                                                                                                                                                         
                        ]),
                        html.Small("select a employmentsince", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("statussex", htmlFor="statussex"),
                        dcc.Dropdown(id="statussex",className="col-12 p-0", options=[
                            {'label':'A91', 'value':'A91'},
                            {'label':'A92', 'value':'A92'},
                            {'label':'A93', 'value':'A93'},
                            {'label':'A94', 'value':'A94'},                                                                                                                                                                        
                        ]),
                        html.Small("select a statussex", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("otherdebtors", htmlFor="otherdebtors"),
                        dcc.Dropdown(id="otherdebtors",className="col-12 p-0", options=[
                            {'label':'A101', 'value':'A101'},
                            {'label':'A102', 'value':'A102'},
                            {'label':'A103', 'value':'A103'},
                                                                                                                                                                       
                        ]),
                        html.Small("select a otherdebtors", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("property", htmlFor="property"),
                        dcc.Dropdown(id="property",className="col-12 p-0", options=[
                            {'label':'A121', 'value':'A121'},
                            {'label':'A122', 'value':'A122'},
                            {'label':'A123', 'value':'A123'},
                            {'label':'A124', 'value':'A124'},                                                                                                                                           
                        ]),
                        html.Small("select a property", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("otherinstallmentplans", htmlFor="otherinstallmentplans"),
                        dcc.Dropdown(id="otherinstallmentplans",className="col-12 p-0", options=[
                            {'label':'A141', 'value':'A141'},
                            {'label':'A142', 'value':'A142'},
                            {'label':'A143', 'value':'A143'},                                                                                                                                           
                        ]),
                        html.Small("select a otherinstallmentplans", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("housing", htmlFor="housing"),
                        dcc.Dropdown(id="housing",className="col-12 p-0", options=[
                            {'label':'A151', 'value':'A151'},
                            {'label':'A152', 'value':'A152'},
                            {'label':'A153', 'value':'A153'},                                                                                                                                           
                        ]),
                        html.Small("select a housing", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("job", htmlFor="job"),
                        dcc.Dropdown(id="job",className="col-12 p-0", options=[
                            {'label':'A171', 'value':'A171'},
                            {'label':'A172', 'value':'A172'},
                            {'label':'A173', 'value':'A173'},
                            {'label':'A174', 'value':'A174'},                                                                                                                                           
                        ]),
                        html.Small("select a job", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("telephone", htmlFor="telephone"),
                        dcc.Dropdown(id="telephone",className="col-12 p-0", options=[
                            {'label':'A191', 'value':'A191'},
                            {'label':'A192', 'value':'A192'},                                                                                                                                           
                        ]),
                        html.Small("select a telephone", className="text-muted")
                    ]),                  
                    html.Div(className="form-group col-6",children=[
                        html.Label("foreignworker", htmlFor="foreignworker"),
                        dcc.Dropdown(id="foreignworker",className="col-12 p-0", options=[
                            {'label':'A201', 'value':'A201'},
                            {'label':'A202', 'value':'A202'},                                                                                                                                           
                        ]),
                        html.Small("select a foreignworker", className="text-muted")
                    ]),                    
                    html.Div(className="form-group col-6",children=[
                        html.Label("method to test", htmlFor="method"),
                        dcc.Dropdown(id="method",  value="svm",className="col-12 p-0", options=[
                            {'label':'XGboost', 'value':0},
                            {'label':'Naive Bayes', 'value':1},
                            {'label':'Logistic Regression', 'value':2},
                            {'label':'ADAboost', 'value':3}
                        ]),
                        html.Small("select a method to test", className="text-muted")
                    ]),
                ], className="row"),
                html.Hr(),
                html.Button("valider", className="btn btn-success", id="action_3"),
                html.Div(className="alert alert-primary text-center mt-4", children="please enter data to test if u are a good clent :p ...", id="output_msg_3"),
                
                ]),
    ])

    ])

])


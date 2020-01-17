
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pickle
from pickle import load
from dash.dependencies import Input, Output
import numpy as np
import pandas

from app import app

with open ('../model.pkl','rb') as file:
    data = load(file)

layout3 = html.Div(className="container-fluid mb-4", children= [

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

        html.Div(className="row" ,children=[

        html.Div(id="divleft",className="col-6",children=[
            html.H3("scores d'accuracy pour chaque modele entrainé : ", className="col-11 offset-1 text-dark"),
            html.Hr(className="col-10 offset-1 mb-4"),
            html.Div(className="row",children=[
                html.Div(className="col-11 offset-1", children=[
                    html.Div(className="row", children=[
                        html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("KNN", className="text-muted"),
                    html.P(data[0][0],className="display-4 text-success " if data[0][0]>=0.8 else "display-4 text-warning")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("SVM", className="text-muted"),
                    html.P(data[1][0],className="display-4 text-success" if data[1][0]>=0.8 else "display-4 text-warning")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P(" Random Forest", className="text-muted"),
                    html.P(data[2][0],className="display-4 text-success" if data[2][0]>=0.8 else "display-4 text-warning")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("LGBM", className="text-muted"),
                    html.P(data[3][0],className="display-4 text-success" if data[3][0]>=0.8 else "display-4 text-warning")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("XGBoost", className="text-muted"),
                    html.P(data[4][0],className="display-4 text-success" if data[4][0]>=0.8 else "display-4 text-warning")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P(" Logistic Regression", className="text-muted"),
                    html.P(data[5][0],className="display-4 text-success" if data[5][0]>=0.8 else "display-4 text-warning")
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
                        {'x': data[0][1], 'y': data[0][2], 'type': 'scatter', 'name': 'KNN'},
                        {'x': data[1][1], 'y': data[1][2], 'type': 'scatter', 'name': 'SVM'},
                        {'x': data[2][1], 'y': data[2][2], 'type': 'scatter', 'name': 'RF'},
                        {'x': data[3][1], 'y': data[3][2], 'type': 'scatter', 'name': 'LGBM '},
                        {'x': data[4][1], 'y': data[4][2], 'type': 'scatter', 'name': 'XGB'},
                        {'x': data[5][1], 'y': data[5][2], 'type': 'scatter', 'name': 'LR'}

                    ],
                    'layout': {
                        'title': 'ROC courbe'
                    }
                }
             )
            ])


])
 ]),


        html.Div(className="col-6",children=[
                html.H3(className="text-dark col-11 offset-1 mt-1", children="Formulaire à remplir :"),
                html.Hr(className="col-11 offset-1"),
                html.Div(className="p-5 ml-5 shadow",children=[
                html.Form([
                    html.Div(className="form-group col-6",children=[
                        html.Label("LIMIT_Bal", htmlFor="LIMIT_Bal"),
                        dcc.Input(type="number",id="LIMIT_Bal", className="form-control", placeholder="enter the LIMIT_Bal value"),
                        html.Small("enter the LIMIT_Bal value", className="text-muted")
                    ]),


                    html.Div(className="form-group col-6",children=[
                        html.Label("Gender", htmlFor="Gender"),
                        dcc.Dropdown(id="Gender",  value="other",className="col-12 p-0", options=[
                            {'label':'H', 'value':1},
                            {'label':'F', 'value':2},
                        ]),
                        html.Small("select a Gender ", className="text-muted")
                    ]),



                    html.Div(className="form-group col-6",children=[
                        html.Label("EDUCATION", htmlFor="EDUCATION"),
                        dcc.Dropdown(id="EDUCATION",  value="other",className="col-12 p-0", options=[
                            {'label':'graduate school', 'value':1},
                            {'label':'university', 'value':2},
                            {'label':'high school', 'value':3},
                            {'label':'others', 'value':4},

                        ]),
                        html.Small("select a EDUCATION ", className="text-muted")
                    ]),


                    html.Div(className="form-group col-6",children=[
                        html.Label("MARRAIGE", htmlFor="MARRAIGE"),
                        dcc.Dropdown(id="MARRAIGE",  value="other",className="col-12 p-0", options=[
                            {'label':'married', 'value':1},
                            {'label':'single', 'value':2},
                            {'label':'others', 'value':3},

                        ]),
                        html.Small("select a MARRAIGE ", className="text-muted")
                    ]),


                    html.Div(className="form-group col-6",children=[
                        html.Label("AGE", htmlFor="AGE"),
                        dcc.Input(type="number",id="AGE",  className="form-control", placeholder="enter the AGE"),
                        html.Small("enter the AGE", className="text-muted")
                    ]),





                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_0", htmlFor="PAY_0"),
                        dcc.Dropdown(id="PAY_0",  value="other",className="col-12 p-0", options=[
                            {'label':'pay duly', 'value':-1},
                            {'label':'payment delay for 1 month', 'value':1},
                            {'label':'payment delay for 2 month', 'value':2},
                            {'label':'payment delay for 3 month', 'value':3},
                            {'label':'payment delay for 4 month', 'value':4},
                            {'label':'payment delay for 5 month', 'value':5},
                            {'label':'payment delay for 6 month', 'value':6},
                            {'label':'payment delay for 7 month', 'value':7},
                            {'label':'payment delay for 8 month', 'value':8},
                            {'label':'payment delay for 9 month', 'value':9},


                        ]),
                        html.Small("select a PAY_0 ", className="text-muted")
                    ]),


                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_2", htmlFor="PAY_2"),
                        dcc.Dropdown(id="PAY_2",  value="other",className="col-12 p-0", options=[
                            {'label':'pay duly', 'value':-1},
                            {'label':'payment delay for 1 month', 'value':1},
                            {'label':'payment delay for 2 month', 'value':2},
                            {'label':'payment delay for 3 month', 'value':3},
                            {'label':'payment delay for 4 month', 'value':4},
                            {'label':'payment delay for 5 month', 'value':5},
                            {'label':'payment delay for 6 month', 'value':6},
                            {'label':'payment delay for 7 month', 'value':7},
                            {'label':'payment delay for 8 month', 'value':8},
                            {'label':'payment delay for 9 month', 'value':9},


                        ]),
                        html.Small("select a PAY_2 ", className="text-muted")
                    ]),



                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_3", htmlFor="PAY_3"),
                        dcc.Dropdown(id="PAY_3",  value="other",className="col-12 p-0", options=[
                            {'label':'pay duly', 'value':-1},
                            {'label':'payment delay for 1 month', 'value':1},
                            {'label':'payment delay for 2 month', 'value':2},
                            {'label':'payment delay for 3 month', 'value':3},
                            {'label':'payment delay for 4 month', 'value':4},
                            {'label':'payment delay for 5 month', 'value':5},
                            {'label':'payment delay for 6 month', 'value':6},
                            {'label':'payment delay for 7 month', 'value':7},
                            {'label':'payment delay for 8 month', 'value':8},
                            {'label':'payment delay for 9 month', 'value':9},


                        ]),
                        html.Small("select a PAY_3 ", className="text-muted")
                    ]),




                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_4", htmlFor="PAY_4"),
                        dcc.Dropdown(id="PAY_4",  value="other",className="col-12 p-0", options=[
                            {'label':'pay duly', 'value':-1},
                            {'label':'payment delay for 1 month', 'value':1},
                            {'label':'payment delay for 2 month', 'value':2},
                            {'label':'payment delay for 3 month', 'value':3},
                            {'label':'payment delay for 4 month', 'value':4},
                            {'label':'payment delay for 5 month', 'value':5},
                            {'label':'payment delay for 6 month', 'value':6},
                            {'label':'payment delay for 7 month', 'value':7},
                            {'label':'payment delay for 8 month', 'value':8},
                            {'label':'payment delay for 9 month', 'value':9},


                        ]),
                        html.Small("select a PAY_4 ", className="text-muted")
                    ]),



                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_5", htmlFor="PAY_5"),
                        dcc.Dropdown(id="PAY_5",  value="other",className="col-12 p-0", options=[
                            {'label':'pay duly', 'value':-1},
                            {'label':'payment delay for 1 month', 'value':1},
                            {'label':'payment delay for 2 month', 'value':2},
                            {'label':'payment delay for 3 month', 'value':3},
                            {'label':'payment delay for 4 month', 'value':4},
                            {'label':'payment delay for 5 month', 'value':5},
                            {'label':'payment delay for 6 month', 'value':6},
                            {'label':'payment delay for 7 month', 'value':7},
                            {'label':'payment delay for 8 month', 'value':8},
                            {'label':'payment delay for 9 month', 'value':9},


                        ]),
                        html.Small("select a PAY_5 ", className="text-muted")
                    ]),




                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_6", htmlFor="PAY_6"),
                        dcc.Dropdown(id="PAY_6",  value="other",className="col-12 p-0", options=[
                            {'label':'pay duly', 'value':-1},
                            {'label':'payment delay for 1 month', 'value':1},
                            {'label':'payment delay for 2 month', 'value':2},
                            {'label':'payment delay for 3 month', 'value':3},
                            {'label':'payment delay for 4 month', 'value':4},
                            {'label':'payment delay for 5 month', 'value':5},
                            {'label':'payment delay for 6 month', 'value':6},
                            {'label':'payment delay for 7 month', 'value':7},
                            {'label':'payment delay for 8 month', 'value':8},
                            {'label':'payment delay for 9 month', 'value':9},


                        ]),
                        html.Small("select a PAY_6 ", className="text-muted")
                    ]),


                    html.Div(className="form-group col-6",children=[
                        html.Label("BILL_AMT1", htmlFor="BILL_AMT1"),
                        dcc.Input(type="number",id="BILL_AMT1",  className="form-control", placeholder="amount of bill statement in September"),
                        html.Small("amount of bill statement in September", className="text-muted")
                    ]),

                    html.Div(className="form-group col-6",children=[
                        html.Label("BILL_AMT2", htmlFor="BILL_AMT2"),
                        dcc.Input(type="number",id="BILL_AMT2",  className="form-control", placeholder="amount of bill statement in August"),
                        html.Small("amount of bill statement in August", className="text-muted")
                    ]),

                    html.Div(className="form-group col-6",children=[
                        html.Label("BILL_AMT3", htmlFor="BILL_AMT3"),
                        dcc.Input(type="number",id="BILL_AMT3",  className="form-control", placeholder="amount of bill statement in July"),
                        html.Small("amount of bill statement in July", className="text-muted")
                    ]),

                    html.Div(className="form-group col-6",children=[
                        html.Label("BILL_AMT4", htmlFor="BILL_AMT4"),
                        dcc.Input(type="number",id="BILL_AMT4",  className="form-control", placeholder="amount of bill statement in June"),
                        html.Small("amount of bill statement in June", className="text-muted")
                    ]),

                    html.Div(className="form-group col-6",children=[
                        html.Label("BILL_AMT5", htmlFor="BILL_AMT5"),
                        dcc.Input(type="number",id="BILL_AMT5",  className="form-control", placeholder="amount of bill statement in May"),
                        html.Small("amount of bill statement in May", className="text-muted")
                    ]),

                    html.Div(className="form-group col-6",children=[
                        html.Label("BILL_AMT6", htmlFor="BILL_AMT6"),
                        dcc.Input(type="number",id="BILL_AMT6",  className="form-control", placeholder="amount of bill statement in April"),
                        html.Small("amount of bill statement in April", className="text-muted")
                    ]),



                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_AMT1", htmlFor="PAY_AMT1"),
                        dcc.Input(type="number",id="PAY_AMT1",  className="form-control", placeholder="amount paid in September"),
                        html.Small("amount paid in September ", className="text-muted")
                    ]),


                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_AMT2", htmlFor="PAY_AMT2"),
                        dcc.Input(type="number",id="PAY_AMT2",  className="form-control", placeholder="amount paid in August"),
                        html.Small("amount paid in August ", className="text-muted")
                    ]),


                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_AMT3", htmlFor="PAY_AMT3"),
                        dcc.Input(type="number",id="PAY_AMT3",  className="form-control", placeholder="amount paid in July"),
                        html.Small("amount paid in July ", className="text-muted")
                    ]),


                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_AMT4", htmlFor="PAY_AMT4"),
                        dcc.Input(type="number",id="PAY_AMT4",  className="form-control", placeholder="amount paid in June"),
                        html.Small("amount paid in June", className="text-muted")
                    ]),



                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_AMT5", htmlFor="PAY_AMT5"),
                        dcc.Input(type="number",id="PAY_AMT5",  className="form-control", placeholder="amount paid in May"),
                        html.Small("amount paid in May ", className="text-muted")
                    ]),





                    html.Div(className="form-group col-6",children=[
                        html.Label("PAY_AMT6", htmlFor="PAY_AMT6"),
                        dcc.Input(type="number",id="PAY_AMT6",  className="form-control", placeholder="amount paid in April"),
                        html.Small("amount paid in April ", className="text-muted")
                    ]),




                    html.Div(className="form-group col-6",children=[
                        html.Label("method to test", htmlFor="method"),
                        dcc.Dropdown(id="method",  value="svm",className="col-12 p-0", options=[
                            {'label':'Random forest', 'value':2},
                            {'label':'SVM', 'value':3},
                            {'label':'KNN', 'value':4},
                            {'label':'logistic regression', 'value':5},
                            {'label':'xgboost', 'value':6},
                        ]),
                        html.Small("select a reason for the loan", className="text-muted")
                    ]),


                ], className="row"),
                html.Hr(),
                html.Button("valider", className="btn btn-success", id="action_3"),
               html.Div(className="alert alert-primary text-center mt-4", children="please enter data to test if u are a good clent :p ...", id="output_msg_3"),

            ])

        ])

    ])
])



@app.callback(Output("output_msg_3","children"),[Input("action_3","n_clicks")],[
    State("LIMIT_Bal","value"),
    State("Gender","value"),
    State("EDUCATION","value"),
    State("MARRAIGE","value"),
    State("AGE","value"),
    State("PAY_0","value"),
    State("PAY_2","value"),
    State("PAY_3","value"),
    State("PAY_4","value"),
    State("PAY_5","value"),
    State("PAY_6","value"),
    State("BILL_AMT1","value"),
    State("BILL_AMT2","value"),
    State("BILL_AMT3","value"),
    State("BILL_AMT4","value"),
    State("BILL_AMT5","value"),
    State("BILL_AMT6","value"),
    State("PAY_AMT1","value"),
    State("PAY_AMT2","value"),
    State("PAY_AMT3","value"),
    State("PAY_AMT4","value"),
    State("PAY_AMT5","value"),
    State("PAY_AMT6","value"),

    ])


def predict_customer(inp,LIMIT_Bal, Gender, EDUCATION, MARRAIGE, AGE, PAY_0, PAY_2, PAY_3, PAY_4, PAY_5, PAY_6, BILL_AMT1, BILL_AMT2, BILL_AMT3, BILL_AMT4, BILL_AMT5 ,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6):
    if inp is not None:
        df = np.array([LIMIT_Bal, Gender, EDUCATION, MARRAIGE, AGE, PAY_0, PAY_2, PAY_3, PAY_4, PAY_5, PAY_6, BILL_AMT1, BILL_AMT2, BILL_AMT3, BILL_AMT4, BILL_AMT5,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6]).reshape(1,23)

        print(df.shape)


        if  data[0][3].predict(df)==0:
            return "sorry you are a bad client :("
        else :
            return "felicitation! you have earned a loan from our bank"
    return "please enter data to test if u are a good clent :p ..."


@app.callback(Output("output_msg_3","className"),[Input("output_msg_3","children")])
def change_color(input1):
    if input1.startswith("please enter correct data"):
        return "alert alert-warning text-center mt-4 "

    if input1.startswith("sorry"):
        return "alert alert-danger text-center mt-4"

    if input1.startswith("felicitation"):
        return "alert alert-success text-center mt-4"

    return "alert alert-primary text-center mt-4"


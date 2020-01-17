import dash
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output, State
from app import  app

from pickle import load 
import pandas as pd
import numpy as np

with open ('../pickle.pckl','rb') as file:
    data = load(file)

with open('../acp.pckl','rb') as file:
    data_pca = load(file)

pca =data_pca[0]
marker = data_pca[1]
pca_components = data_pca[2]
pca_colnames = data_pca[3]

reason_encoders = data[0]
job_encoders = data[1]
scaler = data[7]




layout1= html.Div(className="container-fluid mb-4", children= [

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

    html.Div(className="row", children=[
        html.Div(id="divleft",className="col-6",children=[
            html.H3("scores d'accuracy pour chaque modele entrainé : ", className="col-11 offset-1 text-dark"),
            html.Hr(className="col-10 offset-1 mb-4"),
            html.Div(className="row",children=[
                html.Div(className="col-11 offset-1", children=[
                    html.Div(className="row", children=[
                        html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("Random Forest", className="text-muted"),
                    html.P(round(data[2][0],2),className="display-4 text-success" if round(data[2][0],2)>=0.9 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[2][3][0],2)), className="mb-0 mt-0 text-muted float-right")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("SVM", className="text-muted"),
                    html.P(round(data[3][0],2),className="display-4 text-success" if round(data[3][0],2)>=0.9 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[2][3][0],2)), className="mb-0 mt-0 text-muted float-right")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("KNN", className="text-muted"),
                    html.P(round(data[4][0],2),className="display-4 text-success" if round(data[4][0],2)>=0.9 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[2][3][0],2)), className="mb-0 mt-0 text-muted float-right")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("Logistic Regression", className="text-muted"),
                    html.P(round(data[5][0],2),className="display-4 text-success" if round(data[5][0],2)>=0.9 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[2][3][0],2)), className="mb-0 mt-0 text-muted float-right")
                ]),
                html.Div(className="col-3 m-2 pt-4 pb-4 shadow text-center",children=[
                    html.P("XGBoost", className="text-muted"),
                    html.P(round(data[6][0],2),className="display-4 text-success" if round(data[6][0],2)>=0.9 else "display-4 text-warning"),
                    html.Small(children ="auc: "+str(round(data[2][3][0],2)), className="mb-0 mt-0 text-muted float-right")
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
                        {'x': data[2][3][2], 'y': data[2][3][1], 'type': 'scatter', 'name': 'random forest'},
                        {'x': data[3][3][2], 'y': data[3][3][1], 'type': 'scatter', 'name': 'SVM'},
                        {'x': data[4][3][2], 'y': data[4][3][1], 'type': 'scatter', 'name': 'KNN'},
                        {'x': data[5][3][2], 'y': data[5][3][1], 'type': 'scatter', 'name': 'Logistic Regression'},
                        {'x': data[6][3][2], 'y': data[6][3][1], 'type': 'scatter', 'name': 'XGB'},
                    ],
                    'layout': {
                        'title': 'ROC courbe'
                    }
                }
             )
            ]),
            html.H3("Cercle du correlations", className="col-11 offset-1 text-dark mt-4"),
            html.Hr(className="col-10 offset-1 mb-5"),
            html.Div(className="shadow p-4 col-10 offset-1", children=[
                dcc.Graph(figure={
                    'data': [
                            {'x': [0, pca_components[0][i]], 'y': [0,pca_components[1][i]], 'type': 'scatter', 'name':pca_colnames[i]} for i in range(len(pca_components[0]))
                        ],
                        'layout': {
                            'title': 'Cercle du correlation',
                            'height':500
                        }
                    })
            ])
        ] 
        ),


        html.Div(className="col-6",children=[
                html.H3(className="text-dark col-11 offset-1 mt-1", children="Formulaire à remplir :"),
                html.Hr(className="col-11 offset-1"),
                html.Div(className="p-5 ml-5 shadow",children=[
                html.Form([
                    html.Div(className="form-group col-6",children=[
                        html.Label("loan", htmlFor="loan"),
                        dcc.Input(type="number",id="loan", className="form-control", placeholder="enter the loan value"),
                        html.Small("enter the loan value", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("mortdue", htmlFor="mortdue"),
                        dcc.Input(type="number",id="mortdue",  className="form-control", placeholder="enter the mortdue"),
                        html.Small("enter the mortdue", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("value", htmlFor="value"),
                        dcc.Input(type="number",id="value",  className="form-control", placeholder="enter the value"),
                        html.Small("enter the value", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("Reason", htmlFor="Reason"),
                        dcc.Dropdown(id="Reason",  value="other",className="col-12 p-0", options=[
                            {'label':'DebtCon', 'value':'DebtCon'},
                            {'label':'HomeImp', 'value':'HomeImp'},
                            {'label':'other', 'value':'other'},
                        ]),
                        html.Small("select a reason for the loan", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("job", htmlFor="job"),
                        dcc.Dropdown(id="job",value="Other",options=[
                            {"label":"Mgr", "value":"Mgr"},
                            {"label":"Office", "value":"Office"},
                            {"label":"ProfExe", "value":"ProfExe"},
                            {"label":"Sales", "value":"Sales"},
                            {"label":"Self", "value":"Self"},
                            {"label":"Other", "value":"Other"},
                            
                            ]),
                        html.Small("select yoour job", className="text-muted")
                    ]),
                    html.Div(className="form-group col-3",children=[
                        html.Label("yoj", htmlFor="yoj"),
                        dcc.Slider(id="yoj",  className="col-12 p-0 mb-3", min=0, max=40, step=1, tooltip={"always_visible":False,'placement':'right'}),
                        html.Small("years at current yoj", className="text-muted")
                    ]),
                    html.Div(className="form-group col-3",children=[
                        html.Label("derog", htmlFor="derog"),
                        dcc.Slider(id="derog",  className="col-12 p-0 mb-3", min=0, max=20, step=1, tooltip={"always_visible":False,'placement':'right'}),
                        html.Small("number of derog rappoerts", className="text-muted")
                    ]),
                    html.Div(className="form-group col-3",children=[
                        html.Label("clage", htmlFor="clage"),
                        dcc.Input(type="number",id="clage",  className="form-control", placeholder="enter the value"),
                        html.Small("enter clage", className="text-muted")
                    ]),
                    html.Div(className="form-group col-3",children=[
                        html.Label("delinq", htmlFor="delinq"),
                        dcc.Slider(id="delinq",  className="col-12 p-0 mb-3", min=0, max=40, step=1, tooltip={"always_visible":False,'placement':'right'}),
                        html.Small("number of delinq", className="text-muted")
                    ]),
                    html.Div(className="form-group col-3",children=[
                        html.Label("ninq", htmlFor="ninq"),
                        dcc.Slider(id="ninq",  className="col-12 p-0 mb-3", min=0, max=40, step=1, tooltip={"always_visible":False,'placement':'right'}),
                        html.Small("number of ninq", className="text-muted")
                    ]),
                    html.Div(className="form-group col-3",children=[
                        html.Label("clno", htmlFor="clno"),
                        dcc.Slider(id="clno",  className="col-12 p-0 mb-3", min=0, max=40, step=1, tooltip={"always_visible":False,'placement':'right'}),
                        html.Small("number of clno", className="text-muted")
                    ]),
                    html.Div(className="form-group col-6",children=[
                        html.Label("debtoinc", htmlFor="debtoinc"),
                        dcc.Input(type="number",id="debtoinc",  className="form-control", placeholder="enter the value"),
                        html.Small("enter debt to income ratio", className="text-muted")
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
                html.Button("valider", className="btn btn-success", id="action"),
                html.Div(className="alert alert-primary text-center mt-4", children="please enter data to test if u are a good clent :p ...", id="output_msg"),
                
                ]),

                html.H3(className="text-dark col-11 ml-5 mt-4", children="Analyse des Composants Principales:"),
                html.Hr(className="col-11 ml-5"),
                html.Div(className=" p-4 ml-5 mt-3 shadow", children=[
                dcc.Graph(figure={
                    'data': [
                            {'x': pca[marker==1][:,0], 'y': pca[marker==1][:,1], 'type': 'scatter', 'mode':'markers', 'name':'bad'},
                            {'x': pca[marker==0][:,0], 'y': pca[marker==0][:,1], 'type': 'scatter', 'mode':'markers', 'name':'good'}
                        ],
                        'layout': {
                            'title': 'PCA',
                            'height':500,
                            'xaxis':{'range':[-5,10]
                            }
                        }
                    })
                

        ])        
        
        ])
    ])
]
)


@app.callback(Output("output_msg","children"),[Input("action","n_clicks")],[
    State("loan","value"),
    State("mortdue","value"),
    State("value","value"),
    State("Reason","value"),
    State("job","value"),
    State("yoj","value"),
    State("derog","value"),
    State("clage","value"),
    State("delinq","value"),
    State("ninq","value"),
    State("clno","value"),
    State("debtoinc","value"),
    State("method","value")
    ])
def predict_customer(inp, loan, mortdue, value, Reason, job, yoj, derog, clage, delinq, ninq, clno, debtoinc,method):
    if inp is not None:
        if (loan is None ) or (mortdue is None and value is None) or (clage is None) or (debtoinc is None) :
            return "please enter correct data "
        reason_10=0
        reason_20=0
        if reason_encoders[Reason] == 10: 
            reason_10 =1
        if reason_encoders[Reason] == 20:  
            reason_20 =1
        job_0 =0
        job_1 =0
        job_2 =0
        job_3 =0
        job_4 =0
        if job_encoders[job] == 0:
            job_0 =1
        if job_encoders[job] == 1:
            job_1 =1
        if job_encoders[job] == 2:
            job_2 =1
        if job_encoders[job] == 3:
            job_3 =1
        if job_encoders[job] == 4:
            job_4 =1


        if yoj is None :
            yoj=0
        if derog is None :
            derog=0
        if delinq is None :
            delinq=0
        if ninq is None :
            ninq=0
        if clno is None :
            clno=0

        df = np.array([loan, mortdue, value, yoj, derog, delinq, clage, ninq, clno, debtoinc,reason_10, reason_20, job_0, job_1, job_2, job_3, job_4]).reshape(1,17)         
        df = pd.DataFrame( scaler.transform(df), columns=['LOAN', 'MORTDUE', 'VALUE', 'YOJ', 'DEROG','DELINQ', 'CLAGE', 'NINQ',    'CLNO', 'DEBTINC',  10, 20,0, 1,  2,  3,  4]) 
        
        if  data[method][1].predict(df)[0]==1:
            return "sorry you are a bad client :("  
        else :
            return "felicitation! you have earned a loan from our bank"    
    return "please enter data to test if u are a good clent :p ..."    

@app.callback(Output("output_msg","className"),[Input("output_msg","children")])
def change_color(input1):
    if input1.startswith("please enter correct data"):
        return "alert alert-warning text-center mt-4 " 
    
    if input1.startswith("sorry"):
        return "alert alert-danger text-center mt-4" 

    if input1.startswith("felicitation"):
        return "alert alert-success text-center mt-4" 
        
    return "alert alert-primary text-center mt-4"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle 
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, roc_auc_score, auc , roc_curve
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.svm import SVC
import xgboost
import time
#**********************************************************************************
data = pd.read_csv("Bank_of_America_data.csv")
data_bl = data.dropna()
features = data_bl.iloc[:,1:]
target = data_bl.iloc[:,0]

final_array = []
#**********************************************************************************
encoder = LabelEncoder()
one_hot_encoder = OneHotEncoder()
standard = StandardScaler()

rfc_params = {'max_features':range(1,13)}
knn_params = {'n_neighbors':np.arange(12)*2 +1}
log_params = {'C' : np.logspace(-5,5,40)}
svc_params = {'C' : np.logspace(-5,5,40),'gamma':[i for i in np.linspace(0.55,0.7,12)]}
lm_params={'alpha' : np.logspace(-5,5,40)}

rfc_gs_bl = GridSearchCV(RandomForestClassifier(),rfc_params, cv=5)
rfc_gs_fe = GridSearchCV(RandomForestClassifier(n_estimators=100),rfc_params, cv=5)

knn_gs_bl = GridSearchCV(KNeighborsClassifier(),knn_params, cv=5)
knn_gs_fe = GridSearchCV(KNeighborsClassifier(),knn_params, cv=5)

log_gs_bl = GridSearchCV(LogisticRegression(solver='lbfgs', max_iter=400),log_params, cv=5)
log_gs_fe = GridSearchCV(LogisticRegression(solver='lbfgs', max_iter=400),log_params, cv=5)

svc_gs_bl = GridSearchCV(SVC(),svc_params ,cv=5)
svc_gs_fe = GridSearchCV(SVC(),svc_params, cv=5, n_jobs=4)

ridge_gs = GridSearchCV(Ridge(),lm_params, cv=10)

#******************functions ****************************************************

def fit_model (model, X_train, y_train):
    model.fit(X_train,y_train)

def predict_model(model, X_test):
    return model.predict(X_test)

def score_model(model, prediction, y_test):
    return accuracy_score(y_test, prediction)

def predict_proba_model(model, X_test, proba):
    pred= model.predict_proba(X_test)
    pred[pred > proba]=1
    pred[pred <= proba]=0
    return pred[:,1]

def compete_model(model, X_train, y_train, X_test, y_test, proba=0.5):
    fit_model (model, X_train, y_train)
    try :
        print(confusion_matrix(y_test, predict_proba_model(model,X_test,proba), labels=[0,1]))
    except :
        print("proba is not available")
    pred = predict_model(model, X_test)
    fpr , tpr, threshold = roc_curve(y_test, pred, pos_label=1)
    return [score_model(model, pred, y_test), model.best_estimator_, pd.DataFrame(confusion_matrix(y_test, pred, labels=[0,1]), columns=['pred 0','pred 1'], index=[0,1]), [roc_auc_score(y_test, pred),tpr,fpr]]

#*****************************************************************************
ridge_gs.fit(data_bl.MORTDUE.values.reshape(-1,1),data_bl.VALUE)
lm = ridge_gs.best_estimator_
#value = mortdue* coef + intercept    
data_fe = data.dropna(thresh=5)
data_fe.REASON.fillna("other",inplace=True)
data_fe.JOB.fillna("Other",inplace=True)
data_fe.DEROG.fillna(0,inplace=True)
data_fe.YOJ.fillna(0,inplace=True)

#data_fe.CLNO.fillna(0,inplace=True)
data_fe.NINQ.fillna(0,inplace=True)
data_fe.DELINQ.fillna(0,inplace=True)

data_fe.CLAGE.fillna(data.CLAGE.mean(),inplace=True)
data_fe.DEBTINC.fillna(data.DEBTINC.mean(),inplace=True)
data_fe = data_fe[(~data_fe.MORTDUE.isna())|(~data_fe.VALUE.isna())]

data_fe.MORTDUE.fillna(data_fe.VALUE/lm.coef_ - lm.intercept_,inplace=True)
data_fe.VALUE.fillna(data_fe.MORTDUE*lm.coef_ + lm.intercept_, inplace=True)

#****************************************************************************
data_fe=data_fe.dropna()
features_fe=data_fe.iloc[:,1:]
target_fe=data_fe.iloc[:,0]

#***************************************************************************
reason_fe = pd.DataFrame(one_hot_encoder.fit_transform(features_fe.REASON.to_numpy().reshape(-1,1)).toarray(), index=features_fe.index,columns=[10,20,30]).drop(30,axis=1)
jobs_fe = pd.DataFrame(one_hot_encoder.fit_transform(features_fe.JOB.to_numpy().reshape(-1,1)).toarray(),index=features_fe.index).drop(5,axis=1)
features_fe_numeric = pd.concat([features_fe.drop(['REASON','JOB'],axis=1), reason_fe, jobs_fe],axis=1) 


#***************************************logging*********************************
reason_encodage = {}
for e in zip(pd.concat([features_fe.REASON,features_fe_numeric[[10,20]]],axis=1).groupby("REASON").first().values,pd.concat([features_fe.REASON,features_fe_numeric[[10,20]]],axis=1).groupby("REASON").first().index):
    try :
        reason_encodage[e[1]] = 10*(list(e[0]).index(1)+1)
    except:
        reason_encodage[e[1]] = 30
       
final_array.append(reason_encodage)
print(reason_encodage)  

job_encodage = {}
for e in zip(pd.concat([features_fe.JOB,features_fe_numeric[[0,1,2,3,4]]],axis=1).groupby("JOB").first().values,pd.concat([features_fe.JOB,features_fe_numeric[[0,1,2,3,4]]],axis=1).groupby("JOB").first().index):
    try :
        job_encodage[e[1]] = list(e[0]).index(1)
    except:
        job_encodage[e[1]] = 5

final_array.append(job_encodage)
print(job_encodage)  

#*******************************************************scaling and selecting *******************************
features_fe_numeric = pd.DataFrame(standard.fit_transform(features_fe_numeric), columns=features_fe_numeric.columns, index=features_fe_numeric.index)

X_train_fe, X_test_fe, y_train_fe, y_test_fe =  train_test_split(features_fe_numeric, target_fe,test_size=0.25)


#***************************************testing *********************************

print ("started :"+str(time.time()))

final_array.append(compete_model(rfc_gs_fe, X_train_fe, y_train_fe, X_test_fe, y_test_fe))
final_array.append(compete_model(svc_gs_fe, X_train_fe, y_train_fe, X_test_fe, y_test_fe))
final_array.append(compete_model(knn_gs_fe, X_train_fe, y_train_fe, X_test_fe, y_test_fe))
final_array.append(compete_model(log_gs_fe, X_train_fe, y_train_fe, X_test_fe, y_test_fe))
#********************************************xg boost ***************************************
data_xg = data.dropna(thresh=5)
data_xg.REASON.fillna("other",inplace=True)
data_xg.JOB.fillna("Other",inplace=True)

features_xg=data_xg.iloc[:,1:]
target_xg=data_xg.iloc[:,0]

reason_fe = pd.DataFrame(one_hot_encoder.fit_transform(features_xg.REASON.to_numpy().reshape(-1,1)).toarray(), index=features_xg.index,columns=[10,20,30]).drop(30,axis=1)
jobs_fe = pd.DataFrame(one_hot_encoder.fit_transform(features_xg.JOB.to_numpy().reshape(-1,1)).toarray(),index=features_xg.index).drop(5,axis=1)
features_xg_numeric = pd.concat([features_xg.drop(['REASON','JOB'],axis=1), reason_fe, jobs_fe],axis=1) 

X_train_xg, X_test_xg, y_train_xg, y_test_xg =  train_test_split(features_xg_numeric, target_xg, test_size=0.25)

xgb_params={ 'reg_alpha': [0.1e-2 ,0.1e-1, 0.1,1]}

xgb_gs = GridSearchCV(xgboost.XGBClassifier(colsample_bytree= 0.357, subsample= 0.67,learning_rate=0.3,n_estimators=1000,max_depth=5, min_child_weight=1 ,n_jobs=4),xgb_params, cv=5)

final_array.append(compete_model(xgb_gs, X_train_xg, y_train_xg, X_test_xg, y_test_xg))



print ("finished :"+str(time.time()))

final_array.append(standard)

with open('pickle.pckl','wb') as file:
    pickle.dump(final_array,file)

print(final_array)
print(X_train_fe.index)
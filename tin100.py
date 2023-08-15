### Importering av moduler

import pandas as pd
from sklearn.imputer import SimpleImputer
import numpy as np
from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

### Split datasett i train og test

train_raw = pd.read_csv("train.csv")
test_raw = pd.read_csv("test.csv")
train = train_raw.drop(['Loan_ID'], axis=1)
test = test_raw.drop(['Loan_ID'], axis=1)

simp = SimpleImputer(missing_values=np.nan, strategy='most_frequent')


def add_values(var):
    for col in var.columns:
        simp_1 = simp.fit(var[[f'{col}']])
        var[f'{col}'] = simp_1.transform(var[[f'{col}']])
    return var


train = add_values(train)
test = add_values(test)

le = LabelEncoder()
for col in train[
    ['Gender', 'Married', 'Education', 'Self_Employed', 'Dependents', 'Property_Area', 'Credit_History',
     'Loan_Status']]:
    # print(col)
    train[col] = le.fit_transform(train[col])

train['CoapplicantIncome'] = train['CoapplicantIncome'].astype('int')
# train.head()

le = LabelEncoder()
for col in test[
    ['Gender', 'Married', 'Education', 'Self_Employed', 'Dependents', 'Credit_History', 'Property_Area']]:
    # print(col)
    test[col] = le.fit_transform(test[col])

test['CoapplicantIncome'] = test['CoapplicantIncome'].astype('int')

x = train.drop('Loan_Status', axis=1)
y = train['Loan_Status']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, stratify=y)


### Randomforest classifier

def RanForClf():
    parameter_grid = {
        'n_estimators': [200, 300, 400],
        'max_features': ['auto', 'sqrt'],
        'max_depth': [5, 6, 7, 8],
        'criterion': ['gini', 'entropy']
    }
    rfc = RandomForestClassifier(random_state=42)
    CV_rfc = GridSearchCV(estimator=rfc, param_grid=parameter_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)
    CV_rfc.fit(x, y)
    return CV_rfc


def predic(x, model):
    return model.predict(x)


### Predict of the whole datasett
if __name__ == "__main__":

    model = RanForClf()
    pred = model.predict(test)

    test['Loan_Status'] = pred

    ### Creating a new column with 5* total income < loan

    New_loan_status = []
    for i in range(len(test)):
        if test.iloc[i]['Loan_Status'] == 0:
            # print('hei')
            income = 5 * 12 * (test.iloc[i]['ApplicantIncome'] + test.iloc[i]['CoapplicantIncome'])
            loan = (test.iloc[i]['LoanAmount']) * 1000
            New_loan_status.append(income < loan)
        else:
            New_loan_status.append(1)

    test['new_loan_status'] = New_loan_status

    df = test['Loan_Status']
    df.value_counts()

    df = test['new_loan_status']
    df.value_counts()
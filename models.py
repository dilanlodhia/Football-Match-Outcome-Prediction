#%%
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import scale
import numpy as np
import pandas as pd
from edit_df import df_edit

data = df_edit()

cols = ['Home_Team_ELO', 'Away_Team_ELO', 'Home_Shots',
       'Away_Shots', 'Home_Shot_Accuracy', 'Away_Shot_Accuracy',
       'Home_Possession', 'Away_Possession', 'Home_Total_Passes',
       'Away_Total_Passes', 'Home_Successful_Pass_Avg', 'Away_Successful_Pass_Avg']

for col in cols:
    data[col] = scale(data[col])

X = data[cols].to_numpy()

y = data['Winner'].to_numpy()
# print(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)
y_pred = log_reg.predict(X_test)
print(accuracy_score(y_test, y_pred))
print('y_test: ', y_test)
print('y_pred: ', y_pred)

# %%

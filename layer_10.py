# -*- coding: utf-8 -*-
"""Layer_10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NXzkt-Dj4XIXpmg_n4mjK2_L1LMXKrQU
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
import warnings
warnings.filterwarnings("ignore")

train = pd.read_csv('/content/drive/MyDrive/ML Module/ML Mini Project/Data/L10/train.csv')
test = pd.read_csv('/content/drive/MyDrive/ML Module/ML Mini Project/Data/L10/test.csv')
valid = pd.read_csv('/content/drive/MyDrive/ML Module/ML Mini Project/Data/L10/valid.csv')

# Find columns with missing values and count how many missing values in each column
missing_columns = train.columns[train.isnull().any()]
missing_counts = train[missing_columns].isnull().sum()

# Print the columns with missing values and their corresponding missing value counts
print("shape of train: ", train.shape)
for column in missing_columns:
    print(f"Column '{column}' has {missing_counts[column]} missing values.")

from google.colab import drive
drive.mount('/content/drive')

L1 = "label_1" #Speaker ID
L2 = "label_2" #Speaker age
L3 = "label_3" #Speaker gender
L4 = "label_4" #Speaker accent
LABELS = [L1, L2, L3, L4,]
AGE_LABEL = L2
FEATURES = [f'feature_{i}' for i in range(1,769)]

train_df = train.copy()
test_df = test.copy()
valid_df = valid.copy()

train_df.head()

train_df[LABELS + [FEATURES[i] for i in range(0,768)]].describe()

# @title **Scaling and Eliminating Outliers**
from sklearn.preprocessing import RobustScaler

x_train = {}
x_valid = {}
x_test = {}

y_train = {}
y_valid = {}
y_test = {}

#create dictionaries for each label
for target_label in LABELS:
  tr_df = train_df[train_df['label_2'].notna()] if target_label == "label_2" else train_df
  vl_df = valid_df[valid_df['label_2'].notna()] if target_label == "label_2" else valid_df
  te_df = test_df

  scaler = RobustScaler()

  x_train[target_label] = pd.DataFrame(scaler.fit_transform(tr_df.drop(LABELS, axis=1)), columns=FEATURES)
  y_train[target_label] = tr_df[target_label]

  x_valid[target_label] = pd.DataFrame(scaler.transform(vl_df.drop(LABELS, axis=1)), columns=FEATURES)
  y_valid  [target_label] = vl_df[target_label]

  x_test[target_label] = pd.DataFrame(scaler.transform(te_df.drop(['ID'], axis=1)), columns=FEATURES)

# @title **Assigning Label**

train_label = 'label_1'

x_train_df = x_train[train_label].copy()
y_train_df = y_train[train_label].copy()

x_valid_df = x_valid[train_label].copy()
y_valid_df = y_valid[train_label].copy()

x_test_df = x_test[train_label].copy()

from sklearn.utils import class_weight
from sklearn import metrics
from sklearn.metrics import classification_report, f1_score
from sklearn.metrics import confusion_matrix

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

"""### **Test before Feature Engineering**"""

classifier = svm.SVC(kernel='rbf')
classifier.fit(x_train_df, y_train_df)

y_pred = classifier.predict(x_valid_df)

print("accuracy_score: ",metrics.accuracy_score(y_valid_df, y_pred))
print("f1_score: ",f1_score(y_valid_df, y_pred, average='weighted'))
print("precision_score: ",metrics.precision_score(y_valid_df, y_pred, average='weighted' ))
print("recall_score: ",metrics.recall_score(y_valid_df, y_pred, average='weighted'))

"""### **FEATURE ENGINEERING**"""

# @title 1. Feature selection using SelectKBest and f_classif
from sklearn.feature_selection import SelectKBest, f_classif

selector = SelectKBest(f_classif, k=150)
x_train_df_after_f_classif = selector.fit_transform(x_train_df, y_train_df)
x_valid_df_after_f_classif = selector.transform(x_valid_df)
print("shape: ", x_train_df_after_f_classif.shape)

x_test_df_after_f_classif = selector.transform(x_test_df)

# @title 2. PCA for feature engineering
from sklearn.decomposition import PCA

pca = PCA(n_components=0.98, svd_solver='full')
pca.fit(x_train_df)
x_new = pd.DataFrame(pca.transform(x_train_df))
x_valid_trf_pca = pd.DataFrame(pca.transform(x_valid_df))
print('Shape after PCA: ',x_new.shape)

x_test_df_final = pd.DataFrame(pca.transform(x_test_df))

"""### **Model Evaluation (Without Hyper-parameter Tuning)**"""

# @title 1. SVM

svm_clf = svm.SVC(kernel="rbf", class_weight='balanced')
svm_clf.fit( x_new, y_train_df)

y_pred = svm_clf.predict(x_valid_trf_pca)

print("accuracy_score: ",metrics.accuracy_score(y_valid_df, y_pred))
print("f1_score: ",f1_score(y_valid_df, y_pred, average='weighted'))
print("precision_score: ",metrics.precision_score(y_valid_df, y_pred, average='weighted' ))
print("recall_score: ",metrics.recall_score(y_valid_df, y_pred, average='weighted'))

# @title 2. K-NN

k = 5  # Number of neighbors
knn_clf = KNeighborsClassifier(n_neighbors=k)

knn_clf.fit(x_new, y_train_df)
y_pred = knn_clf.predict(x_valid_trf_pca)

print("accuracy_score: ",metrics.accuracy_score(y_valid_df, y_pred))
print("f1_score: ",f1_score(y_valid_df, y_pred, average='weighted'))
print("precision_score: ",metrics.precision_score(y_valid_df, y_pred, average='weighted' ))
print("recall_score: ",metrics.recall_score(y_valid_df, y_pred, average='weighted'))

# @title 3. Random Forest

n = 60  # Number of estimators
rf_clf = RandomForestClassifier(n_estimators=n)

rf_clf.fit(x_new, y_train_df)
y_pred = rf_clf.predict(x_valid_trf_pca)

print("accuracy_score: ",metrics.accuracy_score(y_valid_df, y_pred))
print("f1_score: ",f1_score(y_valid_df, y_pred, average='weighted'))
print("precision_score: ",metrics.precision_score(y_valid_df, y_pred, average='weighted' ))
print("recall_score: ",metrics.recall_score(y_valid_df, y_pred, average='weighted'))

"""### **Hyper-parameter Tuning**"""

from sklearn.model_selection import RandomizedSearchCV

svm_clf = svm.SVC()

param_grid = {
    'C': [0.1,1],           # Uniform distribution between 0 and 10
    'gamma': [0.001, 1],           # Log-uniform distribution between 0.001 and 1
    'kernel': ['rbf'],
    'degree': [1,2]
}

grid_search = RandomizedSearchCV(svm_clf, param_distributions=param_grid, n_iter=2, cv=5, verbose=1, n_jobs=-1)
grid_search.fit(x_new, y_train_df)

grid_search.best_estimator_

y_pred = grid_search.best_estimator_.predict(x_valid_trf_pca)

print("accuracy_score: ",metrics.accuracy_score(y_valid_df, y_pred))
print("f1_score: ",f1_score(y_valid_df, y_pred, average='weighted'))
print("precision_score: ",metrics.precision_score(y_valid_df, y_pred, average='weighted' ))
print("recall_score: ",metrics.recall_score(y_valid_df, y_pred, average='weighted'))

"""# **Final Predictions and Results**"""

y_test_pred = grid_search.best_estimator_.predict(x_test_df_final)

csv_file = "/content/drive/MyDrive/ML Mini Project/NoteBook/190530H_submission_Layer10.csv"
dataframe = pd.read_csv(csv_file)
dataframe[train_label] = y_test_pred
dataframe.to_csv(csv_file,index=False)
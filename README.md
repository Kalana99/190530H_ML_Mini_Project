# 190530H_ML_Mini_Project

## Overview

Dataset: AudioMNIST is the dataset used to create the features. Check this link for further
details about the dataset Link.

This project has two phases:

1. Individual task - Classification model development and Kaggle competition for each assigned layer.
2. Group submission - 6-page research paper

The above notebooks provide classification models for **Layer 09** and **Layer 10**.

## Data Pre-processing and Feature Engineering Steps

- Load data sets from the Google Drive.
- Identify labels with missing values.
- Drop the entries with missing values and Scale for each label to handle outliers.
- Create dictionaries for each label using Train, Valid, and Test data sets.
- Apply feature selection using **SelectKBest** and **f_classif**.
- Conduct PCA analysis.

## Training the Final Model

- **SVM**, **K-NN**, and **Random Forest** are considered possible candidates for the classifier model. Each of these models is tested with pre-processed data. Based on the results, SVM stands out as the most suitable model.
- **Hyper-parameter Tuning** is conducted using a **Random Grid Search** for an SVM instance. The resulting best estimator is used to predict the labels using the Test dataset.
- The result is written into a CSV file in the required format.

*The above operation sequence is carried out for each label separately by changing the label in the **“Assigning Labels”** cell.*

```Python
# @title **Assigning Label**

train_label = 'label_X'

x_train_df = x_train[train_label].copy()
y_train_df = y_train[train_label].copy()

x_valid_df = x_valid[train_label].copy()
y_valid_df = y_valid[train_label].copy()

x_test_df = x_test[train_label].copy()
```

Replace **X** with **1, 2, 3** or **4** based on the label that needs to be predicted

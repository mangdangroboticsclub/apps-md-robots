#
# Description: This script is designed to train AI model for gesture detection
# 

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import itertools

def load_data(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

def convert_dict_to_arrays(data_dict):
    data = []
    labels = []
    for img_path, landmarks in data_dict.items():
        data.append(np.array(landmarks).flatten())
        labels.append(img_path.split("/")[-2])
    return np.asarray(data), np.asarray(labels)

def split_data(data, labels, test_size=0.2):
    if len(data) == 0 or len(labels) == 0:
        raise ValueError("No data available to split.")
    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=test_size, shuffle=True, stratify=labels)
    return x_train, x_test, y_train, y_test

def tune_hyperparameters(x_train, y_train):
    # param_grid = {
    #     'learning_rate': [0.1],
    #     'n_estimators': [200],
    #     'max_depth': [7],
    #     'subsample': [1.0],
    #     'colsample_bytree': [1.0],
    #     'tree_method': ['hist'],
    # }
    xgb = XGBClassifier(objective='multi:softprob', eval_metric='mlogloss', n_jobs=1, random_state=42)
    # grid_search = GridSearchCV(estimator=xgb, param_grid=param_grid, cv=3, n_jobs=1, verbose=2, scoring='accuracy', error_score='raise')
    xgb.fit(x_train, y_train)
    # print("Best parameters found: ", grid_search.best_params_)
    # print("Best cross-validation score: {:.2f}".format(grid_search.best_score_))
    return xgb

def evaluate_model(model, x_test, y_test):
    y_predict = model.predict(x_test)
    accuracy = accuracy_score(y_predict, y_test)
    report = classification_report(y_test, y_predict)
    matrix = confusion_matrix(y_test, y_predict)
    return accuracy, report, matrix

def plot_confusion_matrix(matrix, labels, title='Confusion Matrix'):
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)
    thresh = matrix.max() / 2.
    for i, j in itertools.product(range(matrix.shape[0]), range(matrix.shape[1])):
        plt.text(j, i, format(matrix[i, j], 'd'), horizontalalignment="center", color="white" if matrix[i, j] > thresh else "black")
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

def plot_metrics(matrix, labels, accuracy, report):
    plt.figure(figsize=(10,5))
    plot_confusion_matrix(matrix, labels)
    plt.show()
    print(f"Classification Accuracy: {accuracy*100:.2f}%")
    print("\nClassification Report:\n", report)

def save_model(model, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump({'model': model}, f)
    
try:
    data_dict = load_data('/Users/soumikbarua/Documents/MangDang Technology Limited/Gesture Recognition/facial-expression-recognition/data.pickle')
    if not data_dict:
        raise ValueError("The data dictionary is empty.")
    data, labels = convert_dict_to_arrays(data_dict)
    if data.size == 0 or labels.size == 0:
        raise ValueError("Converted data or labels are empty.")
    print(f"Number of samples: {data.shape[0]}")
    label_encoder = LabelEncoder()
    labels_encoded = label_encoder.fit_transform(labels)
    label_classes = label_encoder.classes_
    x_train, x_test, y_train, y_test = split_data(data, labels_encoded)
    best_model = tune_hyperparameters(x_train, y_train)
    accuracy, report, matrix = evaluate_model(best_model, x_test, y_test)
    plot_metrics(matrix, label_classes, accuracy, report)
    print(f"Accuracy: {accuracy}")
    save_model(best_model, '../models/model.p')
    print("Model saved!")
except Exception as e:
    print("An error occurred:", str(e))

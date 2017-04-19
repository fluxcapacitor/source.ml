import sys
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
import dill as pickle

my_model = None

def train():
    print("Training model...")

    training_data = pd.read_csv('model_training.csv', sep=',', header=None)

    X = training_data.values[:, 1:5]
    Y = training_data.values[:, 0]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)

    global my_model
    my_model = DecisionTreeClassifier(criterion="gini", random_state=100, max_depth=3, min_samples_leaf=5)
    my_model.fit(X_train, y_train)

    print("...Done!")


def predict(inputs):
    global my_model

    return my_model.predict_proba(inputs)


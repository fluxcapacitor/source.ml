import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier

model = None

def train():
    training_data = pd.read_csv('model_training.csv', sep=',', header=None)

    X = training_data.values[:, 1:5]
    Y = training_data.values[:, 0]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)

    global model
    model = DecisionTreeClassifier(criterion="gini", random_state=100, max_depth=3, min_samples_leaf=5)
    model.fit(X_train, y_train)

def predict(inputs):
    global model 
    return model.predict_proba(inputs)

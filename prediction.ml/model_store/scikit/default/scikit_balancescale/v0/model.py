import sys
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
import dill as pickle

class Predictor():
    def __init__(self, model):
        self.model = model

    def predict(self, inputs):
        return self.model.predict_proba(inputs)

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('model_pkl_filename')
    args = parser.parse_args()
    model_pkl_filename = args.model_pkl_filename

    print("Training model...")
    training_data = pd.read_csv('model_training.csv', sep=',', header=None)
    X = training_data.values[:, 1:5]
    Y = training_data.values[:, 0]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=100)
    model = DecisionTreeClassifier(criterion="gini", random_state=100, max_depth=3, min_samples_leaf=5)
    model.fit(X_train, y_train)
    print("...Done!")

    print("Pickling model to '%s'..." % model_pkl_filename)
    predictor = Predictor(model) 
    with open(model_pkl_filename, 'wb') as model_pkl_file:
        pickle.dump(predictor, model_pkl_file)
    print("...Done!")

import sys
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import datasets
import dill as pickle

class Predictor(object):

    def __init__(self, model):
        self.model = model


    def setup(self):
        pass


    def predict(self, inputs):
        return self.model.predict(inputs)


if __name__ == '__main__':

    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('model_pkl_filename')
    args = parser.parse_args()
    model_pkl_filename = args.model_pkl_filename

    print("Training model...")

    # Load the diabetes dataset
    diabetes = datasets.load_diabetes()

    # ONLY USING 1 FEATURE FOR THIS EXAMPLE!
    # Use only one feature
    diabetes_X = diabetes.data[:, np.newaxis, 2]

    # Split the data into training/testing sets
    diabetes_X_train = diabetes_X[:-20]
    diabetes_X_test = diabetes_X[-20:]

    # Split the targets into training/testing sets
    diabetes_y_train = diabetes.target[:-20]
    diabetes_y_test = diabetes.target[-20:]

    # Create linear regression model
    model = linear_model.LinearRegression()

    # Train the model using the training sets
    model.fit(diabetes_X_train, diabetes_y_train)
    print("...Done!")

    print("Pickling model to '%s'..." % model_pkl_filename)
    predictor = Predictor(model) 
    with open(model_pkl_filename, 'wb') as model_pkl_file:
        pickle.dump(predictor, model_pkl_file)
    print("...Done!")

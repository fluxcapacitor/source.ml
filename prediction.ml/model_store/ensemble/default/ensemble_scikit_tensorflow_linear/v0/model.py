import sys
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import datasets
import dill as pickle

# TODO:  Coming Soon!

class Predictor():

    def __init__(self, models, agg_fn):
        self.models = models
        self.agg_fn = agg_fn

        # load scikit
        with open(model_filename, 'rb') as fh:
            model = pickle.load(fh)

        # load tensorflow
        tensorflow_model_path = "."
        with tf.Session(graph=tf.Graph()) as sess:
            tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], tensorflow_model_path)


    def predict(self, inputs):
        # TODO:  Parallelize this
        outputs = []

        for model in self.models:
        # TODO: append to list of outputs
            #outputs.append(self.model.predict(inputs))
        
        # TODO: aggregate outputs using agg_fn.agg()
#        return agg_fn.agg(outputs)
        return 1.0
                    

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

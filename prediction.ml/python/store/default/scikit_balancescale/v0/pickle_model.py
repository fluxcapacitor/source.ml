import json
import dill as pickle

import model

if __name__ == '__main__':
    model.train()

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('model_pkl_filename')
    args = parser.parse_args()

    model_pkl_filename = args.model_pkl_filename

    print("Pickling model '%s'..." % model_pkl_filename)

    # pickle the entire `model` module imported above 
    # Note:  this must contain predict(inputs) method
    with open(model_pkl_filename, 'wb') as model_pkl_file:
        pickle.dump(model, model_pkl_file)

    print("...Done!")

import sys
import dill as pickle

import model

if __name__ == '__main__':
    print("Training model...")

    model.train()

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('model_pkl_filename')
    args = parser.parse_args()

    model_pkl_filename = args.model_pkl_filename

    print("Pickling model to '%s'..." % model_pkl_filename)

    # Pickle the entire `model` module imported above 
    # Note:  this must contain predict(inputs) method
    with open(model_pkl_filename, 'wb') as model_pkl_file:
        pickle.dump(sys.modules['model'], model_pkl_file)

    print("...Done!")

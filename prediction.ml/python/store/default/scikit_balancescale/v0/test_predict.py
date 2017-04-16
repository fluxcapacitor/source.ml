from __future__ import print_function, absolute_import, division

import sys
import pickle
import ujson
import pandas as pd
from io_transformers import input_transformer, output_transformer

def test(model_filename, test_input_filename, test_output_filename):
    with open(model_filename, 'rb') as fh:
        model = pickle.load(fh)
    with open(test_input_filename, 'rb') as fh:
        data = fh.read() 
    with open(test_output_filename, 'rb') as fh:
        expected_output = fh.read()
#    print(expected_output)

    df = input_transformer(data)
    actual_output = model.predict(df)
#    print(actual_output)
    actual_output = output_transformer(actual_output)
#    print(actual_output)
    return (expected_output.decode('utf-8').strip() == actual_output.strip())

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('model_filename')
    parser.add_argument('test_input_filename')
    parser.add_argument('test_output_filename')
    args = parser.parse_args()

    print('TESTS PASSED:  %s' % test(args.model_filename, args.test_input_filename, args.test_output_filename))

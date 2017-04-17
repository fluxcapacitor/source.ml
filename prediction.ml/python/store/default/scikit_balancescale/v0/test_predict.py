from __future__ import print_function, absolute_import, division

import json
import importlib
import dill as pickle

def test(model_filename, test_input_filename, test_output_filename):
    with open(model_filename, 'rb') as fh:
        model = pickle.load(fh)
    with open(test_input_filename, 'rb') as fh:
        actual_input = fh.read() 
    with open(test_output_filename, 'rb') as fh:
        expected_output = fh.read()
    print(expected_output)

    # Load io_transformers module
    transformers_module_name = 'io_transformers'
    spec = importlib.util.spec_from_file_location(transformers_module_name, '%s.py' % transformers_module_name)
    transformers_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(transformers_module)

    actual_transformed_input = transformers_module.transform_inputs(actual_input)
    actual_output = model.predict(actual_transformed_input)
    actual_transformed_output = transformers_module.transform_outputs(actual_output)
    print(actual_transformed_output)

    return (json.loads(expected_output.decode('utf-8').strip())
        == json.loads(actual_transformed_output.strip()))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('model_filename')
    parser.add_argument('test_input_filename')
    parser.add_argument('test_output_filename')
    args = parser.parse_args()
    print('')
    print('TESTS PASSED:  %s' % test(args.model_filename, args.test_input_filename, args.test_output_filename))
    print('')

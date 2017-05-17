from __future__ import print_function, absolute_import, division

import json
import importlib
import tensorflow as tf


TODO:  FIX THIS!!


def test(test_input_filename, test_output_filename):
    model_path = '.'
    with open(test_input_filename, 'rb') as fh:
        actual_input = fh.read()
    with open(test_output_filename, 'rb') as fh:
        expected_output = fh.read()

    # Load io_transformers module
    transformers_module_name = 'model_io_transformers'
    spec = importlib.util.spec_from_file_location(transformers_module_name, '%s.py' % transformers_module_name)
    transformers_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(transformers_module)
    actual_transformed_input = transformers_module.transform_inputs(actual_input)
    print(actual_transformed_input)

    #model.setup()

    with tf.Session(graph=tf.Graph()) as sess:
        tf.saved_model.loader.load(sess, [tf.saved_model.tag_constants.SERVING], model_path)   

        print('graph %s' % sess.graph)

        #x_observed = tf.placeholder(dtype=tf.float32,
        #                                  shape=[None, 1],
        #                                  name='x_observed')
        x_observed = sess.graph.get_tensor_by_name('x_observed:0')
        y_pred = sess.graph.get_tensor_by_name('add:0')        
        actual_output = sess.run(y_pred, feed_dict={'x_observed:0':actual_transformed_input.inputs['x_observed'].float_val})
        print('actual output: %s' % actual_output)
        print('actual output type: %s' % type(actual_output))
        #actual_output = model.predict(actual_transformed_input)
        hacked_actual_output = type('hacked_actual_output_obj', (object,), {'outputs' : actual_output}) 
        hacked_actual_output.outputs = {'y_pred': actual_output}
        actual_transformed_output = transformers_module.transform_outputs(hacked_actual_output)
             #json.dumps(actual_output.tolist())
        #transformers_module.transform_outputs(actual_output)
        # TODO:  add {"y_pred":...}
        print('actual transformed output: %s' % actual_transformed_output)
        print('expected: %s' % expected_output.decode('utf-8').strip())

    return (json.loads(expected_output.decode('utf-8').strip()) == json.loads(actual_transformed_output.strip()))

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('test_input_filename')
    parser.add_argument('test_output_filename')
    args = parser.parse_args()
    print('')
    print('TESTS PASSED:  %s' % test(args.test_input_filename, args.test_output_filename))
    print('')

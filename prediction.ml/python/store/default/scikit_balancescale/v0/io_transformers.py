from __future__ import print_function, absolute_import, division

import ujson
import numpy as np

# input: raw json
# output: numpy array
def transform_inputs(input_binary):
    input_str = input_binary.decode('utf-8')
    input_str = input_str.strip().replace('\n', ',')
    # surround the json with '[' ']' to prepare for conversion
    input_str = '[%s]' % input_str
    input_json = ujson.loads(input_str)

    input_transformed = ([parse_json_line(json_line) for json_line in input_json])
    return np.array(input_transformed)

def parse_json_line(json_line):
    return json_line['feature0'], json_line['feature1'], json_line['feature2'], json_line['feature3']

# input: numpy array
# output: list of json
def transform_outputs(output_np):
    return ujson.dumps(output_np.tolist())

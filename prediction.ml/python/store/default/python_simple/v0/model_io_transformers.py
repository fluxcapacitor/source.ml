from __future__ import print_function, absolute_import, division

import json

# input: raw json (binary)
# output: python dict 
def transform_inputs(input_binary):
    input_str = input_binary.decode('utf-8')
    input_str = input_str.strip().replace('\n', ',')
    input_dict = json.loads(input_str)
    return input_dict

# input: dict 
# output: json
def transform_outputs(output_dict):
    output_json = json.dumps(output_dict)
    return output_json

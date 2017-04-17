#!/bin/bash

echo "Testing model..."

source activate model_environment

export PIO_MODEL_FILENAME=$(ls *.pkl | sed -n 1p)

[ -s ./test_predict.py ] && python test_predict.py \
                                $PIO_MODEL_FILENAME \
                                "./test_inputs.txt" \
                                "./test_outputs.txt"
echo "...Done!"

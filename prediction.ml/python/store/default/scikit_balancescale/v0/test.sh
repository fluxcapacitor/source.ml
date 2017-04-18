#!/bin/bash

[ -s ./install.sh ] && ./install.sh

echo "Activating 'model_environment'..."
source activate model_environment
echo "...Done!"

export PIO_MODEL_FILENAME=$(ls *.pkl | sed -n 1p)

echo "Testing model..."
[ -s ./test_model.py ] && python test_model.py \
                                $PIO_MODEL_FILENAME \
                                "./test_inputs.txt" \
                                "./test_outputs.txt"

echo "...Done!"

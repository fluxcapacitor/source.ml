#!/bin/sh

# ensure we're in the root conda environment
source activate root

# remove a possibly pre-existing `model_environment` environment.
conda env remove -n model_environment --yes || true

# create a new, empty `model_environment` environment.
conda create --yes -n model_environment python=3.5

# Activate it.
source activate model_environment

# Check for (non-empty) conda_requirements.txt and `conda install` from it.
[ -s ./conda_requirements.txt ] && conda install --yes --file ./conda_requirements.txt

# Check for (non-empty) requirements.txt and `pip install` it.
[ -s ./requirements.txt ] && pip install -r ./requirements.txt

# Check for (non-empty) wheel_requirements.txt and `pip install` it.
[ -s ./wheel_requirements.txt ] && pip install -r ./wheel_requirements.txt

export PIO_MODEL_FILENAME=$(ls *.pkl | sed -n 1p)
[ -s ./test_predict.py ] && python test_predict.py \
                                $PIO_MODEL_FILENAME \
                                "./test_inputs.txt" \
                                "./test_outputs.txt"

source deactivate model_environment

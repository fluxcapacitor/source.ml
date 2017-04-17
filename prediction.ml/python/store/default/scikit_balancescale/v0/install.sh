#!/bin/bash

echo "Installing model and dependencies..."
# Activate model_environment
source activate model_environment

# Check for (non-empty) conda_requirements.txt and `conda install` from it.
[ -s ./requirements_conda.txt ] && conda install --yes --file ./requirements_conda.txt

# Check for (non-empty) requirements.txt and `pip install` it.
[ -s ./requirements.txt ] && pip install -r ./requirements.txt

# Check for (non-empty) wheel_requirements.txt and `pip install` it.
[ -s ./requirements_wheel.txt ] && pip install -r ./requirements_wheel.txt
echo "...Done!"

#!/bin/bash

echo "Activating 'model_environment'..."
source activate model_environment
echo "...Done!"

python model.py model.pkl

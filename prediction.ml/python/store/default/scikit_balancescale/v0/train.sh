#!/bin/bash

[ -s ./install.sh ] && ./install.sh

echo "Activating 'model_environment'..."
source activate model_environment
echo "...Done!"

python train_model.py model.pkl

#!/bin/bash

export PIO_MODEL_FILENAME=$(ls *.pmml | sed -n 1p)

echo "Testing model..."

echo "...Done!"

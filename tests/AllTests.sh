#!/bin/sh
# ---------------
# Run the tests
# ---------------

# Add the src folder to the python path
export PYTHONPATH=$PYTHONPATH:../src:./src
# Run all tests
python AllTests.py

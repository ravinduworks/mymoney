#!/bin/bash


# Make sure you are under the mymoney app directory before executing the this script.
python3 -m pip install -r requirements.txt
python3 -m geektrust sample_inputs/not_rebalaceable.txt
python3 -m geektrust sample_inputs/rebalaceable.txt
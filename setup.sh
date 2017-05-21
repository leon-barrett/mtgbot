#!/bin/bash

set -ex

# Download libs
pip install -r requirements.txt -t lib/ --upgrade
# Download card data
test -f AllSets.json || (wget http://mtgjson.com/json/AllSets.json.zip && unzip AllSets.json.zip)
# Preprocess card info and verify that needed secrets are available
python -m data

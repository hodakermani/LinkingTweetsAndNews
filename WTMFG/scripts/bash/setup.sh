#!/usr/bin/env bash
export LC_ALL=C
mkdir tmp
touch tmp/texts.txt
export PYTHONPATH=$(pwd)/src/stanford-ner-tagger/:$(pwd)/
virtualenv -p python3 venv
source ./venv/bin/activate
pip3 install -r requirements.txt
python3 ./scripts/python/setup_nltk.py

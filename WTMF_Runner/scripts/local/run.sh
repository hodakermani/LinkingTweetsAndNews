#!/usr/bin/env bash
export LC_ALL=C
cd $LOCAL_DIR/WTMFG
mkdir tmp
touch tmp/texts.txt
export PYTHONPATH=$(pwd)/src/stanford-ner-tagger/:$(pwd)/
source ./venv/bin/activate
source ./scripts/bash/pick_dev_sample.sh 100 200 300
source ./run.sh
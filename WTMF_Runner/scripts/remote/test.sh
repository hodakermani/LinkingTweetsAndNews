#!/usr/bin/env bash
export LC_ALL=C
export NUM_OF_PROCESSORS=$1
export NUM_OF_THREADS=$1
export TEXTS_FILE_PATH=./data/train/texts.txt
export TWEETS_FILE_PATH=./data/train/tweets.txt
export NEWS_FILE_PATH=./data/train/news.txt
source ./scripts/bash/setup.sh
nohup time python3 ./src/test.py &> out.log & echo $! > run.pid
#!/usr/bin/env bash
export NUM_OF_PROCESSORS=2
export TEXTS_FILE_PATH=./data/dev/texts.txt
export TWEETS_FILE_PATH=./data/dev/tweets.txt
export NEWS_FILE_PATH=./data/dev/news.txt
python3 ./src/test.py
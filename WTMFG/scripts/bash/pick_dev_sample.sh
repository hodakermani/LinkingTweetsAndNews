#!/usr/bin/env bash
tail -n $1 data/train/news.txt > data/dev/news.txt
tail -n $2 data/train/texts.txt > data/dev/texts.txt
tail -n $3 data/train/tweets.txt > data/dev/tweets.txt
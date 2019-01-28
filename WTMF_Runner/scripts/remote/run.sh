#!/usr/bin/env bash
export LC_ALL=C
source ~/.ssh/environment
cp ~/scripts/test.sh ~/WTMFG/run.sh
cd ~/WTMFG
source run.sh $1

#!/usr/bin/env bash
export LC_ALL=C
cp ~/scripts/testdev.sh ~/WTMFG/run.sh
cd ~/WTMFG
source run.sh $1

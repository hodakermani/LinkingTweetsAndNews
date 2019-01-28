#!/usr/bin/env bash
export LC_ALL=C
cp ~/scripts/test.sh ~/WTMFG/run.sh
cd ~/WTMFG
git pull
cd ~/acl2013
git pull
cd code
g++ -std=c++11 *.cpp -o wtmf -I/usr/local/include -L/usr/local/lib -litpp -pthread


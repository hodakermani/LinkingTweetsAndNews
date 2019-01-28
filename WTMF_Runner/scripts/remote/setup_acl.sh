#!/usr/bin/env bash
git clone https://amirs7:amirAS45875154@github.com/amirs7/OptWTMFG.git
mv OptWTMFG acl2013
cd ~/acl2013
cd code
g++ -std=c++11 *.cpp -o wtmf -I/usr/local/include -L/usr/local/lib -litpp -pthread
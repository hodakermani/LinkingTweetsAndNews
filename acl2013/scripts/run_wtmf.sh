#! /bin/bash
cd code
g++ -w -std=c++11 *.cpp -o wtmf -I/usr/local/include -L/usr/local/lib -litpp -lpthread
./wtmf  1  $DATA_DIR/train.tfidf.sm $DATA_DIR/train.weight.sm  $DATA_DIR/train.adjacency.sm $MODEL_DIR/model  100  20  0.01  3  $1
cd ..
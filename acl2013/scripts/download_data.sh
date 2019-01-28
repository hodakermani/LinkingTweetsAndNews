#! /bin/bash
mkdir data
cd data
wget http://www.cs.columbia.edu/~weiwei/code/acl2013.zip
unzip acl2013.zip -d acl2013
cp -r acl2013/data/model model
mv data/model/train.ind data/model/train.tfidf.sm
mv data/model/train.weight.ind data/model/train.weight.sm
mv data/model/nb.ind data/model/train.adjacency.sm
cd ..
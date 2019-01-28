#! /bin/bash
cd $ROOT_DIR
if [ ! -e data ]; then
    mkdir data
fi
cd data
if [ ! -e model ]; then
    mkdir model
fi
cd $ROOT_DIR
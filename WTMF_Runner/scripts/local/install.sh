#!/usr/bin/env bash
source ~/.bash_profile
if [[ -z $HOME ]]; then
    echo "HOME is not set"
    return 1
fi
if [[ -z $LOCAL_DIR ]]; then
    echo "LOCAL_DIR is not set"
    return 1
fi
cd $LOCAL_DIR
source ~/.bash_profile

if [ ! -e WTMFG ]; then
    git clone https://amirs7:amirAS45875154@github.com/amirs7/WTMFG.git
fi
cd WTMFG
git checkout parallel
source scripts/bash/setup.sh

cd $LOCAL_DIR
if [ ! -e OptWTMFG ]; then
    rm -rf OptWTMFG
    git clone https://amirs7:amirAS45875154@github.com/amirs7/OptWTMFG.git
fi
mv OptWTMFG acl2013
cd acl2013
source scripts/setup.sh
cd $LOCAL_DIR

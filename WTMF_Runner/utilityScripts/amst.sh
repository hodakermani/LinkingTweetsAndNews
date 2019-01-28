#!/usr/bin/env bash
export REMOTE_WTMFG_DIR=~/WTMFG
export AMST_IP=188.166.91.77
export AMST_WTMFG_DIR=~/wtmfg
export DATA_DIR=/Users/amir/hodaProject/data/remote

scp -r secrets/ root@$AMST_IP:$AMST_WTMFG_DIR -i ./secrets/do_id_rsa
scp -i do_id_rsa -r root@167.99.0.112:$REMOTE_WTMFG_DIR/tmp $AMST_WTMFG_DIR:./newtmp
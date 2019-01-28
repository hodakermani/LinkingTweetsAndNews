#! /bin/bash

# source scripts/setup_data_dir.sh

# source scripts/download_data.sh
# source scripts/copy_data.sh
echo 'Setting Up ACL'
source $SCRIPTS_DIR/vars.sh
# source scripts/install.sh
# source scripts/install_mac.sh

cd $ROOT_DIR/code
g++ -w -std=c++11 *.cpp -o wtmf -I/usr/local/include -L/usr/local/lib -litpp -lpthread
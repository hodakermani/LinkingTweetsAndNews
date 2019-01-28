#! /bin/bash
brew update
brew install htop libblas-dev liblapack-dev libfftw3-dev build-essential cmake unzip default-jre default-jdkß -y
cd $ROOT_DIR
mkdir itpp
cd itpp
wget https://sourceforge.net/projects/itpp/files/itpp/4.2.0/itpp-4.2.tar.gz
tar -xvzf itpp-4.2.tar.gz
cd $ROOT_DIR/itpp/itpp-4.2
./configure
make
make install
ldconfig
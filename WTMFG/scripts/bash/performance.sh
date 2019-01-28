#!/usr/bin/env bash
export LC_ALL=C
apt-get update -y
apt-get install python3-pip virtualenv libblas-dev liblapack-dev libfftw3-dev build-essential cmake unzip default-jre default-jdk -y
if [[ -d ./itpp ]]   # for file "if [-f /home/rama/file]"
then
    echo "itpp dir present"
    rm -r ./itpp
fi
mkdir itpp
cd itpp
wget https://sourceforge.net/projects/itpp/files/itpp/4.2.0/itpp-4.2.tar.gz
tar -xvzf itpp-4.2.tar.gz
cd /root/itpp/itpp-4.2
./configure
make
make install
ldconfig
cd ../../

if [[ -d ./acl2013 ]]   # for file "if [-f /home/rama/file]"
then
    echo "acl dir present"
    rm -r ./acl2013
fi
wget http://www.cs.columbia.edu/~weiwei/code/acl2013.zip
unzip acl2013.zip -d acl2013
cd acl2013/code
g++ -std=c++11 *.cpp -o wtmf -I/usr/local/include -L/usr/local/lib -litpp
cd ../../
rm acl2013.zip
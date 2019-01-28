#!/usr/bin/env bash
cd ~
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
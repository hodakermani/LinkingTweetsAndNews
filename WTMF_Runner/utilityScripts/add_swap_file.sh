#!/usr/bin/env bash
sudo fallocate -l $1 /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show
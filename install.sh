#!/bin/bash

CWD=$(pwd)

sudo adduser $USER lp
sudo apt install python3
sudo apt install pythn3.11-venv

python3 -m venv .env 
source .env/bin/activate
pip install -r requirements.txt 

sed -i "s/user/${USER}/" bql-label-printer.service 
sed -i "s|pwd|$CWD|g" bql-label-printer.service 


sudo cp bql-label-printer.service /etc/systemd/system/bql.service

sudo systemctl start bql 


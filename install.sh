#!/bin/bash

CWD=$(pwd)

sudo adduser $USER lp
sudo apt install python3 

python3 -m venv .env 
source .env/bin/activate
pip install -r requirements 

sed -i "s/user/${USER}/" bql-label-printer.service 
sed -i "s|pwd|$CWD|g" bql-label-printer.service 


sudo cp bql-label-printer.service /etc/systemd/system/bql.service

sudo systemctl start bql 


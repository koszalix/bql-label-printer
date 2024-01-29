#!/bin/bash

sudo adduser $USER lp
sudo apt install python 

python -m venv .env 
source .env/bin/activate
pip install -r requirements 

sed "s/user/${USER}/" bql-label-printer.service 
sed "s|pwd|$CWD|g" bql-label-printer.service 


cp bql-label-printer.service /etc/systemd/system/bql.service

systemctl start bql 



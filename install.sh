#!/bin/bash

CWD=$(pwd)

mkdir -p /usr/bin/bql-label-printer
apt install python3
apt install python3.11-venv

cp -r . /usr/bin/bql-label-printer

cd /usr/bin/bql-label-printer || exit 

python3 -m venv .env 
source .env/bin/activate
pip install -r requirements.txt 

cp bql.service /etc/systemd/system/bql.service

systemctl enable bql
systemctl start bql 


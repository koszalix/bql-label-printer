#!/bin/bash

CWD=$(pwd)

mkdir -p /opt/bql-label-printer
mkdir -p /etc/bql-label-printer

apt install python3
apt install python3.11-venv

cp -r . /opt/bql-label-printer
cd /opt/bql-label-printer || exit 

python3 -m venv .env 
source .env/bin/activate
pip install -r requirements.txt 

cp bql.service /etc/systemd/system/bql.service
cp bql.yml /etc/bql-label-printer/

systemctl enable bql
systemctl start bql 
systemctl status bql

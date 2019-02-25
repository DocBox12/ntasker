#!/bin/bash

set -e

virtualenv -p python3 .
./bin/pip3 install requests
./bin/pip3 install ics
git init
git pull https://github.com/DocBox12/ntasker.git
chmod +x install.py
chmod +x ./src/main.py
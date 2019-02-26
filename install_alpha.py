#!/usr/bin/env python3


import os

exe = ("""
set -e
virtualenv -p python3 .
./bin/pip3 install requests
./bin/pip3 install ics
git clone https://github.com/DocBox12/ntasker.git
chmod +x ./ntasker/src/main.py
""")

os.system(exe)
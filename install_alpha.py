#!/usr/bin/env python3


import os
import argparse

def install():
    exe = ("""
    set -e
    virtualenv -p python3 .
    ./bin/pip3 install requests
    ./bin/pip3 install ics
    git clone https://github.com/DocBox12/ntasker.git
    chmod +x ./ntasker/src/main.py
    chmod +x ./ntasker/src/ntasker_cron.py
    """)

    os.system(exe)
    return

def upgrade_download():
    exe = ("""
    wget https://raw.githubusercontent.com/DocBox12/ntasker/installer/upgrade_alpha.sh
    chmod +x upgrade_alpha.sh
    ./upgrade_alpha.sh
    """)

    os.system(exe)


parser = argparse.ArgumentParser()

parser.add_argument("--install", help="Install latest application.", action="store_true")

parser.add_argument("--upgrade", help="Upgrade application to latest version.", action="store_true")

args = parser.parse_args()

if args.install:
    install()

if args.upgrade:
    upgrade_download()



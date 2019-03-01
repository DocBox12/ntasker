#!/bin/bash

set -e

rm -rf ./ntasker/
git clone https://github.com/DocBox12/ntasker.git
chmod +x ./ntasker/src/main.py
chmod +x ./ntasker/src/ntasker_cron.py
rm upgrade_alpha.sh

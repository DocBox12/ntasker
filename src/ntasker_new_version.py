#!/usr/bin/env python3

import os
import argparse
import requests

URL_VERSION = "https://raw.githubusercontent.com/DocBox12/ntasker/installer/VERSION.TXT"
URL_WARNING = "https://raw.githubusercontent.com/DocBox12/ntasker/installer/WARNING.TXT"
MORE_INFORMATION = "https://github.com/DocBox12/ntasker/releases"
VERION_FILE_NAME = "VERSION.TXT"

# Check local version
def check_version():
    version_file = os.path.join(os.path.dirname(__file__), VERION_FILE_NAME)
    with open(version_file, "r") as vf:
        version = vf.read()
        return version

# Check version from network
def search_update():
    website_data = requests.get(URL_VERSION)
    if website_data.status_code == 200:
        # Remove all white chars
        raw_data_from_website = website_data.content.decode("utf-8").rstrip('\r\n\t')
        return raw_data_from_website
    else:
        print("I can not download the update data.", website_data.status_code)
        exit()

def check_update():

    local_version = check_version().rstrip('\r\n\t') # Remove all white char
    latest_version = search_update()
    if local_version.lower() != latest_version.lower():
        info = ("New version %s is avaiable.") % latest_version
        print(info)
        check_warning()
    else:
        print("You have the latest version.")
    return

# This function checks if there are any warnings for the latest update
def check_warning():
    website_data = requests.get(URL_WARNING)
    if website_data.status_code == 200:
        # Remove all white chars
        raw_data_from_website = website_data.content.decode("utf-8").rstrip('\r\n\t')
        STR_raw_data_from_website = str(raw_data_from_website).upper()
    else:
        print("I can not download the data. The update was interrupted.", website_data.status_code)
        exit()
    
    if "YES" in STR_raw_data_from_website:
        statement = ("WARNING! The update will change the configuration files. For more information, please visit this link -> %s") % (MORE_INFORMATION)
        print(statement)
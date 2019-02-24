#!/usr/bin/env python3

import os
import argparse
import requests

URL_VERSION = "https://raw.githubusercontent.com/DocBox12/ntasker/installer/VERSION.TXT"
URL_REPOSITORY = "https://github.com/DocBox12/ntasker.git"
URL_WARNING = "https://raw.githubusercontent.com/DocBox12/ntasker/installer/WARNING.TXT"
MORE_INFORMATION = "https://github.com/DocBox12/ntasker/releases"

def update():
    execute_command = ("""
                        git pull %s
                        chmod +x ./src/main.py
                        chmod +x install.py
                        """) % URL_REPOSITORY
    
    os.system(execute_command)
    exit()


def force_update():
    execute_command = ("""
                        git reset --hard
                        git pull %s
                        chmod +x ./src/main.py
                        chmod +x install.py
                        """) % URL_REPOSITORY

    os.system(execute_command)
    exit()

def reset_app():
    execute_command = ("""
                        git reset --hard
                        chmod +x ./src/main.py
                        chmod +x install.py
                        """)
    os.system(execute_command)
    exit()


# Check local version
def check_version():
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION.txt')
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

    local_version = check_version()
    latest_version = search_update()

    if local_version != latest_version:
        value = check_warning()
        print("Do you want to continue? [Y=YES] [N=NO]")
        while True:
            choose = input()
            if choose.upper() == "Y":
                if value is True: # If warning run force
                    force_update()
                else:
                    update()
            elif choose.upper() == "N":
                print("The update was interrupted at the user's request.")
                exit()
            else:
                print("Bad choice, try again.")
    else:
        print("You have the latest version.")


    return

# This function checks if there are any warnings for the latest update
def check_warning():
    website_data = requests.get(URL_WARNING)
    if website_data.status_code == 200:
        # Remove all white chars
        raw_data_from_website = website_data.content.decode("utf-8").rstrip('\r\n\t')
    else:
        print("I can not download the data. The update was interrupted.", website_data.status_code)
        exit()
    
    if str(raw_data_from_website).upper() == "YES":
        print("WARNING! Detected that the latest update changes important files that are necessary for the operation of the update. Read the release information to learn more %s") % (MORE_INFORMATION)
        return True
    else:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--check_update", help="Checks if a new version of the program is available, if it is offered by updates", action="store_true")

    parser.add_argument("--force_update", help="It restores the state of the application to the official release and downloads the latest version from the server. All your settings will be deleted", action="store_true")

    parser.add_argument("--reset", help="Returns the application to its original state. All your settings will be deleted", action="store_true")

    args = parser.parse_args()
    
    if args.force_update:
        force_update()
    
    if args.reset:
        reset_app()

    if args.check_update:
        check_update()
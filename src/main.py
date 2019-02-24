#!/usr/bin/env python3

import os
import json
import time
import configparser
import ntasker_email
import sys
import argparse
import ntasker_calendar
import ntasker_logs

def extract_task(debug):

    today_is = time.strftime("%A")

    raw_data_from_json = loading_json_file()

    if debug is True:
        LIST_tasks_from_json = raw_data_from_json.get("debug")
    else:
        LIST_tasks_from_json = raw_data_from_json.get(today_is)

    DICT_all_tasks = LIST_tasks_from_json[0]

    for task in DICT_all_tasks:
        if task == "___comment___":
            continue
        comment = DICT_all_tasks.get(task)
        ntasker_email.send_email(task, comment)
    
    return

def loading_json_file():
    tasks_json = os.path.join(os.path.dirname(__file__), 'tasks.json')

    try:
        with open(tasks_json) as tf:
            raw_data_from_json = json.load(tf)
            return raw_data_from_json
    except sys.exc_info()[0] as error:
            print(error)
            ntasker_logs.save_logs(error)
            return
            
# Loading config
config = configparser.RawConfigParser()

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file)

ical_url = config['Calendar']['ical_url']
timezone = config['Calendar']['Timezone']
tags = config['Calendar']['Tags']

today = config['Translation']['Today']

parser = argparse.ArgumentParser()

parser.add_argument("--verify", help="Verify json file. If file have errors program return information about this.", action="store_true")

parser.add_argument("--debug", help="Send tasks to nozbe without regardless day of the week.", action="store_true")

parser.add_argument("--run", help="Run app.", action="store_true")

parser.add_argument("--calendar", help="Import tasks from calendar and add to nozbe.", action="store_true")

args = parser.parse_args()

if args.verify:
    loading_json_file()

if args.debug:
    extract_task(True)

if args.run:
    extract_task(False)

if args.calendar:
    json_content = loading_json_file()
    ntasker_calendar.import_tasks_from_calendar(ical_url, timezone, tags, today, json_content)


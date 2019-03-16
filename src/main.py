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
import ntasker_sqlite
import ntasker_new_version

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
    try:
        with open(tasks_json) as tf:
            raw_data_from_json = json.load(tf)
            return raw_data_from_json
    except sys.exc_info()[0] as error:
            print(error)
            ntasker_logs.save_logs(error)
            return



def get_tags_for_calendar():
    raw_data_from_json = loading_json_file()
    LIST_tasks_from_json = raw_data_from_json.get("TagsForCalendar")
    DICT_all_tasks = LIST_tasks_from_json[0]
    hashtags = DICT_all_tasks.get("Tags")

    return hashtags

def import_today_flag():
    json_content = loading_json_file()
    hashtags = get_tags_for_calendar()
    ntasker_calendar.import_tasks_from_calendar(ical_url, timezone, hashtags, today, json_content, Add_start_time, False)
    
    return

def import_next_day_flag():
    json_content = loading_json_file()
    today = tomorrow
    hashtags = get_tags_for_calendar()
    ntasker_calendar.import_tasks_from_calendar(ical_url, timezone, hashtags, today, json_content, Add_start_time, True)
    return

def kill_process():
    with open(pid_file, 'r') as pf:
        pid_number = pf.read()
        pf.close()

    command_exe = "kill " + pid_number
    os.system(command_exe)
    exit()
    return

pid_file = os.path.join(os.path.dirname(__file__), 'pid.txt') 

# Loading config
config = configparser.RawConfigParser()

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file)

ical_url = config['Calendar']['ical_url']
timezone = config['Calendar']['Timezone']

today = config['Translation']['Today']
tomorrow = config['Translation']['Tomorrow']
Add_start_time = config['Calendar']['Add_start_time']

tasks_json = config['JSON']['json_localization']

parser = argparse.ArgumentParser()

parser.add_argument("--verify", help="Verify json file. If file have errors program return information about this.", action="store_true")

parser.add_argument("--debug", help="Send tasks to nozbe without regardless day of the week.", action="store_true")

parser.add_argument("--run", help="Run app and send tasks to Nozbe only from json file.", action="store_true")

parser.add_argument("--importtoday", help="Import tasks from calendar and add to nozbe.", action="store_true")

parser.add_argument("--importnextday", help="Import tomorrow tasks from calendar and add to nozbe", action="store_true")

parser.add_argument("--createdb", help="Create database", action="store_true")

parser.add_argument("--cleardb", help="Remove all data from database", action="store_true")

parser.add_argument("--remove_logs", help="Remove all log files.", action="store_true")

parser.add_argument("--check_update", help="Checks if a new version of the program is available", action="store_true")

parser.add_argument("--kill", help="Closes the ntasker_cron process", action="store_true")

parser.add_argument("--version", help="Show version", action="store_true")

args = parser.parse_args()

if args.verify:
    loading_json_file()

if args.debug:
    extract_task(True)

if args.run:
    extract_task(False)

if args.importtoday:
   import_today_flag()

if args.importnextday:
    import_next_day_flag()

if args.createdb:
    ntasker_sqlite.create_db()

if args.cleardb:
    ntasker_sqlite.remove_all()

if args.check_update:
    ntasker_new_version.check_update()

if args.version:
    version = ntasker_new_version.check_version()
    print(version)

if args.remove_logs:
    ntasker_logs.remove_all_logs()

if args.kill:
    kill_process()
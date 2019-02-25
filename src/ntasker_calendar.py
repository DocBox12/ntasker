#!/usr/bin/env python3

import requests
import time
import datetime
from ics import Calendar
from urllib.request import urlopen
import datetime
import ntasker_email

LIST_added = []

def import_tasks_from_calendar(URL, timezone, tags, today, raw_data_from_json):
    
    if today == "":
        today = "#Today"

    raw_url = Calendar(urlopen(URL).read().decode('utf-8'))

    raw_url = Calendar(requests.get(URL).text)

    LIST_data_from_calendar = raw_url.events

    for i in range(len(LIST_data_from_calendar)):
        task_details = LIST_data_from_calendar[i]
        
        task_name_from_calendar = task_details.name
        start_date_from_task = task_details.begin.to(timezone).format('YYYY,M,DD HH:mm')
        raw_end_time = task_details.end.to(timezone)
        raw_start_time = task_details.begin.to(timezone)
        hashtah_time = subtracting_time(raw_start_time, raw_end_time)
        
        LIST_start_date_from_task = start_date_from_task.split(" ")
        details_date = LIST_start_date_from_task[0]
        
        LIST_details_date = details_date.split(",")
        day_of_the_month = LIST_details_date[2]
        time_from_task = LIST_start_date_from_task[1]

        task_name_from_json = raw_data_from_json.get("Calendar")
        DICT_all_tasks = task_name_from_json[0]

        today_day_is = time.strftime("%d")
        """
        If task from calendar has sameone date how than today:
        - search for a task in json file
        - if task is in json file, extract comment and send values to generate_syntax funtion
        - is task is not in json file, send values to generate_syntax_function
        """
        if today_day_is == day_of_the_month:
            for one_task_from_json in DICT_all_tasks:
                if one_task_from_json.lower() == "___comment___":
                    continue
                if one_task_from_json.lower() == task_name_from_calendar.lower():
                    comment = DICT_all_tasks.get(one_task_from_json)
                    generate_syntax(True, one_task_from_json, today, hashtah_time, comment)
                    break
                else:
                    continue
            else:
                generate_syntax(False, task_name_from_calendar, tags, today, time_from_task, hashtah_time)
            """
            If the calendar task has a different date than today:
            - search for a task in json file
            - if task is in json, extract comment and send values to generate_syntax funtio
            - if task is not in json, return to for i in range (len(LIST_data_from_calendar)):

            This is used because application compare DTSTART from event with time.strftime("%d") (date created event in calendar with day today), but cyclical tasks have DTSTART from first event that has been created. For this reason, cyclical tasks are skipped when only the date is compared. The biggest problem is with everyday tasks.
            """
        else:
            for one_task_from_json in DICT_all_tasks:
                if one_task_from_json.lower() == task_name_from_calendar.lower():
                    comment = DICT_all_tasks.get(one_task_from_json)
                    generate_syntax(True, one_task_from_json, today, hashtah_time, comment)
                    break
                else:
                    continue

    return

def added_tasks(task_name):
    if len(LIST_added) == 0:
        LIST_added.append(task_name.lower())
        return False
    else:
        for i in range(len(LIST_added)):
            value = LIST_added[i]
            if task_name.lower() == value.lower():
                return True
            else:
                continue
        LIST_added.append(task_name.lower())
        return False

def generate_syntax(*args):
    if args[0] is True:
        # True, one_task_from_json, today, hashtah_tim, comment
        one_task_from_json = args[1] + " " + str(args[2]) + " " + str(args[3])
        value = added_tasks(args[1])
        if value is False:
            print(one_task_from_json)
            #ntasker_email.send_email(one_task_from_json, args[4])
            return
        else:
            return
    else:
        # False, task_name_from_calendar, tags, today, time_from_task, hashtah_time
        task_syntax = str(args[1]) + " " + str(args[2]) + " " + str(args[3].lower()) + " " + str(args[4]) + " " + str(args[5])
        value = added_tasks(args[1])
        if value is False:
            print(task_syntax)
            #ntasker_email.send_email(task_syntax, "")
            return
        else:
            return

def subtracting_time(start_time, end_time):
    subtracting_time_result  = end_time - start_time
    STR_subtracting_time_result = str(subtracting_time_result)
    DICT_time = {
                    "0:05:00":"#5 min",
                    "0:10:00":"#10 min",
                    "0:15:00":"#15 min",
                    "0:20:00":"#20 min",
                    "0:30:00":"#30 min",
                    "0:45:00":"#45 min",
                    "1:00:00":"#1 h",
                    "1:30:00":"#1:30 h",
                    "2:00:00":"#2 h",
                    "2:30:00":"#2:30 h",
                    "3:00:00":"#3 h",
                    "4:00:00":"#4 h",
                    "5:00:00":"#5 h",
                    "6:00:00":"#6 h",
                    "7:00:00":"#7 h",
                    "8:00:00":"#8 h"
                }

    
    time_hashtag = DICT_time.get(STR_subtracting_time_result)
    return time_hashtag  
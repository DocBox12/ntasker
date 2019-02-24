#!/usr/bin/env python3

import requests
import time
import datetime
from ics import Calendar
from urllib.request import urlopen
import datetime
import ntasker_email

def import_tasks_from_calendar(URL, timezone, tags, today, raw_data_from_json):

    if today == "":
        today = "#Today"

    TUPLE_WEEKSDAY = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

    raw_url = Calendar(urlopen(URL).read().decode('utf-8'))

    raw_url = Calendar(requests.get(URL).text)

    LIST_data_from_calendar = raw_url.events

    for i in range (len(LIST_data_from_calendar)):
        task_details = LIST_data_from_calendar[i]
        
        task_name_from_calendar = task_details.name
        start_date_from_task = task_details.begin.to(timezone).format('YYYY,M,DD HH:mm')

        raw_end_time = task_details.end.to(timezone)
        raw_start_time = task_details.begin.to(timezone)
        hashtah_time = subtracting_time(raw_start_time, raw_end_time)
        
        LIST_start_date_from_task = start_date_from_task.split(" ")
        details_date = LIST_start_date_from_task[0]
        LIST_details_date = details_date.split(",")
        time_from_task = LIST_start_date_from_task[1]
        
        numer_day_of_week = datetime.datetime(int(LIST_details_date[0]), int(LIST_details_date[1]), int(LIST_details_date[2])).weekday()
        
        day_of_week = TUPLE_WEEKSDAY[numer_day_of_week]

        today_is = time.strftime("%A")
        if today_is == day_of_week:
            task_name_from_json = raw_data_from_json.get("Calendar")
            DICT_all_tasks = task_name_from_json[0]
            for one_task_from_json in DICT_all_tasks:
                if one_task_from_json.lower() == "___comment___":
                    continue
                if one_task_from_json.lower() == task_name_from_calendar.lower():
                    one_task_from_json = one_task_from_json + " " + str(today) + " " + str(hashtah_time)
                    comment = DICT_all_tasks.get(task_name_from_calendar)
                    ntasker_email.send_email(one_task_from_json, comment)
                    break
                else:
                    continue
            else:                
                task_syntax = str(task_name_from_calendar) + " " + str(tags) + " " + str(today.lower()) + " " + str(time_from_task) + " " + str(hashtah_time)
                ntasker_email.send_email(task_syntax, "")

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
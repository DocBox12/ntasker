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
        today = "#Dzisiaj"

    TUPLE_WEEKSDAY = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

    raw_url = Calendar(urlopen(URL).read().decode('utf-8'))

    raw_url = Calendar(requests.get(URL).text)

    LIST_data_from_calendar = raw_url.events

    for i in range (len(LIST_data_from_calendar)):
        task_details = LIST_data_from_calendar[i]
        task_name_from_calendar = task_details.name
        start_date_from_task = task_details.begin.to(timezone).format('YYYY,M,DD HH:mm')

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
                if one_task_from_json == task_name_from_calendar:
                    comment = DICT_all_tasks.get(task_name_from_calendar)
                    ntasker_email.send_email(one_task_from_json, comment)
                    break
                else:
                    continue

            else:
                task_syntax = str(task_name_from_calendar) + " " + str(tags) + " " + str(today.lower()) + " " + str(time_from_task)
                ntasker_email.send_email(task_syntax, "")

                

    return





    
  
#!/usr/bin/env python3

import requests
import time
import datetime
from ics import Calendar
from urllib.request import urlopen
import datetime
import ntasker_email
from dateutil.rrule import rrulestr
import ntasker_sqlite


DICT_rrule = {}


def search_tasks(URL, timezone, next_day):

    LIST_with_tasks = []

    if next_day is True:
        DATE_new_day = datetime.datetime.now() + datetime.timedelta(days=1)
        STR_new_day = DATE_new_day.strftime("%Y%m%d")
        today_is = STR_new_day
    else:
        today_is = time.strftime("%Y%m%d")    

    raw_url = Calendar(urlopen(URL).read().decode('utf-8'))

    raw_url = Calendar(requests.get(URL).text)

    LIST_data_from_calendar = raw_url.events

    for i in range(len(LIST_data_from_calendar)):
        task_details = LIST_data_from_calendar[i]
        uid_task = task_details.uid
        start_date_from_task = task_details.begin.to(timezone).format('YYYYMMDD') # Covert time for humans

        if int(today_is) == int(start_date_from_task):
            LIST_with_tasks.append(task_details)
            continue


        LIST_task_details = str(task_details).split("\n")
        for j in range(len(LIST_task_details)):
            if "RRULE" in LIST_task_details[j]:
                rrule_details = LIST_task_details[j]
                value = rrulestr(rrule_details)
                rrule_data = value.after(datetime.datetime.now()).strftime("%Y%m%d")
                if int(rrule_data) == int(today_is):
                    LIST_with_tasks.append(task_details)
                    DICT_rrule.update({uid_task:rrule_data})
                else:
                    continue

    return LIST_with_tasks

def import_tasks_from_calendar(URL, timezone, tags, today, raw_data_from_json, Add_start_time, next_day):
    

    LIST_data_from_calendar = search_tasks(URL, timezone, next_day)
    DICT_general_tasks = {}
    DICT_sequence = {}
    DICT_dtstart = {}
    DICT_task_name = {}
    DICT_comment = {}
    DICT_start_date_from_task = {}
    DICT_task_duration = {}

    for i in range(len(LIST_data_from_calendar)):
        task_details = LIST_data_from_calendar[i]


        task_name_from_calendar = task_details.name # Get task name
        uid_task = task_details.uid 
        comment_from_calendar = task_details.description # Get description from task
        start_date_from_task = task_details.begin.to(timezone).format('HH:mm') # Covert time for people
        task_duration_from_calendar = task_details.duration


        dt_start = task_details.begin.to(timezone).format('YYYYMMDDHHmm')
        LIST_task_details = str(task_details).split("\n")
        for j in range(len(LIST_task_details)):
            if "SEQUENCE" in LIST_task_details[j]:
                sequence = LIST_task_details[j]
                LIST_sequence = sequence.split(":")
                sequence_number = LIST_sequence[1]


                uid_from_DICT = DICT_general_tasks.get(uid_task)
                if uid_from_DICT is None:
                    DICT_general_tasks.update({uid_task:task_name_from_calendar})
                    # UID and sequence
                    DICT_sequence.update({uid_task:int(sequence_number)})  
                
                    # UID and task name from calendar
                    DICT_task_name.update({uid_task:task_name_from_calendar})

                    # UID and comment from task
                    DICT_comment.update({uid_task:comment_from_calendar})

                    # UID and sequence
                    DICT_sequence.update({uid_task:int(sequence_number)})

                    # UID and DTSTART
                    DICT_dtstart.update({uid_task:dt_start})

                    # UID and start_date_from_task
                    DICT_start_date_from_task.update({uid_task:start_date_from_task})

                    # UID and task duration
                    DICT_task_duration.update({uid_task:task_duration_from_calendar})
                else:
                    currently_sequence = DICT_sequence.get(uid_task)
                    if int(currently_sequence) > int(sequence_number):
                        # UID and DTSTART
                        DICT_dtstart.update({uid_task:dt_start})
                        # UID and sequence
                        DICT_sequence.update({uid_task:int(sequence_number)})
                        # UID and task duration
                        DICT_task_duration.update({uid_task:task_duration_from_calendar})

    for uid_task in DICT_sequence:
        dtstart_from_dict = DICT_dtstart.get(uid_task)
        sequence_number_from_dict = DICT_sequence.get(uid_task)
        task_name_from_calendar_from_dict = DICT_task_name.get(uid_task)
        comment_from_calendar_from_dict = DICT_comment.get(uid_task) 
        start_date_from_task_from_dict = DICT_start_date_from_task.get(uid_task)
        task_duration_from_calendar_from_dict = DICT_task_duration.get(uid_task)
        rrule_time_calendar_from_dict = DICT_rrule.get(uid_task)

        '''
         If rrule is None send to SQL the time from dstart and mark task as False that is, not having a rrule

         else

         send to SQL the time from rrule and mark task as True that is having a rrule.
        '''
        
        if rrule_time_calendar_from_dict is None:
            result_sql = ntasker_sqlite.search_task(uid_task, dtstart_from_dict, sequence_number_from_dict, False)
        else:
            result_sql = ntasker_sqlite.search_task(uid_task, rrule_time_calendar_from_dict, sequence_number_from_dict, True)

        '''
        True - The task is in the database and has not changed

        String - The task is in the database, but the date of sending the task from the database is                different from the date from the rrule, therefore the date must be updated in the                 database and the task sent again. This is used for repetitive tasks because one UID is            generated and subsequent dates are generated based on RRULE. Therefore, this                      condition must be checked for the task to be sent.

        None - The task isn't in the database - they should be sent and added to the database
        '''

        if result_sql is True:
            continue
        elif result_sql is str:
            ntasker_sqlite.update_dtstart(uid_task, rrule_time_calendar_from_dict)
        elif result_sql is None:
            ntasker_sqlite.add_task(uid_task, dtstart_from_dict, sequence_number_from_dict)
        '''
        Unfortunately, Nozbe does not understand the calculated time and must be changed. See the subtracting_time function
        REMEMBER! Nozbe will set the length of the task only when it appears after the word Today. See instructions:

        generate_syntax(True, one_task_from_json, today, hashtah_time, comment

        hashtah_time is after today 
        '''
        hashtah_time = subtracting_time(task_duration_from_calendar_from_dict)

        # Loading tasks from json file
        task_name_from_json = raw_data_from_json.get("Calendar")
        DICT_all_tasks = task_name_from_json[0]


        if Add_start_time == "all":
            start_date_for_json = start_date_from_task_from_dict
            start_date_for_calendar = start_date_from_task_from_dict
        elif Add_start_time == "json":
            start_date_for_json = start_date_from_task_from_dict
            start_date_for_calendar = ""
        elif Add_start_time == "calendar":
            start_date_for_json = ""
            start_date_for_calendar = start_date_from_task_from_dict
        else:
            start_date_for_json = ""
            start_date_for_calendar = ""
    
        """
        If task from calendar has sameone date how than today:
        - search for a task in json file
        - if task is in json file, extract comment and send values to generate_syntax funtion
        - is task is not in json file, send values to generate_syntax_function
        """
    
        for one_task_from_json in DICT_all_tasks:
            if one_task_from_json.lower() == "___comment___":
                continue
            if one_task_from_json.lower() == task_name_from_calendar_from_dict.lower():
                #result_sql = ntasker_sqlite.search_task(uid_task, dtstart_from_dict, #sequence_number_from_dict, True)
                #if result_sql is True:
                    #continue 
                comment = DICT_all_tasks.get(one_task_from_json)
                one_task_from_json = one_task_from_json + " " + str(today.lower()) + " " + str(start_date_for_json) + " " + str(hashtah_time)
                ntasker_email.send_email(one_task_from_json, comment)
                #if result_sql is None:
                    #ntasker_sqlite.add_task(uid_task, dtstart_from_dict, sequence_number_from_dict)
                break
            else:
                continue
        else:
            task_syntax = str(task_name_from_calendar_from_dict) + " " + str(tags) + " " + str(today.lower()) + " " + str(start_date_for_calendar) + " " + str(hashtah_time)
            ntasker_email.send_email(task_syntax, comment_from_calendar_from_dict)
            #if result_sql is None:
                #ntasker_sqlite.add_task(uid_task, dtstart_from_dict, sequence_number_from_dict)

        

    return

'''
Calculate how long the task takes. This value is usage with Nozbe to settings the length of the task.
Unfortunately, Nozbe does not understand the calculated time and must be changed.
'''
def subtracting_time(duration):
    
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

    
    time_hashtag = DICT_time.get(str(duration))
    return time_hashtag  
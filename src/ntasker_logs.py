#!/usr/bin/env python3

import os
import time
import datetime

def save_logs(error):
    errors_file = os.path.join(os.path.dirname(__file__), 'errors.txt') 
    if not os.path.exists(errors_file):
        open(errors_file, "w+")

    now_time = (time.strftime("%Y-%m-%d-%H:%M:%S"))
    with open(errors_file, 'a') as ef:
        ef.write(str(now_time))
        ef.write("\t")
        ef.write(str(error))
        ef.write("\n")
        ef.close()


def save_events_app(event):
    events_file = os.path.join(os.path.dirname(__file__), 'events.txt') 
    if not os.path.exists(events_file):
        open(events_file, "w+")

    now_time = (time.strftime("%Y-%m-%d-%H:%M:%S"))
    with open(events_file, 'a') as ef:
        ef.write(str(now_time))
        ef.write("\t")
        ef.write(str(event))
        ef.write("\n")
        ef.close()

def sent_emails(operation, number):

    email_file = os.path.join(os.path.dirname(__file__), 'email.txt') 
    if not os.path.exists(email_file):
        open(email_file, "w+")


    raw_create_time = os.path.getmtime(email_file)
    human_create_time =  datetime.datetime.fromtimestamp(raw_create_time).strftime('%d')

    today_is = time.strftime('%d')
    if int(today_is) > int(human_create_time):
        os.remove(email_file)
        open(email_file, "w+")

    if operation == "save":
        with open(email_file, 'w') as ef:
            ef.write(str(number))
            ef.close()
            return

    if operation == "read":
        with open(email_file, 'r') as ef:
            email_number = ef.read()
            if email_number == "":
                email_number = 0

            return email_number
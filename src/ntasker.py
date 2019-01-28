#!/usr/bin/env python3

# Maintainer: DocBox12
# Webpage: http://aboutme.morfiblog.pl/
# Version: 

import os
import json
import time
import configparser
import smtplib
from email.message import EmailMessage
import sys

def extract_task():
    today_is = time.strftime("%A")

    LIST_tasks_from_json = raw_data_from_json.get(today_is)

    DICT_all_tasks = LIST_tasks_from_json[0]

    for task in DICT_all_tasks:
        if task == "___comment___":
            continue
        comment = DICT_all_tasks.get(task)
        send_email(task, comment)

    return


def send_email(topic, comment):
    email_message = EmailMessage()
    email_message['Subject'] = str(topic)
    email_message['From'] = str(email_username)
    email_message['To'] = str(email_address)
    email_message.set_content(str(comment))
    i=0
    while i < 3:
        try:
            connect_email = smtplib.SMTP_SSL(email_server, str(email_port))
            connect_email.ehlo()
            connect_email.login(email_username, email_password)
            connect_email.send_message(email_message)
            connect_email.close()
            break
        except sys.exc_info()[0] as error:
            print(error)
            now_time = (time.strftime("%Y-%m-%d-%H:%M:%S"))
            with open(errors_file, 'a') as ef:
                ef.write(str(now_time))
                ef.write("\t")
                ef.write(str(error))
                ef.write("\n")
                ef.close()
            i+=1
            if i == 3:
                exit()
            else:
                continue

    return

if __name__ == "__main__":
    # Loading files
    errors_file = os.path.join(os.path.dirname(__file__), 'errors.txt') 
    if not os.path.exists(errors_file):
        os.mknod(errors_file)

    tasks_json = os.path.join(os.path.dirname(__file__), 'tasks.json')

    try:
        with open(tasks_json) as tf:
            raw_data_from_json = json.load(tf)
    except sys.exc_info()[0] as error:
            print(error)
            now_time = (time.strftime("%Y-%m-%d-%H:%M:%S"))
            with open(errors_file, 'a') as ef:
                ef.write(str(now_time))
                ef.write("\t")
                ef.write(str(error))
                ef.write("\n")
                ef.close()
                exit()

    config = configparser.ConfigParser()

    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_file)

    email_server = config['Email']['server']
    email_username = config['Email']['username']
    email_password = config['Email']['password']
    email_port = config['Email']['port']
    email_address = config['Email']['address']

    extract_task()
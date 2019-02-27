#!/usr/bin/env python3

import smtplib
from email.message import EmailMessage
import ntasker_logs
import sys
import os
import configparser

def send_email(topic, comment):
    value = ntasker_logs.sent_emails("read", "")
    if int(value) == int(max_emails):
        error = "Exhausted email limit"
        ntasker_logs.save_logs(error)
        return
    else:
        new_value = int(value) + 1
        
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
            value = ntasker_logs.sent_emails("save", str(new_value))
            ntasker_logs.save_events_app("Send mail")
            break
        except sys.exc_info()[0] as error:
            ntasker_logs.save_logs(error)
            i+=1
            if i == 3:
                return
            else:
                continue

    return

# Loading config
config = configparser.RawConfigParser()

config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file)

email_server = config['Email']['server']
email_username = config['Email']['username']
email_password = config['Email']['password']
email_port = config['Email']['port']
email_address = config['Email']['address']
max_emails = config['Email']['max_emails']
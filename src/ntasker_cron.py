#!/usr/bin/env python3

import time
import configparser
import os
import main

def start_cron():

    while True:
        now_time = time.strftime("%H:%M")
        time.sleep(int(check_new_tasks))
        main.import_today_flag()

        if send_tasks_from_json == now_time:
            main.extract_task(False)
        if send_task_tomorrow_from_calendar == now_time:
            main.import_next_day_flag()
            


if __name__ == "__main__":
    # Loading config
    config = configparser.RawConfigParser()

    config_file = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(config_file)

    check_new_tasks = config['Cron']['check_new_tasks']
    send_tasks_from_json = config['Cron']['send_tasks_from_json']
    send_task_tomorrow_from_calendar = config['Cron']['send_task_tomorrow_from_calendar']


    start_cron()

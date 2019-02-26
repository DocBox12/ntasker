#!/usr/bin/env python3

import os
import time

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
        exit()


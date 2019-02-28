#!/usr/bin/env python3


import sqlite3
import os
import ntasker_logs
import sys


db = os.path.join(os.path.dirname(__file__), 'ntasker_database.db')

def create_db():
    sql_exe = ("""
            CREATE TABLE `ntasker` (
        	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	        `ical`	TEXT,
            'dtstart' TEXT
                                    );
            """)


    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql_exe)
    conn.commit()
    conn.close()
    return

def add_task(uid_task, dtstart):
    sql_exe = ("""
                insert into ntasker (ical, dtstart)
                VALUES("%s", "%s");
            """) % (str(uid_task), str(dtstart))

    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(sql_exe)
        conn.commit()
        conn.close()
        ntasker_logs.save_events_app("Add task to database")
        return
    except sys.exc_info()[0] as error:
        ntasker_logs.save_logs(error)
        return

def search_task(uid_task, dt_start):
    sql_exe = ("""
                select * FROM ntasker
                where ical="%s";
            """) % (str(uid_task))
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(sql_exe)
        raw_data_from_sql = c.fetchall()
        if len(raw_data_from_sql) == 0:
            return False
        else:
            LIST_information_about_task  = raw_data_from_sql[0]
            dt_start_from_sql = LIST_information_about_task[2]
            if str(dt_start) == str(dt_start_from_sql):
                return True
            else:
                remove_task(uid_task)
                return False
    except sys.exc_info()[0] as error:
        ntasker_logs.save_logs(error)
        return True    

def remove_task(uid_task):
    sql_exe = ("""
                DELETE FROM ntasker where ical='%s';
            """) % (str(uid_task))
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(sql_exe)
        conn.commit()
        conn.close()
        ntasker_logs.save_events_app("Delete task from database")
        return
    except sys.exc_info()[0] as error:
        ntasker_logs.save_logs(error)
        return

def remove_all():
    sql_exe = ("""
                delete from ntasker;
            """)

    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql_exe)
    conn.commit()
    conn.close()
    ntasker_logs.save_events_app("Clear database")
    return
    

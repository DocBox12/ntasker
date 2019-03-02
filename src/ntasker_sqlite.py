#!/usr/bin/env python3


import sqlite3
import os
import ntasker_logs
import sys
import ntasker_hash


db = os.path.join(os.path.dirname(__file__), 'ntasker_database.db')

def create_db():
    sql_exe = ("""
            CREATE TABLE `ntasker` (
        	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	        `ical`	TEXT,
            'dtstart' TEXT,
            'sequence' INT
                                    );
            """)


    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql_exe)
    conn.commit()
    conn.close()
    return

def add_task(uid_task, dtstart, sequence):
    uid_task = ntasker_hash.hash(uid_task)
    dtstart = ntasker_hash.hash(dtstart)

    sql_exe = ("""
                insert into ntasker (ical, dtstart, sequence)
                VALUES("%s", "%s", "%s");
            """) % (str(uid_task), str(dtstart), int(sequence))

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

def search_task(uid_task, dtstart, sequence, rrule):
    uid_task = ntasker_hash.hash(uid_task)
    dtstart = ntasker_hash.hash(dtstart)

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
            return None
        else:
            LIST_information_about_task  = raw_data_from_sql[0]
            start_time_from_sql = LIST_information_about_task[2]
            sequence_from_sql = LIST_information_about_task[3]

            if int(sequence) > int(sequence_from_sql):
                update_sequence(uid_task, sequence)
                update_dtstart(uid_task, dtstart)
                return False
            else:
                if rrule is True:
                    if int(dtstart) > int(start_time_from_sql):
                        update_dtstart(uid_task, dtstart)
                        return False
                return True     
    except sys.exc_info()[0] as error:
        ntasker_logs.save_logs(error)
        return True   

def update_dtstart(uid_task, dtstart):
    sql_exe = ("""
                    update ntasker
                    set dtstart="%s"
                    where ical="%s";
                """) % (str(dtstart), str(uid_task)) 

    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(sql_exe)
        conn.commit()
        conn.close()
        ntasker_logs.save_events_app("Update dtstart for task in database.")
        return 
    except sys.exc_info()[0] as error:
        ntasker_logs.save_logs(error)
        return  



def update_sequence(uid_task, sequence):
    sql_exe = ("""
                update ntasker
                set sequence="%s"
                where ical="%s";
            """) % (int(sequence), str(uid_task))

    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(sql_exe)
        conn.commit()
        conn.close()
        ntasker_logs.save_events_app("Update sequence for task in database.")
        return True
    except sys.exc_info()[0] as error:
        ntasker_logs.save_logs(error)
        return False

    return 

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
    

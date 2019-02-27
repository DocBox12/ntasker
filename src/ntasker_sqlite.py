#!/usr/bin/env python3


import sqlite3
import os
import ntasker_logs


db = os.path.join(os.path.dirname(__file__), 'ntasker_database.db')

def create_db():
    sql_exe = ("""
            CREATE TABLE `ntasker` (
        	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	        `Details`	TEXT
                                    );
            """)


    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql_exe)
    conn.commit()
    conn.close()
    return

def add_task(uid_task):
    sql_exe = ("""
                insert into ntasker (Details)
                VALUES("%s");
            """) % str(uid_task)

    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql_exe)
    conn.commit()
    conn.close()
    ntasker_logs.save_events_app("Add task to database")
    return



def search_task(uid_task):
    sql_exe = ("""
                select * FROM ntasker
                where Details="%s";
            """) % str(uid_task)
            
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute(sql_exe)
    
    raw_data_from_sql = c.fetchall()
    if len(raw_data_from_sql) == 0:
        return False
    else:
        return True



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
    

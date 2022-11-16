# -*- coding: utf-8 -*-
import sqlite3
import os
import shutil

conn = None
cur = None

def AddUserToDB(id):
    id = str(id)
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()
    res = cur.execute(f"""
        SELECT EXISTS(SELECT * FROM users WHERE userid = {id})
    """)
    if res.fetchone()[0] == 0:
        cur.execute(f"""
        INSERT INTO users VALUES
        ({id},0,0,-3,-1)
        """)
        conn.commit()

def InfoAboutUser(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()
    res = cur.execute(f"""
        SELECT EXISTS(SELECT * FROM users WHERE userid = {id})
    """)
    if res.fetchone()[0] == 1:
        new_res = cur.execute(f"SELECT countwin, countlose FROM users WHERE userid = '{id}'")
        countwin, countlose = new_res.fetchone()
        return countwin, countlose
    else:
        return list(['USER_NOT_FOUND', 'USER_NOT_FOUND'])

def AllInfoAboutUser(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()
    res = cur.execute(f"""
        SELECT EXISTS(SELECT * FROM users WHERE userid = {id})
    """)
    if res.fetchone()[0] == 1:
        new_res = cur.execute(f"SELECT userid, countwin, countlose, state, session FROM users WHERE userid = '{id}'")
        all_info = list(new_res.fetchone())
        return all_info
    else:
        return list(['USER_NOT_FOUND', 'USER_NOT_FOUND', 'USER_NOT_FOUND', 'USER_NOT_FOUND', 'USER_NOT_FOUND'])

def RecreateDBs():
    dirname = os.path.dirname(__file__)
    if os.path.exists(dirname + "\\DATABASEs"):
        shutil.rmtree(dirname + "\\DATABASEs", ignore_errors = True)
    print("DATABASE CLEAR")
    
    CreateDBs()

def CreateDBs():
    dirname = os.path.dirname(__file__)
    if (os.path.exists(dirname + "\\DATABASEs")) == False:
        os.mkdir(dirname + "\\DATABASEs")
        conn = sqlite3.connect(dirname + "\\DATABASEs\\" + "Users-Sessions-Questions-Tables.db")
        cur = conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            userid TEXT,
            countwin TEXT,
            countlose TEXT,
            state INT,
            session TEXT);
        """)
        print("USERS DATABASE CREATE")
        conn.commit()

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS sessions(
            id TEXT,
            answer_id TEXT,
            player_1_id TEXT,
            player_2_id TEXT);
        """)
        print("USERS SESSIONS CREATE")
        conn.commit()

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS questions(
            id TEXT,
            answer TEXT,
            text_question TEXT);
        """)
        print("USERS QUESTIONS CREATE")
        conn.commit()

if __name__ == "__main__":
    RecreateDBs()
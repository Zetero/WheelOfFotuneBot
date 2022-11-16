# -*- coding: utf-8 -*-
import sqlite3
import os
import shutil

conn = None
cur = None

def AddUserToDB(id):
    id = str(id)
    conn = sqlite3.connect("DATABASEs\\users.db")
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
    conn = sqlite3.connect("DATABASEs\\users.db")
    cur = conn.cursor()
    res = cur.execute(f"SELECT countwin, countlose FROM users WHERE userid = '{id}'")
    countwin, countlose = res.fetchone()
    return countwin, countlose

def RecreateDBs():
    dirname = os.path.dirname(__file__)
    shutil.rmtree(dirname + "\\DATABASEs", ignore_errors = True)
    print("DATABASE CLEAR")
    CreateDBs()

def CreateDBs():
    dirname = os.path.dirname(__file__)
    if (os.path.exists(dirname + "\\DATABASEs")) == False:
        os.mkdir(dirname + "\\DATABASEs")
        conn = sqlite3.connect(dirname + "\\DATABASEs\\" + "users.db")
        cur = conn.cursor()
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            userid TEXT,
            countwin TEXT,
            countlose TEXT,
            state INT,
            sessoin TEXT);
        """)
        print("USERS DATABASE CREATE")
        conn.commit()

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            userid TEXT,
            countwin TEXT,
            countlose TEXT,
            state INT,
            sessoin TEXT);
        """)
        print("USERS DATABASE CREATE")
        conn.commit()

if __name__ == "__main__":
    CreateDBs()
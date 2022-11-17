# -*- coding: utf-8 -*-
import sqlite3
import os
import shutil
import random as r

conn = None
cur = None

def AddUserToDB(id):
    id = str(id)
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()
    res = cur.execute(f"""
        SELECT EXISTS(SELECT * FROM users WHERE id = {id})
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
        SELECT EXISTS(SELECT * FROM users WHERE id = {id})
    """)
    if res.fetchone()[0] == 1:
        new_res = cur.execute(f"SELECT countwin, countlose FROM users WHERE id = '{id}'")
        countwin, countlose = new_res.fetchone()
        return countwin, countlose
    else:
        return list(['USER_NOT_FOUND', 'USER_NOT_FOUND'])

def AllInfoAboutUser(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()
    res = cur.execute(f"""
        SELECT EXISTS(SELECT * FROM users WHERE id = {id})
    """)
    if res.fetchone()[0] == 1:
        new_res = cur.execute(f"SELECT id, countwin, countlose, state, session FROM users WHERE id = '{id}'")
        all_info = list(new_res.fetchone())
        return all_info
    else:
        return list(['USER_NOT_FOUND', 'USER_NOT_FOUND', 'USER_NOT_FOUND', 'USER_NOT_FOUND', 'USER_NOT_FOUND'])

def AddNewSession(id):
    id = str(id)
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()
    res = cur.execute(f"""
        SELECT EXISTS(SELECT * FROM users WHERE id = {id});
    """)
    conn.commit()
    if res.fetchone()[0] == 1:
        new_token = False
        token = ''
        while new_token == False:
            token = GenerateToken()
            new_res = cur.execute(f"SELECT EXISTS(SELECT * FROM sessions WHERE id = '{token}')").fetchone()
            if new_res[0] == 0:
                new_token = True

        cur.execute(f"""
        INSERT INTO sessions VALUES
        ('{token}', 'Кошелек', {id}, -1);
        """)
        print("SESSION GOOD")
        conn.commit()

        cur.execute(f"""
        UPDATE users SET session = '{token}' WHERE id = {id}
        """)
        conn.commit()
        return token
    else:
        return 'USER_NOT_FOUND'

def NewGame(id, token):
    id = str(id)
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()
    res = cur.execute(f"SELECT player_1_id FROM sessions WHERE id = '{token}';").fetchone()
    conn.commit()
    player_1_id = res[0]
    player_2_id = id
    print(player_1_id)

    if str(player_2_id) != str(player_1_id):
        res = cur.execute(f"""
            SELECT EXISTS(SELECT * FROM sessions WHERE id  = '{token}');
        """)
        if res.fetchone()[0] == 1:
            first_player = r.randint(0,1)
            new_res = cur.execute(f"""
            UPDATE sessions SET player_2_id = '{id}' WHERE id = '{token}'
            """)
            conn.commit()
            new_res = cur.execute(f"""
            UPDATE users SET session = '{token}' WHERE id = '{id}'
            """)
            conn.commit()
            if first_player == 0:
                new_res = cur.execute(f"""
                UPDATE users SET state = 0 WHERE id = '{player_1_id}'
                """)
                conn.commit()
                new_res = cur.execute(f"""
                UPDATE users SET state = 1 WHERE id = '{player_2_id}'
                """)
                conn.commit()
            else:
                new_res = cur.execute(f"""
                UPDATE users SET state = 0 WHERE id = '{player_2_id}'
                """)
                conn.commit()
                new_res = cur.execute(f"""
                UPDATE users SET state = 1 WHERE id = '{player_1_id}'
                """)
                conn.commit()

def Surrender(id):
    id = str(id)
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()

    res = cur.execute(f"""
        SELECT session FROM users WHERE id = '{id}'
    """).fetchone()
    conn.commit()
    id_session = res[0]
    if(str(id_session) != '-1'):
        res = cur.execute(f"""
            SELECT player_1_id, player_2_id FROM sessions WHERE id = '{id_session}'
        """).fetchone()
        player_1_id, player_2_id = res
        print(player_1_id)
        print(player_2_id)
        if ((id_session != '-1') and (player_2_id != '-1')):
            if str(id) == str(player_1_id):
                print("SURRENDER 1")
                countlose = cur.execute(f"SELECT countlose FROM users WHERE id = '{player_1_id}'").fetchone()
                countlose = str(int(countlose[0]) + 1)
                res = cur.execute(f"UPDATE users SET countlose = '{countlose}' WHERE id = '{player_1_id}'")
                countwin = cur.execute(f"SELECT countwin FROM users WHERE id = '{player_2_id}'").fetchone()
                countwin = str(int(countwin[0]) + 1)
                res = cur.execute(f"UPDATE users SET countwin = '{countwin}' WHERE id = '{player_2_id}'")
                conn.commit()
            elif str(id) == str(player_2_id):
                print("SURRENDER 2")
                countlose = cur.execute(f"SELECT countlose FROM users WHERE id = '{player_2_id}'").fetchone()
                countlose = str(int(countlose[0]) + 1)
                res = cur.execute(f"UPDATE users SET countlose = '{countlose}' WHERE id = '{player_2_id}'")
                conn.commit()
                countwin = cur.execute(f"SELECT countwin FROM users WHERE id = '{player_1_id}'").fetchone()
                countwin = str(int(countwin[0]) + 1)
                res = cur.execute(f"UPDATE users SET countwin = '{countwin}' WHERE id = '{player_1_id}'")
                conn.commit()

            res = cur.execute(f"UPDATE users SET session = '-1', state = -3 WHERE id = '{player_1_id}'")
            conn.commit()
            res = cur.execute(f"UPDATE users SET session = '-1', state = -3 WHERE id = '{player_2_id}'")
            conn.commit()
            DeleteSession(player_1_id)
        elif (id_session != '-1'):
            DeleteSession(player_1_id)
            
def DeleteSession(id):
    id = str(id)
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    cur = conn.cursor()
    res = cur.execute(f"""
        DELETE FROM sessions WHERE player_1_id = '{id}';
    """)
    print("DELETED")
    conn.commit()

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
            id TEXT,
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

def GenerateToken():
    token = ''
    for i in range(4):
        token += chr(r.randint(97,122))
    return token

if __name__ == "__main__":
    RecreateDBs()
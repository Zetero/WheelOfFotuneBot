# -*- coding: utf-8 -*-
import sqlite3
import os
import shutil
import Telegramm_Core
import random as r

answer = "Кошелек"
text_question = "В Греции на новый год гости кладут на порог хозяйна камень, желая ему чтобы эта вещь весила столько не меньше. Что это за вещь?"

def AddUserToDB(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"""
        SELECT EXISTS(SELECT * FROM users WHERE id = {id})
    """)
    if res.fetchone()[0] == 0:
        cur.execute(f"""
        INSERT INTO users VALUES
        ({id},0,0,-3,-1)
        """)
        ## DEL THIS ##

def InfoAboutUser(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
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
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
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
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"""
        SELECT EXISTS(SELECT * FROM users WHERE id = {id});
    """)
    ## DEL THIS ##
    if res.fetchone()[0] == 1:
        new_token = False
        token = ''
        while new_token == False:
            token = GenerateToken()
            new_res = cur.execute(f"SELECT EXISTS(SELECT * FROM sessions WHERE id = '{token}')").fetchone()
            if new_res[0] == 0:
                new_token = True

        # 1 - сделанный мной индекс
        res = cur.execute(f"SELECT answer FROM questions WHERE id = '1'").fetchone()
        answer_2 = res[0]
        current_word = "К" + "□□□□□□"#str(len(answer)-1 * "□")
        print(current_word)  

        cur.execute(f"""
        INSERT INTO sessions VALUES
        ('{token}', '{current_word}', '1', {id}, -1);
        """)
        print("SESSION GOOD")
        ## DEL THIS ##

        cur.execute(f"""
        UPDATE users SET session = '{token}' WHERE id = {id}
        """)
        ## DEL THIS ##
        return token
    else:
        return 'USER_NOT_FOUND'

def DeleteSession(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"""
        DELETE FROM sessions WHERE player_1_id = '{id}';
    """)
    print("DELETED")
    ## DEL THIS ##

def GetQuestion(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE id = '{id}')").fetchone()
    if res[0] == 1:
        res = cur.execute(f"SELECT session, state FROM users WHERE id = '{id}'").fetchone()
        print(res[0])
        print(res[1])
        if str(res[0]) != '-1' and str(res[1]) != '-3':
            res = cur.execute(f"SELECT answer_id FROM sessions WHERE id = '{res[0]}'").fetchone()
            print(res[0])
            res = cur.execute(f"SELECT text_question FROM questions WHERE id = '{res[0]}'").fetchone()
            print(res[0])
            return str(res[0])
        else:
            return "Чтобы получить вопрос - сначала начните игру!"

def GetAnswerAndWord(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE id = '{id}')").fetchone()
    if res[0] == 1:
        id = cur.execute(f"SELECT session FROM users WHERE id = '{id}'").fetchone()
        res = cur.execute(f"SELECT EXISTS(SELECT * FROM sessions WHERE id = '{id[0]}')").fetchone()
        if res[0] == 1:
            res = cur.execute(f"SELECT answer_id, current_word FROM sessions WHERE id = '{id[0]}'").fetchone()
            answer = res[0]
            current_word = res[1]
            answer = cur.execute(f"SELECT answer FROM questions WHERE id = '{answer}'").fetchone()
            print("hh")
            return (answer[0], current_word)
        else:
            return -1, -1
    else:
        return -1, -1

def GetState(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE id = '{id}')").fetchone()
    if res[0] == 1:
        res = cur.execute(f"SELECT state FROM users WHERE id = '{id}'").fetchone()
        return res[0]

def NewGame(id, token):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE id = '{id}')").fetchone()
    if res[0] == 1:
        res = cur.execute(f"SELECT EXISTS(SELECT * FROM sessions WHERE id = '{token}')").fetchone()
        ### ЕСЛИ ИГРА УЖЕ ИДЕТ И ТЫ ПЕРЕСОЗДАЕШЬ ТО ТЕБЕ ПОРАЖЕНИЕ ВРАГУ ПОБЕДА
        if res[0] == 1:
            res = cur.execute(f"SELECT player_1_id FROM sessions WHERE id = '{token}';").fetchone()
            player_1_id = res[0]
            player_2_id = id
            if str(player_2_id) != str(player_1_id):
                res = cur.execute(f"""
                    SELECT EXISTS(SELECT * FROM sessions WHERE id  = '{token}');
                """)
                first_player = 0
                if res.fetchone()[0] == 1:
                    first_player = r.randint(0,1)
                    new_res = cur.execute(f"""
                    UPDATE sessions SET player_2_id = '{id}' WHERE id = '{token}'
                    """)
                    new_res = cur.execute(f"""
                    UPDATE users SET session = '{token}' WHERE id = '{id}'
                    """)
                    if first_player == 0:
                        new_res = cur.execute(f"""
                        UPDATE users SET state = 0 WHERE id = '{player_1_id}'
                        """)
                        new_res = cur.execute(f"""
                        UPDATE users SET state = 1 WHERE id = '{player_2_id}'
                        """)
                    else:
                        new_res = cur.execute(f"""
                        UPDATE users SET state = 0 WHERE id = '{player_2_id}'
                        """)
                        new_res = cur.execute(f"""
                        UPDATE users SET state = 1 WHERE id = '{player_1_id}'
                        """)
                    Telegramm_Core.SendQuestion(player_1_id, player_2_id, first_player)
            else:
                Telegramm_Core.SendMessage(id, "Нельзя подключиться к своей же сессии.")
        else:
            Telegramm_Core.SendMessage(id, "Такой сессии не существует..")
    else:
        Telegramm_Core.SendMessage(id, "Создайте пользователя с помощью команды /start")

def Surrender(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"""
        SELECT session FROM users WHERE id = '{id}'
    """).fetchone()
    ## DEL THIS ##
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
                ## DEL THIS ##
            elif str(id) == str(player_2_id):
                print("SURRENDER 2")
                countlose = cur.execute(f"SELECT countlose FROM users WHERE id = '{player_2_id}'").fetchone()
                countlose = str(int(countlose[0]) + 1)
                res = cur.execute(f"UPDATE users SET countlose = '{countlose}' WHERE id = '{player_2_id}'")
                ## DEL THIS ##
                countwin = cur.execute(f"SELECT countwin FROM users WHERE id = '{player_1_id}'").fetchone()
                countwin = str(int(countwin[0]) + 1)
                res = cur.execute(f"UPDATE users SET countwin = '{countwin}' WHERE id = '{player_1_id}'")
                ## DEL THIS ##

            res = cur.execute(f"UPDATE users SET session = '-1', state = -3 WHERE id = '{player_1_id}'")
            ## DEL THIS ##
            res = cur.execute(f"UPDATE users SET session = '-1', state = -3 WHERE id = '{player_2_id}'")
            ## DEL THIS ##
            DeleteSession(player_1_id)
        elif (id_session != '-1'):
            DeleteSession(player_1_id)
            
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
        ## DEL THIS ##

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS sessions(
            id TEXT,
            current_word TEXT,
            answer_id TEXT,
            player_1_id TEXT,
            player_2_id TEXT);
        """)
        print("USERS SESSIONS CREATE")
        ## DEL THIS ##

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS questions(
            id TEXT,
            answer TEXT,
            text_question TEXT);
        """)
        print("USERS QUESTIONS CREATE")
        ## DEL THIS ##

        cur.executescript(f"""
        INSERT INTO questions VALUES
        ('1','{answer}', '{text_question}');
        """)
        ## DEL THIS ##
        print("QUESTION 1 READY")

def RecreateDBs():
    dirname = os.path.dirname(__file__)
    if os.path.exists(dirname + "\\DATABASEs"):
        shutil.rmtree(dirname + "\\DATABASEs", ignore_errors = True)
    print("DATABASE CLEAR")
    
    CreateDBs()

def GenerateToken():
    token = ''
    for i in range(4):
        token += chr(r.randint(97,122))
    return token

if __name__ == "__main__":
    RecreateDBs()

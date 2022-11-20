# -*- coding: utf-8 -*-
import sqlite3
import os
import shutil
import Telegramm_Core
import random as r

answer = "Кошелёк"
text_question = "В Греции на новый год гости кладут на порог хозяйна камень, желая ему чтобы эта вещь весила столько не меньше. Что это за вещь?"
conn = '' # подключаю залупу

# Создаем хендлер
class DatabaseQueryHandler():
    # иницируем те переменные которые нужны всем наследникам (например путь размещения базы)
    def __init__(self, DB_path):
        self.DB_path = DB_path
    
    # интерфейс (для чего?)
    def CreateDBs(self):
        path = self.DB_path()

# Подкласс
class SQL_DB(DatabaseQueryHandler):

    #Переопределение функции
    def CreateDBs(self):
        dirname = self.DB_path()


        # Реализация создания базы в SQL
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


# WORK
def AddUserToDB(id):
    user_exists = ExistsInDB("users", id)
    if user_exists == False:
        id = str(id)
        count_win = '0'
        count_lose = '0'
        current_step = '-3'
        current_session = '-1'
        InsertInTable("users", id, count_win, count_lose, current_step, current_session)
        return True
    else:
        return False

# WORK
def InfoAboutUser(id):
    user_exists = ExistsInDB("users", id)
    if user_exists == True:
        return list(SelectFromTable("users", id, "countwin, countlose"))
    else:
        return None, None

# WORK
def AllInfoAboutUser(id):
    user_exists = ExistsInDB("users", id)
    if user_exists == True:
        return list(SelectFromTable("users", id, "id, countwin, countlose, state, session"))
    else:
        return None

# WORK
def AddNewSession(id):
    user_exists = ExistsInDB("users", id)
    if user_exists == True:
        is_uniq_token = False
        session_id = ''
        while is_uniq_token == False:
            session_id = GenerateToken()
            session_id_exists = ExistsInDB("sessions", session_id)
            if session_id_exists == False:
                is_uniq_token = True

        # 1 - сделанный мной индекс
        answer = SelectFromTable("questions", "1", "answer")
        encrypted_word = len(answer[0]) * '🟦'
        question_id = '1'
        player_1_id = str(id)
        player_2_id = '-1'
        InsertInTable("sessions", session_id, encrypted_word, question_id, player_1_id, player_2_id)
        UpdateTable("users", "session", session_id, player_1_id)
        return session_id
    else:
        return None

# WORK
def DeleteSession(id_session):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id_session)
    cur.execute(f"""
        DELETE FROM sessions WHERE id = '{id_session}';
    """)
    conn.close()

# WORK
def GetQuestion(id):
    user_exists = ExistsInDB("users", id)
    if user_exists == True:
        session_id, state = SelectFromTable("users", id, "session, state")
        if str(session_id) != '-1' and str(state) != '-3':
            answer_id = (SelectFromTable("sessions", "'" + session_id + "'", "answer_id"))[0]
            text_question = SelectFromTable("questions", answer_id, "text_question")
            return str(text_question[0])
        else:
            return None

# WORK
def GetAnswerAndWord(id):
    id = str(id)
    user_exists = ExistsInDB("users", id)
    if user_exists == True:
        id_session = SelectFromTable("users", id, "session")[0]
        session_exists = ExistsInDB("sessions", id_session)
        if session_exists == True:
            id_answer, current_word = SelectFromTable("sessions", "'" + id_session + "'", "answer_id, current_word")
            answer = SelectFromTable("questions", id_answer, "answer")[0]
            return (answer, current_word)
        else:
            return None, None
    else:
        return None, None

# WORK
def WinGame(winner, loser, id_session):
    countwin = int(SelectFromTable("users", winner, "countwin")[0])
    countlose = int(SelectFromTable("users", loser, "countwin")[0])
    UpdateTable("users", "countwin", countwin + 1, winner)
    UpdateTable("users", "countlose", countlose + 1, loser)
    UpdateTable("users", "state", "-3", winner)
    UpdateTable("users", "state", "-3", loser)
    UpdateTable("users", "session", "-1", winner)
    UpdateTable("users", "session", "-1", loser)
    DeleteSession(id_session)

# WORK
def NextPlayerMove(id):
    id_session = SelectFromTable("users", id, "session")[0]
    player_1_id, player_2_id = SelectFromTable("sessions", "'" + id_session + "'", "player_1_id, player_2_id") 
    if str(id) == str(player_1_id):
        UpdateTable("users", "state", 1, player_1_id)
        UpdateTable("users", "state", 0, player_2_id)
        Telegramm_Core.SendMessage(player_1_id, text = "Начался ход противника.")
        Telegramm_Core.SendMessage(player_2_id, text = "Ваш ход")
    else:
        UpdateTable("users", "state", 0, player_1_id)
        UpdateTable("users", "state", 1, player_2_id)
        Telegramm_Core.SendMessage(player_2_id, text = "Начался ход противника.")
        Telegramm_Core.SendMessage(player_1_id, text = "Ваш ход")

def GetState(id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    user_exists = ExistsInDB("users", id) 
    if user_exists == True:
        player_state = SelectFromTable("users", id, "state")[0]
        return player_state

def NewGame(id, token):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    id = str(id)
    res = cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE id = '{id}')").fetchone()
    if res[0] == 1:
        res = cur.execute(f"SELECT EXISTS(SELECT * FROM sessions WHERE id = '{token}')").fetchone()
        ### ЕСЛИ ИГРА УЖЕ ИДЕТ И ТЫ ПЕРЕСОЗДАЕШЬ ТО ТЕБЕ ПОРАЖЕНИЕ ВРАГУ ПОБЕДА
        ### ЕСЛИ У ТЕБЯ УЖЕ ИДЕТ ИГРА - ПЕРЕСОЗДАТЬ НЕЛЬЗЯ
    ### ЕСЛИ ТЫ ПОДКЛЮЧАЕШЬСЯ К ИГРЕ И ТАМ НЕ СОВПАДАЕТ С ТВОЕЙ ТЕКУЩЕЙ СЕССИИ, ТО НУЖНО УДАЛИТЬ ТУ СЕССИЮ КОТОРАЯ БУДЕТ ПУСТОЙ
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
                        
                    question = GetQuestion(player_1_id)
                    Telegramm_Core.SendMessage(player_1_id, "Игра началась!")
                    Telegramm_Core.SendMessage(player_2_id, "Игра началась!")
                    Telegramm_Core.SendMessage(player_1_id, question)
                    Telegramm_Core.SendMessage(player_2_id, question)

                    closed_answer = GetAnswerAndWord(player_1_id)[1]
                    Telegramm_Core.SendMessage(player_1_id, "Слово: " + closed_answer)
                    Telegramm_Core.SendMessage(player_2_id, "Слово: " + closed_answer)

                    if first_player == 0:
                        Telegramm_Core.SendMessage(player_1_id, "Ваш ход")
                        Telegramm_Core.SendMessage(player_2_id, "Сейчас идёт ход противника")
                    else:
                        Telegramm_Core.SendMessage(player_2_id, "Ваш ход")
                        Telegramm_Core.SendMessage(player_1_id, "Сейчас идёт ход противника")

                    
            else:
                Telegramm_Core.SendMessage(id, "Нельзя подключиться к своей же сессии.")
        else:
            Telegramm_Core.SendMessage(id, "Такой сессии не существует..")
    else:
        Telegramm_Core.SendMessage(id, "Создайте пользователя с помощью команды /start")

def Surrender(id):
    id = str(id)
    # Проверку на существование пользователя / игры
    id_session = SelectFromTable("users", id, "session")[0]
    if(str(id_session) != '-1'):
        player_1_id, player_2_id = SelectFromTable("sessions", "'" + id_session + "'", "player_1_id, player_2_id")
        if (player_2_id != '-1'):
            if str(id) == str(player_1_id):
                countlose = int(SelectFromTable("users", player_1_id, "countlose")[0]) + 1
                UpdateTable("users", "countlose", str(countlose), player_1_id)
                countwin = int(SelectFromTable("users", player_2_id, "countwin")[0]) + 1
                UpdateTable("users", "countwin", str(countwin), player_2_id)
                Telegramm_Core.SendMessage(player_1_id, "Вам засчитано поражение.")
                Telegramm_Core.SendMessage(player_2_id, "Ваш противник сдался. Поздравляем с преждевременной победой!")
            elif str(id) == str(player_2_id):
                countlose = int(SelectFromTable("users", player_2_id, "countlose")[0]) + 1
                UpdateTable("users", "countlose", str(countlose), player_2_id)
                countwin = int(SelectFromTable("users", player_1_id, "countwin")[0]) + 1
                UpdateTable("users", "countwin", str(countwin), player_1_id)
                Telegramm_Core.SendMessage(player_2_id, "Вам засчитано поражение.")
                Telegramm_Core.SendMessage(player_1_id, "Ваш противник сдался. Поздравляем с преждевременной победой!")

            UpdateTable("users", "session", "-1", player_1_id)
            UpdateTable("users", "session", "-1", player_2_id)
            UpdateTable("users", "state", "-3", player_1_id)
            UpdateTable("users", "state", "-3", player_2_id)
            DeleteSession(id_session)
        elif (id_session != '-1'):
            DeleteSession(id_session)
        # ВЫ СДАЛИСЬ НАПИСАТЬ
            
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

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS sessions(
            id TEXT,
            current_word TEXT,
            answer_id TEXT,
            player_1_id TEXT,
            player_2_id TEXT);
        """)
        print("USERS SESSIONS CREATE")

        cur.executescript("""
        CREATE TABLE IF NOT EXISTS questions(
            id TEXT,
            answer TEXT,
            text_question TEXT);
        """)
        print("USERS QUESTIONS CREATE")
        
        InsertInTable("questions", "1", answer, text_question)
        print(answer, text_question)
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

# Check if object exists in DB
def ExistsInDB(table, id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    print(f"SELECT EXISTS(SELECT * FROM {table} WHERE id = '{id}')")
    res = cur.execute(f"SELECT EXISTS(SELECT * FROM '{table}' WHERE id = '{id}')").fetchone()
    is_exists = res[0]
    conn.close()
    return bool(is_exists)

def InsertInTable(table, *args):
    table = str(table)
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    count_args = str(len(args) * "?,")[:-1]
    cur.execute(f"INSERT INTO '{table}' VALUES ({count_args})", args)
    conn.close()

def SelectFromTable(table, id, values):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    print(f"SELECT {values} FROM {table} WHERE id = {id}")
    res = cur.execute(f"SELECT {values} FROM {table} WHERE id = {id}").fetchone() 
    conn.close()
    return list(res)

def UpdateTable(table, changeable_field, value, id):
    conn = sqlite3.connect("DATABASEs\\Users-Sessions-Questions-Tables.db")
    conn.isolation_level = None
    cur = conn.cursor()
    print(f"UPDATE {table} SET {changeable_field} = '{value}' WHERE id = '{id}'")
    cur.execute(f"UPDATE {table} SET {changeable_field} = '{value}' WHERE id = '{id}'")
    conn.close()

# -*- coding: utf-8 -*-
import telebot
from telebot import types
from DatabaseQueryHandlerClass import *
import Interface_Core
import argparse
import os

FULL_INFO_COMMAND = "full_info"
INFO_COMMAND = "info"
CREATE_USER_COMMAND = "create_user"
HELP_COMMAND = "help"
SEND_QUESTION_COMMAND = "q"
NEW_GAME_COMMAND = "ng"
SURRENDER_COMMAND = "surrender"

bot = telebot.TeleBot(token = "5402715304:AAGqXbYSTkiC6GCvD7OCUJP57dbW_-jK704")
database_engine = 'SQLLITE'
database_path = os.path.dirname(__file__)
first_launch = "N"
database = ''

parser = argparse.ArgumentParser(description = "Parse args")
parser.add_argument('--bot_token', help = "Enter token a telegramm bot", type = str)
parser.add_argument('--database_engine', help = """
Select the database you want to use in the project. (Available databases: \"SQLLITE\")
""", type = str)
parser.add_argument('--database_path', help = "Enter the path to the Database folder", type = str)
parser.add_argument('--first_lauch', help = """
Enter \"Y\" if you are launching the bot for the first time or want to recreate the database. 
This action is required to create tables in the database""", type = str)
args = parser.parse_args()

if args.bot_token:
    bot = telebot.TeleBot(token = args.bot_token)

if args.database_engine:
    database_engine = args.database_engine

if args.database_path:
    database_path = args.database_path

if args.first_lauch:
    first_launch = args.first_lauch

@bot.message_handler(commands = [HELP_COMMAND])
def SendHelp(message):
    clientId = message.chat.id
    SendHelpMessage(clientId)

@bot.message_handler(commands = [CREATE_USER_COMMAND, "start"])
def CreateUser(message):
    clientId = message.chat.id
    if database.AddUserToDB(clientId):
        bot.send_message(chat_id = clientId, text= "✅ Пользователь создан ✅", parse_mode = "html", reply_markup = None)
    else:
        bot.send_message(chat_id = clientId, text= "❌ Пользователь уже существует ❌", parse_mode = "html", reply_markup = None)

@bot.message_handler(commands = [INFO_COMMAND])
def SendInfo(message):
    clientId = message.chat.id
    countwin, countlose = database.InfoAboutUser(clientId)
    if countlose != None:
        bot.send_message(chat_id = clientId, text = f"""
        😎  Количество ваших побед: {countwin}\n😔  Количество ваших поражений: {countlose}
        """, parse_mode = "html")
    else:
        SendHelpMessage(clientId)

@bot.message_handler(commands = [SURRENDER_COMMAND])
def Surrender(message):
    clientId = message.chat.id
    database.Surrender(clientId)

@bot.message_handler(commands = [NEW_GAME_COMMAND])
def StartNewGame(message):
    clientId = message.chat.id
    token = database.AddNewSession(clientId)
    if token != None:
        bot.send_message(chat_id = clientId, text = "🔑 Ваш токен сессии: "+ token, parse_mode = "html")
    else:
        SendHelpMessage(clientId)

@bot.message_handler(commands = [SEND_QUESTION_COMMAND])
def SendQuestionText(message):
    clientId = message.chat.id
    user_exists = database.ExistsInDB("users", id = clientId)
    if user_exists == True:
        question = database.GetQuestion(clientId)
        if question == None:
            bot.send_message(chat_id = clientId, text = f"❌ Чтобы получить вопрос - сначала начните игру ❌", parse_mode = "html")
        else:
            SendMessage(clientId, f"Ваш вопрос:\n{question}")
    else:
        SendHelpMessage(clientId)

@bot.message_handler(commands = [FULL_INFO_COMMAND])
def SendFullInfo(message):
    clientId = message.chat.id
    all_info = database.AllInfoAboutUser(clientId)
    state = ''
    if all_info[3] == -3:
        state = 'Empty session'
    elif all_info[3] == 0:
        state = 'NewLetter'
    elif all_info[3] == 1:
        state = 'NextStep'

    if all_info != None:
        bot.send_message(chat_id = clientId, text = f"Info:\nID: {str(all_info[0])}\nCount Win: {str(all_info[1])}\n\
Count Lose: {str(all_info[2])}\nState: {str(state)}\nSession: {str(all_info[4])}\n", parse_mode = "html")
    else:
        SendHelpMessage(clientId)

@bot.message_handler()
def Msg_Handler(message):
    clientId = message.chat.id
    if len(message.text) == 4:
        database.NewGame(clientId, message.text)
    elif database.GetState(clientId) != -3:
        if database.GetState(clientId) == 0:
            Interface_Core.NextRound(clientId, message.text, database)
        elif database.GetState(clientId) == 1:
            bot.send_message(chat_id = clientId, text = "❌ Сейчас ход противника ❌", parse_mode = "html")
        else:
            bot.send_message(chat_id = clientId, text = f"❔ Напишите /{HELP_COMMAND} для дополнительной информации о функционале бота ❔", parse_mode = "html")

def SendMessage(id, text):
    bot.send_message(chat_id = id, text = f"{text}", parse_mode = "html")

def SendHelpMessage(clientId):
    clientId
    bot.send_message(chat_id = clientId, text=f"""
🍀Вас приветствует игровой бот "Поле Чудес"! 🍀
Для того чтобы начать игру - вам потребуется создать пользователя
Не переживайте. Для этого вам не нужно куда-то лезть и регистрироваться.
Достаточно написать команду /{CREATE_USER_COMMAND}
После того как вы создадите пользователя вы можете создать игру.
Для этого напишите /{NEW_GAME_COMMAND}
При создании новой игры - вам придет токен игровой сессии. Для начала игры - напишите своему другу четырёхзначный код
⚠️ Второй игрок тоже должен иметь игровой аккаунт ⚠️
📊 Хотите узнать игровую статистику пишите /{INFO_COMMAND} 📊 
❔ Забыли вопрос? Смело пишите команду /{SEND_QUESTION_COMMAND} ❔ 
Для повторения данного информационного сообщения пишите /{HELP_COMMAND}
Также не забывайте что основные команды присутсвуют в цифровом меню
""", parse_mode = "html")

if __name__ == "__main__":
    database = ''
    if database_engine == "SQLLITE":
        database = SQL_DB(database_path, "D:\\Projects\\GitHub\\WheelOfFotuneBot\\json_path.json")
    if first_launch == "Y":
        database.CreateDBs()
    bot.polling(none_stop = True)
    
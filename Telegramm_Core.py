# -*- coding: utf-8 -*-
import telebot
from telebot import types
import SQL_Core
import Interface_Core
import argparse

FULL_INFO_COMMAND = "full_info"
INFO_COMMAND = "info"
CREATE_USER_COMMAND = "create_user"
HELP_COMMAND = "help"
SEND_QUESTION_COMMAND = "q"
NEW_GAME_COMMAND = "ng"
SURRENDER_COMMAND = "surrender"

parser = argparse.ArgumentParser(description = "Parse args")
parser.add_argument('--bot_token', help = "Enter token a telegramm bot", type = str)
parser.add_argument('--database_engine', help = """
Select the database you want to use in the project. (Available databases: \"SQLLITE\")
""", type = str)
parser.add_argument('--first_lauch', help = """
Enter \"Y\" if you are launching the bot for the first time or want to recreate the database. 
This action is required to create tables in the database""", type = str)
args = parser.parse_args()

if args.token_path:
    with open(args.token_path, 'r') as f:
        token =  f.readlines()
        token = token[1].strip('\n')
        bot = telebot.TeleBot(token = token)
else:
    with open('tokens.txt', 'r') as f:
        token =  f.readlines()
        token = token[1].strip('\n')
        bot = telebot.TeleBot(token = token) 

if args.token_path:
    with open(args.token_path, 'r') as f:
        token =  f.readlines()
        token = token[1].strip('\n')
        bot = telebot.TeleBot(token = token)
else:
    with open('tokens.txt', 'r') as f:
        token =  f.readlines()
        token = token[1].strip('\n')
        bot = telebot.TeleBot(token = token) 

bot = telebot.TeleBot(token = "5402715304:AAGqXbYSTkiC6GCvD7OCUJP57dbW_-jK704")

@bot.message_handler(commands = [CREATE_USER_COMMAND, "start"])
def CreateUserTable(message):
    clientId = message.chat.id
    if SQL_Core.AddUserToDB(clientId):
        bot.send_message(chat_id = clientId, text= "Пользователь создан!", parse_mode = "Markdown")
    else:
        bot.send_message(chat_id = clientId, text= "Пользователь уже существует!", parse_mode = "Markdown")

@bot.message_handler(commands = [INFO_COMMAND])
def SendInfo(message):
    clientId = message.chat.id
    countwin, countlose = SQL_Core.InfoAboutUser(clientId)
    if countlose != None:
        bot.send_message(chat_id = clientId, text = f"""
        😎  Количество ваших побед: {countwin}\n😔  Количество ваших поражений: {countlose}
        """, parse_mode = "Markdown")
    else:
        bot.send_message(chat_id = clientId, text = f"Пользователь не найден. Напишите боту /{CREATE_USER_COMMAND} для создания пользователя", parse_mode = "Markdown")

@bot.message_handler(commands = [SURRENDER_COMMAND])
def Surrender(message):
    clientId = message.chat.id
    SQL_Core.Surrender(clientId)

@bot.message_handler(commands = [NEW_GAME_COMMAND])
def StartNewGame(message):
    clientId = message.chat.id
    token = SQL_Core.AddNewSession(clientId)
    if token != None:
        bot.send_message(chat_id = clientId, text = "Ваш токен сессии: "+ token, parse_mode = "Markdown")
    else:
        bot.send_message(chat_id = clientId, text = f"Пользователь не найден. Напишите боту /{CREATE_USER_COMMAND} для создания пользователя", parse_mode = "Markdown")

@bot.message_handler(commands = [SEND_QUESTION_COMMAND])
def SendQuestionText(message):
    clientId = message.chat.id
    question = SQL_Core.GetQuestion(clientId)
    if question == None:
        bot.send_message(chat_id = clientId, text = f"Чтобы получить вопрос - сначала начните игру.", parse_mode = "Markdown")
    else:
        SendMessage(clientId, f"Ваш вопрос:\n{question}")

@bot.message_handler(commands = [FULL_INFO_COMMAND])
def SendFullInfo(message):
    clientId = message.chat.id
    all_info = SQL_Core.AllInfoAboutUser(clientId)
    state = ''
    if all_info[3] == -3:
        state = 'Empty session'
    elif all_info[3] == -2:
        state = 'Loser'
    elif all_info[3] == -1:
        state = 'Surrender'
    elif all_info[3] == 0:
        state = 'NewLetter'
    elif all_info[3] == 1:
        state = 'NextStep'
    elif all_info[3] == 2:
        state = 'Winner'

    if all_info != None:
        bot.send_message(chat_id = clientId, text = f"Info:\nID: {str(all_info[0])}\nCount Win: {str(all_info[1])}\n\
Count Lose: {str(all_info[2])}\nState: {str(state)}\nSession: {str(all_info[4])}\n", parse_mode = "Markdown")
    else:
        bot.send_message(chat_id = clientId, text = f"Пользователь не найден. Напишите боту /{CREATE_USER_COMMAND} для создания пользователя", parse_mode = "Markdown")

# @bot.message_handler(commands = [DATABASE_RECREATE_COMMAND])
# def ClearDBs(message):
#     clientId = message.chat.id
#     SQL_Core.RecreateDBs()
#     bot.send_message(chat_id = clientId, text = f"DATABASE RECREATED. CREATE NEW USER (/{CREATE_USER_COMMAND})", parse_mode = "Markdown")

@bot.message_handler()
def Msg_Handler(message):
    clientId = message.chat.id
    if len(message.text) == 4:
        SQL_Core.NewGame(clientId, message.text)
    elif SQL_Core.GetState(clientId) != -3:
        if SQL_Core.GetState(clientId) == 0:
            Interface_Core.NextRound(clientId, message.text)
        elif SQL_Core.GetState(clientId) == 1:
            bot.send_message(chat_id = clientId, text = "Сейчас ход противника", parse_mode = "Markdown")
        else:
            bot.send_message(chat_id = clientId, text = f"Напишите /{HELP_COMMAND} для дополнительной информации о функционале бота.", parse_mode = "Markdown")

def SendMessage(id, text):
    bot.send_message(chat_id = id, text = f"{text}", parse_mode = "Markdown")

if __name__ == "__main__":

    SQL_Core.RecreateDBs()
    print("START TELEGRAMM BOT")
    bot.polling(none_stop = True)
    
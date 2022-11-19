# -*- coding: utf-8 -*-
import telebot
from telebot import types
import SQL_Core
import re
import Interface_Core

DATABASE_RECREATE_COMMAND = "12345"
FULL_INFO_COMMAND = "54321"

bot = telebot.TeleBot(token = "5402715304:AAGqXbYSTkiC6GCvD7OCUJP57dbW_-jK704")

@bot.message_handler(commands = ["start"])
def CreateUserTable(message):
    clientId = message.chat.id
    SQL_Core.AddUserToDB(clientId)
    bot.send_message(chat_id = clientId, text= "ЗАТЫЧКА", parse_mode = "Markdown")

@bot.message_handler(commands = ["recreate"])
def ReCreateUserTable(message):
    clientId = message.chat.id
    SQL_Core.AddUserToDB(clientId)
    bot.send_message(chat_id = clientId, text= "ЗАТЫЧКА!", parse_mode = "Markdown")

@bot.message_handler(commands = ["info"])
def SendInfo(message):
    clientId = message.chat.id
    countwin, countlose = SQL_Core.InfoAboutUser(clientId)
    bot.send_message(chat_id = clientId, text = f"""
    😎  Количество ваших побед: {countwin}\n😔  Количество ваших поражений: {countlose}
    """, parse_mode = "Markdown")

@bot.message_handler(commands = ["surrender"])
def Surrender(message):
    clientId = message.chat.id
    SQL_Core.Surrender(clientId)

@bot.message_handler(commands = ["ng"])
def StartNewGame(message):
    clientId = message.chat.id
    token = SQL_Core.AddNewSession(clientId)
    bot.send_message(chat_id = clientId, text = "Ваш токен: "+ token, parse_mode = "Markdown")

@bot.message_handler(commands = ["q"])
def SendQuestionText(message):
    clientId = message.chat.id
    SendQuestion(clientId, None)

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
    bot.send_message(chat_id = clientId, text = f"Info:\nID: {str(all_info[0])}\nCount Win: {str(all_info[1])}\n\
Count Lose: {str(all_info[2])}\nState: {str(state)}\nSession: {str(all_info[4])}\n", parse_mode = "Markdown")

@bot.message_handler(commands = [DATABASE_RECREATE_COMMAND])
def ClearDBs(message):
    clientId = message.chat.id
    SQL_Core.RecreateDBs()
    bot.send_message(chat_id = clientId, text = "DATABASE RECREATED. CREATE NEW USER (/start)", parse_mode = "Markdown")

@bot.message_handler()
def Msg_Handler(message):
    clientId = message.chat.id
    if len(message.text) == 4:
        SQL_Core.NewGame(clientId, message.text)
    elif SQL_Core.GetState(clientId) != -3:
        if SQL_Core.GetState(clientId) == 0:
            Interface_Core.NextRound(clientId, message.text)
        elif SQL_Core.GetState(clientId) == 1:
            bot.send_message(chat_id = clientId, text = "Сейчас ход противника, олень!", parse_mode = "Markdown")
        ## Переделать мб?
        else:
            bot.send_message(chat_id = clientId, text = "Напишите /help для дополнительной информации о функционале бота.", parse_mode = "Markdown")

def SendQuestion(id1, id2, first_player):
    question = SQL_Core.GetQuestion(id1)
    if id1 != None:
        bot.send_message(chat_id = id1, text = f"Ваш вопрос:\n{question}", parse_mode = "Markdown")
    if id2 != None:
        bot.send_message(chat_id = id2, text = f"Ваш вопрос:\n{question}", parse_mode = "Markdown")
    if first_player == 0:
        bot.send_message(chat_id = id1, text = f"Ваш ход:\nВведите букву:", parse_mode = "Markdown")
        bot.send_message(chat_id = id2, text = f"Сейчас идёт ход противника:", parse_mode = "Markdown")
    else:
        bot.send_message(chat_id = id2, text = f"Ваш ход:\nВведите букву:", parse_mode = "Markdown")
        bot.send_message(chat_id = id1, text = f"Сейчас идёт ход противника:", parse_mode = "Markdown")

def SendMessage(id, text):
    bot.send_message(chat_id = id, text = f"{text}", parse_mode = "Markdown")

if __name__ == "__main__":
    SQL_Core.RecreateDBs()
    print("START TELEGRAMM BOT")
    bot.polling(none_stop = True)
    
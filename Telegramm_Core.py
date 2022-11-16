# -*- coding: utf-8 -*-
import telebot
from telebot import types
import SQL_Core

DATABASE_RECREATE_COMMAND = "12345"

bot = telebot.TeleBot(token = "5402715304:AAGqXbYSTkiC6GCvD7OCUJP57dbW_-jK704")

@bot.message_handler(commands = ["start"])
def CreateUserTable(message):
    clientId = message.chat.id
    SQL_Core.AddUserToDB(clientId)
    bot.send_message(chat_id = clientId, text= "Hello!")

@bot.message_handler(commands = ["info"])
def SendInfo(message):
    clientId = message.chat.id
    countwin, countlose = SQL_Core.InfoAboutUser(clientId)
    bot.send_message(chat_id = clientId, text = f"""
    😎  Количество ваших побед: {countwin}\n😔  Количество ваших поражений: {countlose}
    """)

@bot.message_handler(commands = [DATABASE_RECREATE_COMMAND])
def ClearDBs(message):
    SQL_Core.RecreateDBs()

if __name__ == "__main__":
    print("START TELEGRAMM BOT")
    bot.polling(none_stop = True)
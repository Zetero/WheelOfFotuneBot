# -*- coding: utf-8 -*-
from enum import Enum
import re
import Bot_Core

class State(Enum):
    EmptySession = -3
    Loser = -2
    Surrender = -1
    NewLetter = 0
    NextStep = 1
    Winner = 2

def NextRound(id, letter, database):
    answer, word = database.GetAnswerAndWord(id)
    word = str(word)
    id_session = database.SelectFromTable("users", id, "session")[0] 
    player_1_id, player_2_id = database.SelectFromTable("sessions", "'" + id_session + "'", "player_1_id, player_2_id") 
                
    if answer != -1 and word != -1:
        answer = str(answer).upper()
        letter = str(letter)
        letter = letter.upper()

        if len(letter) == 1 and (bool(re.search("[а-яА-ЯеЁ]", letter)) == True):
            if letter in word: 
                Bot_Core.SendMessage(id, "Такая буква уже есть в слове.")
            elif letter in answer and len(letter) == 1:
                Bot_Core.SendMessage(id, "Есть такая буква! Откройте!")
                word = list(word)
                all_ind = [m.start() for m in re.finditer(letter, answer)]
                for ind in all_ind:
                    word[ind] = letter
                word = "".join(word)
                database.UpdateTable("sessions", "current_word", word, id_session)
                if str(id) == str(player_1_id):
                    Bot_Core.SendMessage(id, "Слово: " + str(word))
                    Bot_Core.SendMessage(player_2_id, f"Соперник назвал букву \"{letter}\"")
                    Bot_Core.SendMessage(player_2_id, "Слово: " + str(word))
                if str(id) == str(player_2_id):
                    Bot_Core.SendMessage(player_2_id, "Слово: " + str(word))
                    Bot_Core.SendMessage(player_1_id, f"Соперник назвал букву \"{letter}\"")
                    Bot_Core.SendMessage(player_1_id, "Слово: " + str(word))
            else:
                Bot_Core.SendMessage(id, f"В слове нет буквы: \"{letter}\"")
                if str(id) != str(player_1_id):
                    Bot_Core.SendMessage(player_1_id, f"В слове нет буквы: \"{letter}\"")
                else:
                    Bot_Core.SendMessage(player_2_id, f"В слове нет буквы: \"{letter}\"")
                database.NextPlayerMove(id)
                
        elif (bool(re.search("[а-яА-Я]", letter)) == False):
            Bot_Core.SendMessage(id, "Только русские символы.")
        else:
            if letter == answer:
                if str(id) == str(player_1_id):
                    Bot_Core.SendMessage(player_1_id, "Вы назвали все слово сразу! Вы победитель!")
                    database.WinGame(player_1_id, player_2_id, id_session)
                    Bot_Core.SendMessage(player_2_id, f"Противник назвал все слово сразу!\nПравильный ответ был: {answer}\nУвы, вы проиграли.")       
                else:
                    Bot_Core.SendMessage(player_2_id, "Вы назвали все слово сразу! Вы победитель!")
                    Bot_Core.SendMessage(player_1_id, f"Противник назвал все слово сразу!\nПравильный ответ был: {answer}\nУвы, вы проиграли.")
            else:
                Bot_Core.SendMessage(id, "Вы написали больше одной буквы.")

        if word == answer:
            if str(id) == str(player_1_id):
                Bot_Core.SendMessage(player_1_id, "Вы победитель!")
                database.WinGame(player_1_id, player_2_id, id_session)
                Bot_Core.SendMessage(player_2_id, f"Противник открыл все слово!\nПравильный ответ был: {answer}\nУвы, вы проиграли.")       
            else:
                Bot_Core.SendMessage(player_2_id, "Вы победитель!")
                Bot_Core.SendMessage(player_1_id, f"Противник открыл все слово!\nПравильный ответ был: {answer}\nУвы, вы проиграли.")

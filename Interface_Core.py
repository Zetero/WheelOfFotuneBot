# -*- coding: utf-8 -*-
from enum import Enum
import re
import SQL_Core
import Telegramm_Core

class State(Enum):
    EmptySession = -3
    Loser = -2
    Surrender = -1
    NewLetter = 0
    NextStep = 1
    Winner = 2

def NextRound(id, letter):
    answer, word = SQL_Core.GetAnswerAndWord(id)
    word = str(word)
    id_session = SQL_Core.SelectFromTable("users", id, "session")[0] 
    player_1_id, player_2_id = SQL_Core.SelectFromTable("sessions", "'" + id_session + "'", "player_1_id, player_2_id") 
                
    if answer != -1 and word != -1:
        answer = str(answer).upper()
        letter = str(letter)
        letter = letter.upper()

        if len(letter) == 1 and (bool(re.search("[а-яА-Я]", letter)) == True):
            if letter in word: 
                Telegramm_Core.SendMessage(id, "Такая буква уже есть в слове.")
            elif letter in answer and len(letter) == 1:
                Telegramm_Core.SendMessage(id, "Есть такая буква! Откройте!")
                word = list(word)
                all_ind = [m.start() for m in re.finditer(letter, answer)]
                for ind in all_ind:
                    word[ind] = letter
                word = "".join(word)
                SQL_Core.UpdateTable("sessions", "current_word", word, id_session)
                if str(id) == str(player_1_id):
                    Telegramm_Core.SendMessage(id, "Слово: " + str(word))
                    Telegramm_Core.SendMessage(player_2_id, f"Соперник назвал букву \"{letter}\"")
                    Telegramm_Core.SendMessage(player_2_id, "Слово: " + str(word))
                if str(id) == str(player_2_id):
                    Telegramm_Core.SendMessage(player_2_id, "Слово: " + str(word))
                    Telegramm_Core.SendMessage(player_1_id, f"Соперник назвал букву \"{letter}\"")
                    Telegramm_Core.SendMessage(player_1_id, "Слово: " + str(word))
            else:
                Telegramm_Core.SendMessage(id, f"В слове нет буквы: \"{letter}\"")
                if str(id) != str(player_1_id):
                    Telegramm_Core.SendMessage(player_1_id, f"В слове нет буквы: \"{letter}\"")
                else:
                    Telegramm_Core.SendMessage(player_2_id, f"В слове нет буквы: \"{letter}\"")
                SQL_Core.NextPlayerMove(id)
                
        elif (bool(re.search("[а-яА-Я]", letter)) == False):
            Telegramm_Core.SendMessage(id, "Только русские символы.")
        else:
            if letter == answer:
                if str(id) == str(player_1_id):
                    Telegramm_Core.SendMessage(player_1_id, "Вы назвали все слово сразу! Вы победитель!")
                    SQL_Core.WinGame(player_1_id, player_2_id, id_session)
                    Telegramm_Core.SendMessage(player_2_id, f"Противник назвал все слово сразу!\nПравильный ответ был: {answer}\nУвы, вы проиграли.")       
                else:
                    Telegramm_Core.SendMessage(player_2_id, "Вы назвали все слово сразу! Вы победитель!")
                    Telegramm_Core.SendMessage(player_1_id, f"Противник назвал все слово сразу!\nПравильный ответ был: {answer}\nУвы, вы проиграли.")
            else:
                Telegramm_Core.SendMessage(id, "Вы написали больше одной буквы.")

        if word == answer:
            if str(id) == str(player_1_id):
                Telegramm_Core.SendMessage(player_1_id, "Вы победитель!")
                SQL_Core.WinGame(player_1_id, player_2_id, id_session)
                Telegramm_Core.SendMessage(player_2_id, f"Противник открыл все слово!\nПравильный ответ был: {answer}\nУвы, вы проиграли.")       
            else:
                Telegramm_Core.SendMessage(player_2_id, "Вы победитель!")
                Telegramm_Core.SendMessage(player_1_id, f"Противник открыл все слово!\nПравильный ответ был: {answer}\nУвы, вы проиграли.")

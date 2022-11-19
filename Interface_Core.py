# -*- coding: utf-8 -*-
from enum import Enum
import re
import SQL_Core

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
    if answer != -1 and word != -1:
        answer = str(answer).upper()
        letter = str(letter)
        letter = letter.upper()

        if letter in word and len(letter) == 1:
            print("Буква уже открыта!")
        elif letter in answer and len(letter) == 1:
            print("Есть такая буква!")
            word = list(word)
            all_ind = [m.start() for m in re.finditer(letter, answer)]
            print(word)
            for ind in all_ind:
                print(ind)
                word[ind] = letter
            word = "".join(word)
        elif letter == answer:
            print("Открыть все слово сразу! Победитель!")
        else:
            print("Нет такой буквы!")

        if word == answer:
            print("Победитель!")

        
    #         elif (bool (re.search("[a-zA-Z]", letter)) == True) and (len(letter) == 1):
    #             print("Ну да, ну да.. Я же не сказал кириллицу, верно? Ну вот теперь говорю. ТОЛЬКО КИРИЛЛИЦА!")
    #         elif (bool (re.search("[0-9]", letter)) == True) and (len(letter) == 1):
    #             print("Цифры? Серьёзно?")
    #         elif (bool (re.search("[а-яА-Я]", letter)) == False) and (len(letter) == 1):
    #             print("Написано же \"БУКВЫ\"")
    #         elif (len(letter) > 1 and letter != STOPGAMEWORD):
    #             print("Вы ввели больше одного символа!")


    #         else:
    #             if letter != STOPGAMEWORD:
    #                 if letter in answer:
    #                     print("Есть такая буква!")
    #                     all_ind = [m.start() for m in re.finditer(letter, answer)]
    #                     print(all_ind)
    #                     word = list(word)
    #                     for ind in all_ind:
    #                         print(ind)
    #                         word[ind] = letter
    #                     word = "".join(word)
    #                     if word == answer:
    #                         current_state = State.Winner
    #                 else:
    #                     print("Нет такой буквы!")
    #                     current_state = State.NextStep

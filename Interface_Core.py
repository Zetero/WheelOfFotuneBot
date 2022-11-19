# -*- coding: utf-8 -*-
from enum import Enum
import re
import SQL_Core

STOPGAMEWORD = "GG"

answer = "Кошелек"
question = "В Греции на новый год гости кладут на порог хозяйна камень, желая ему чтобы эта вещь весила столько не меньше. Что это за вещь?"
word = ""


class State(Enum):
    EmptySession = -3
    Loser = -2
    Surrender = -1
    NewLetter = 0
    NextStep = 1
    Winner = 2

# STATE долдно быть NEW LETTER


def NextRound(id, letter):
    answer, word = SQL_Core.GetAnswerAndWord(id)
    if answer != -1 and word != -1:
        answer = str(answer).upper()
        letter = str(letter)
        letter = letter.upper()

    #         elif (bool (re.search("[a-zA-Z]", letter)) == True) and (len(letter) == 1):
    #             print("Ну да, ну да.. Я же не сказал кириллицу, верно? Ну вот теперь говорю. ТОЛЬКО КИРИЛЛИЦА!")
    #         elif (bool (re.search("[0-9]", letter)) == True) and (len(letter) == 1):
    #             print("Цифры? Серьёзно?")
    #         elif (bool (re.search("[а-яА-Я]", letter)) == False) and (len(letter) == 1):
    #             print("Написано же \"БУКВЫ\"")
    #         elif (len(letter) > 1 and letter != STOPGAMEWORD):
    #             print("Вы ввели больше одного символа!")

        if letter in answer:
            print("Есть такая буква!")
            word = list(word)
            all_ind = [m.start() for m in re.finditer(letter, answer)]
            for ind in all_ind:
                print(ind)
                word[ind] = letter
                word = "".join(word)
                if word == answer:
                    print("Победитель!")
        elif letter in word:
            print("Буква уже открыта!")
        else:
            print("Нет такой буквы!")
            current_state = State.NextStep

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

    #         if letter == STOPGAMEWORD:
    #             current_state = State.Surrender


if __name__ == "__main__":
    answer = "Кошелек"
    question = "В Греции на новый год гости кладут на порог хозяйна камень, желая ему чтобы эта вещь весила столько не меньше. Что это за вещь?"
    word = ""
    # NextRound()

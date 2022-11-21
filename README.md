# WheelOfFotuneBot #
This bot repeats the American game "Wheel of Fortune" (for Russians - "Поле чудес"). Players and questions are stored in the database permanently, sessions are deleted after the end of the game. Tokens consist of 4 English characters, i.e. the maximum number of pairs of players can be 456976.

## Package used in the project ##
pyTelegramBotAPI 4.7.1

## Supported databases ##
- SQLite3

## Supported import ##
In order to import your json into a database, it must have the structure:

[
    {
        "id": 1 (int),
        "answer": "answer" (str), 
        "question": "question" (str)
    }
]

## Available Command line options ##
--bot_token - Enter token a telegramm bot
--database_engine - Select the database you want to use in the project
--database_path - Enter the path to the Database folder
--first_lauch - Enter "Y" if you are launching the bot for the first time or want to recreate the database. This action is required to create tables in the database

### P.S. a filled json file with 2079 questions and answers (in Russian) is in the project folder ###
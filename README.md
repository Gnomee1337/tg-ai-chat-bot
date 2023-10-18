# tg-ai-chat-bot
Unlimited Telegram AI Chat Bot based on [gpt4free](https://github.com/xtekky/gpt4free) using Aiogram

Allows you to maintain long-term communication with AI by saving/requesting unique history from your database for each user

## Setup Bot:
1. Create DB 
    - Import sql template [./database/bot_database.sql](./database/bot_database.sql)
1. Create `.env` (based on `.env.example`) and fill it
1. `pip install -r requirements.txt`
1. Run `main.py`
* [You can change this line for gpt4free AI provider model](./handlers/user_questions.py?plain=1#L110) as it mentioned on [gpt4free](https://github.com/xtekky/gpt4free#models)

## Database info:
* `bot_users` table for bot users
* `user_questions` table for storing user questions history

## Algorithm:
[Each user question is stored in Database](./database/bot_database.sql). As soon as a new question is asked, [the bot retrieves the previous questions history from the Database](./handlers/user_questions.py?plain=1#L94-L96), [beautifies the user question history into an array](./handlers/user_questions.py?plain=1#L98-L107) and [sends beatified array as an "messages" parament to the GPT4Free Provider](./handlers/user_questions.py?plain=1#L110)

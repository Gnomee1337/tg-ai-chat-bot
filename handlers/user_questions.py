import g4f
import nest_asyncio

import random, string, os
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
import logging
import config
from localization.localization import set_localization
from keyboards import keyboards as nav
from database.database import Database
from bot_init import dp, bot, db

class QuestionStates(StatesGroup):
    question = State()
    
# @dp.message_handler(commands='start')
async def cm_start(message: types.Message, state: FSMContext):
    await message.answer("Welcome")
    ## If user exists
    if(db.user_exists(message.from_user.id)):
        ## Send user to main menu
        user_language = db.get_user_language(message.from_user.id)
        await state.set_state(None)
        await message.answer(set_localization('Привет ',user_language) + str(message.from_user.username), parse_mode="html", reply_markup=nav.mainMenu(user_language))
    else:
    ## If user not exists
        ## Init user to DB
        db.add_user_empty(message.from_user.id, message.from_user.username)
        ## Send user to language panel
        await message.answer('Привет. Выберите язык использования!\nHello. Choose your language!', parse_mode="html", reply_markup=nav.langMenu)
        
#@dp.message_handler(state = '*', commands=['cancel'])
#@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    try:
        user_language = db.get_user_language(message.from_user.id)
    except:
        user_language = "ru"
        pass
    #Allow user to cancel any action
    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    #await message.reply('Отмена.\nCancelled.', reply_markup=types.ReplyKeyboardRemove())
    await message.reply('Отмена.\nCancelled.', reply_markup=nav.mainMenu(user_language))

# Update user language during first registration
@dp.callback_query_handler(text_contains = "lang_", state=None)
async def setLanguage(callback: types.CallbackQuery, state: FSMContext):
    logging.debug("###DEBUG### setLanguage started")
    lang = callback.data[5:]
    db.change_user_language(callback.from_user.id, lang)
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, callback.from_user.username + " " +nav.set_localization("привет, прочитай информацию!", lang), reply_markup=nav.mainMenu(lang))
    logging.debug("###DEBUG### setLanguage finished")

async def beatify_questions_history(questions_history):
    new_questions_history = []
    for question_tup in questions_history:
        new_questions_history += [{"role":"user","content":question_tup[0]}]
    return new_questions_history

@dp.callback_query_handler()
#@dp.callback_query_handler(lambda x: x.data and x.data.startswith("reg "))
async def main_menu(call: types.CallbackQuery, state: FSMContext):
    logging.debug(await state.get_state())
    if call.message:
        user_language = db.get_user_language(call.from_user.id)
        if call.data == 'askquestion':
                await call.message.answer(set_localization("Задайте свой вопрос у бота! (Лимит сообщения 4000 символов)",user_language))
                await QuestionStates.question.set()
                #await clear_chat(call.message.message_id, call.message.chat.id)

async def ask_question(message: types.Message, state: FSMContext):
    user_language = db.get_user_language(message.from_user.id)
    if len(message.text) > 4000:
        await message.answer(set_localization("Извините, но вопрос содержит больше 4000 символов.\nЗадайте вопрос ещё раз!", user_language))
        return
    else:
        #ai_response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.Bing, messages=[{"role":"user","content":"Write simple python on version 3.11 chess game"}])
        #print(ai_response)
        db_user_id = db.get_user_id(message.from_user.id)
        if(db_user_id is None):
            bot.send_message(message.from_user.id, "Задайте вопрос снова!")
            return
        # Get user-questions-history
        user_questions_history = db.get_user_question_history(db_user_id)
        print(user_questions_history)
        
        # Change user-questions-history to correct format
        beatified_questions = await beatify_questions_history(user_questions_history)
        print(beatified_questions)
        
        # Current asked question
        asked_question = [{"role":"user","content":str(message.text)}]
        
        # Questions history + current question from user
        beatified_questions += asked_question
        print(beatified_questions)
        
        try:
            ai_response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, provider=g4f.Provider.ChatgptAi, messages=beatified_questions)
            db.add_user_question(message.from_user.id,message.text)
            print(ai_response)
        except:
            pass
        if ai_response != None:
            await bot.send_message(message.from_user.id, str(ai_response), reply_markup=nav.mainMenu(user_language))
        else:
            await bot.send_message(message.from_user.id, "Error occurred try again!", parse_mode="html", reply_markup=nav.mainMenu(user_language))
        await state.finish()
        
        
def register_handlers_user_questions(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['start'], state=None)
    dp.register_message_handler(cancel_handler, state = '*', commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(ask_question, state=QuestionStates.question)
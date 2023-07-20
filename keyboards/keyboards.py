from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from localization.localization import set_localization

#Language
langRU = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='lang_ru')
langEN = InlineKeyboardButton(text='🇺🇸 English', callback_data='lang_en')

#LanguageMenu
langMenu = InlineKeyboardMarkup(resize_keyboard = True)
langMenu.add(langRU, langEN)

def mainMenu(lang='ru'):
    mainMenu = InlineKeyboardMarkup(resize_keyboard = True)
    
    btnAskQuestion = InlineKeyboardButton(set_localization("Задать вопрос", lang),callback_data='askquestion')
    
    mainMenu.add(btnAskQuestion)

    return mainMenu

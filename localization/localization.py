localization = {
    'en':{
        "Тест" : "Cancel"
    }
}

def set_localization(text, language = 'ru'):
    if language == 'ru':
        return text
    else:
        global localization
        try:
            return localization[language][text]
        except:
            return text
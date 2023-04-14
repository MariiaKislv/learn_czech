import translators as ts

def get_translation_for_word(word_ru):

    return ts.translate_text(word_ru, from_language='ru', translator='baidu')

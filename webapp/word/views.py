from flask import Blueprint, render_template, request
import random

from webapp.word.models import Words

blueprint = Blueprint('word', __name__)

@blueprint.route('/')
def words():
    title = 'Список слов'
    words_list = Words.query.all()
    return render_template('word/words.html', page_title=title, words_list=words_list)
    
@blueprint.route('/learning')
def word():
    title = 'Изучение слова'
    words_list = Words.query.all()
    word_id = request.args.get('w_id')

    if word_id != None:
        word_id = int(word_id)
        current_word = list(filter(lambda word: word.id == word_id, words_list))[0]
    else:
        current_word = random.choice(words_list)
    other_worlds = list(filter(lambda word: word.id != current_word.id, words_list))
    random.shuffle(other_worlds)
    words_for_choose = other_worlds[:3]
    words_for_choose.append(current_word)
    random.shuffle(words_for_choose)
    return render_template('word/word.html', page_title=title, words_for_choose=words_for_choose, current_word=current_word)

@blueprint.route('/result')
def answer():
    result = request.args.get('q')
    answer = request.args.get('answer')
    if answer == result:
        sentense = 'Верно'
    else:
        sentense = 'Ошибка'
    return render_template('word/result.html', sentense=sentense)
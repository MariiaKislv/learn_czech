from datetime import datetime
from flask import Blueprint, render_template, request
import random
from sqlalchemy import func

from webapp.db import db
from webapp.word.models import Word, Answer

blueprint = Blueprint('word', __name__)

@blueprint.route('/')
def words():
    title = 'Список слов'
    words_list = Word.query.all()
    return render_template('word/words.html', page_title=title, words_list=words_list)
    
@blueprint.route('/learning')
def word():
    title = 'Изучение слова'
    words_list = Word.query.all()
    word_id = request.args.get('w_id')
    error_data = db.session.query(Answer.word_id, func.count(Answer.word_id)
                            ).filter(Answer.is_correct_answer == False).group_by(Answer.word_id).all()
    
    if word_id != None:
        word_id = int(word_id)
        current_word = list(filter(lambda word: word.id == word_id, words_list))[0]

    else:
        if len(error_data) != 0:
            random_id = (random.choice(error_data))[0]
            current_word = list(filter(lambda word: word.id == random_id, words_list))[0]
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
    answer_word = request.args.get('answer')
    if answer_word == result:
        sentense = 'Верно'
        new_answer = Answer(word_id=result, is_correct_answer=True, answered_at=datetime.now())
    else:
        sentense = 'Ошибка'
        new_answer = Answer(word_id=result, is_correct_answer=False, answered_at=datetime.now())
    db.session.add(new_answer)
    db.session.commit()

    return render_template('word/result.html', sentense=sentense)
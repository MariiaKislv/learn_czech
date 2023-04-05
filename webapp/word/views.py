from datetime import datetime, timedelta
from flask import Blueprint, redirect, render_template, request, url_for, current_app
from flask_login import  current_user
import random
from sqlalchemy import func, and_

from webapp.db import db
from webapp.word.models import Word, Answer

blueprint = Blueprint('word', __name__, url_prefix='/words')

@blueprint.route('/')
def words():
    title = 'Список слов'
    wrong_words = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == False).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id)
    new_words = Word.query.join(Answer, and_(Word.id == Answer.word_id, Answer.user_id == current_user.id), isouter=True).filter(Answer.word_id.is_(None)).group_by(Word.id).limit(50)
    print(new_words)
    return render_template('word/words.html', page_title=title, wrong_words=wrong_words, new_words=new_words)
    
@blueprint.route('/learning')
def word():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    title = 'Изучение слова'
    word_id = request.args.get('w_id')
    wrong_words = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == False).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id).all()
    print(wrong_words)
    if word_id != None:
        current_word = Word.query.get(word_id)
        if current_word == None:
            return redirect(url_for('word.words'))

    else:
        if random.randint(1, 4) == 1:
            random_id = (random.choice(wrong_words))[0]
            current_word = Word.query.get(random_id)
            current_app.logger.info('Следующее слово из списка для повторения')
        else:  
            current_word = Word.query.order_by(func.random()).limit(1).one()
            current_app.logger.info('Следующее слово является рандомным из всех слов')
    words_for_choose = Word.query.filter(Word.id != current_word.id).order_by(func.random()).limit(3).all()
    words_for_choose.append(current_word)
    random.shuffle(words_for_choose)
    return render_template('word/word.html', page_title=title, words_for_choose=words_for_choose, current_word=current_word)


@blueprint.route('/result')
def answer():

    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    result = request.args.get('q')
    answer_word = request.args.get('answer')
    if answer_word == result:
        sentense = 'Верно'
        new_answer = Answer(word_id=result, is_correct_answer=True, answered_at=datetime.now(), user_id=current_user.id)
    else:
        sentense = 'Ошибка'
        new_answer = Answer(word_id=result, is_correct_answer=False, answered_at=datetime.now(), user_id=current_user.id)
    db.session.add(new_answer)
    db.session.commit()
    return render_template('word/result.html', sentense=sentense)

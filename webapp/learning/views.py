from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import  current_user
import random
from sqlalchemy import func, and_

from webapp.db import db
from webapp.learning.forms import AnswerForm
from webapp.learning.models import Word, Answer

blueprint = Blueprint('learning', __name__, url_prefix='/learning')

@blueprint.route('/')
def words():
    title = 'Список слов'
    # Список слов с ошибками определенного пользователя за посление 30 дней
    wrong_words = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == False).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id)
    #  Список слов, на которые не было ответов определенного аккаунта
    new_words = Word.query.join(Answer, and_(Word.id == Answer.word_id, Answer.user_id == current_user.id), isouter=True).filter(Answer.word_id.is_(None)).group_by(Word.id).limit(50)
    # Список слов, на которые определенный пользователь давал правильные ответы за последние 30 дней
    words_for_inputting = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == True).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id).all()
    print(new_words)
    return render_template('learning/words.html', page_title=title, wrong_words=wrong_words, new_words=new_words, words_for_inputting=words_for_inputting)
    
@blueprint.route('/test_cz')
def test_cz():
    """ Перевод с русского на чешский """

    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    title = 'Выберите верный перевод слова'
    word_id = request.args.get('w_id')
    wrong_words = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == False).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id).all()
    print(wrong_words)
    if word_id != None:
        current_word = Word.query.get(word_id)
        if current_word == None:
            return redirect(url_for('learning.words'))

    else:
        if random.randint(1, 4) == 1:
            current_word = random.choice(wrong_words)
            current_app.logger.info('Следующее слово из списка для повторения')
        else:  
            current_word = Word.query.order_by(func.random()).limit(1).one()
            current_app.logger.info('Следующее слово является рандомным из всех слов')
    words_for_choose = Word.query.filter(Word.id != current_word.id).order_by(func.random()).limit(3).all()
    words_for_choose.append(current_word)
    random.shuffle(words_for_choose)
    return render_template('learning/test_cz.html', page_title=title, words_for_choose=words_for_choose, current_word=current_word)

@blueprint.route('/test_ru')
def test_ru():
    """ Перевод с чешского на русский """

    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    title = 'Выберите верный перевод слова'
    word_id = request.args.get('w_id')
    wrong_words = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == False).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id).all()
    print(wrong_words)
    if word_id != None:
        current_word = Word.query.get(word_id)
        if current_word == None:
            return redirect(url_for('learing.words'))

    else:
        if random.randint(1, 4) == 1:
            current_word = random.choice(wrong_words)
            current_app.logger.info('Следующее слово из списка для повторения')
        else:  
            current_word = Word.query.order_by(func.random()).limit(1).one()
            current_app.logger.info('Следующее слово является рандомным из всех слов')
    words_for_choose = Word.query.filter(Word.id != current_word.id).order_by(func.random()).limit(3).all()
    words_for_choose.append(current_word)
    random.shuffle(words_for_choose)
    return render_template('learning/test_ru.html', page_title=title, words_for_choose=words_for_choose, current_word=current_word)

@blueprint.route('/inputting')
def inputting_word():
    """ Правописание слова на чешском """

    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    title = 'Введите слово'
    word_id = request.args.get('w_id')
    words_for_inputting = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == True).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id).all()
    
    if word_id != None:
        current_word = Word.query.get(word_id)
        if current_word == None:
            return redirect(url_for('learing.words'))
    else:
        current_word = random.choice(words_for_inputting)
        word_id = current_word.id

    form = AnswerForm()
    form.word_id.data = word_id
    return render_template('learning/inputting.html', page_title=title, current_word=current_word, form=form)

@blueprint.route('/process-answer', methods=['POST'])
def process_answer():
    question_type = 'inputting'
    form = AnswerForm()
    
    if form.validate_on_submit():
            new_word = form.answer.data
            word_id = int(form.word_id.data)
            if new_word == Word.query.get(word_id).word_cz:
                sentense = 'Верно'
                new_answer = Answer(word_id=word_id, is_correct_answer=True, answered_at=datetime.now(), user_id=current_user.id, question_type=question_type)
            else:
                sentense = 'Ошибка'
                new_answer = Answer(word_id=word_id, is_correct_answer=False, answered_at=datetime.now(), user_id=current_user.id, question_type=question_type)
            db.session.add(new_answer)
            db.session.commit()
            return render_template('learning/result.html', sentense=sentense, question_type=question_type)
    else:
        for field, errors in form.errors.items():
             for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
					getattr(form, field).label.text, 
					error
				))
        return redirect(url_for('learning.words')) 

@blueprint.route('/result')
def answer():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))
    result = request.args.get('id')
    answer_word = request.args.get('answer')
    question_type = request.args.get('qt')
    if answer_word == result:
        sentense = 'Верно'
        new_answer = Answer(word_id=result, is_correct_answer=True, answered_at=datetime.now(), user_id=current_user.id, question_type=question_type)
    else:
        sentense = 'Ошибка'
        new_answer = Answer(word_id=result, is_correct_answer=False, answered_at=datetime.now(), user_id=current_user.id, question_type=question_type)
    db.session.add(new_answer)
    db.session.commit()
    return render_template('learning/result.html', sentense=sentense, question_type=question_type)

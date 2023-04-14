from datetime import datetime, timedelta
import unicodedata
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import  current_user, login_required
import random
from sqlalchemy import func

from webapp.db import db
from webapp.learning.forms import AnswerForm
from webapp.learning.models import Word, Answer
from webapp.lesson.photo import get_photo
from webapp.lesson.translate_word import get_translation_for_word

blueprint = Blueprint('learning', __name__, url_prefix='/learning')

@login_required
@blueprint.route('/')
def words():
    title = 'Обучение'
    return render_template('learning/words.html', page_title=title)

@blueprint.route('/test')
def test():
    """ Режим теста """

    question_type = request.args.get('qt')
    title = 'Выберите верный перевод слова'
    # Слова, в которых пользователь допустил ошибку за последние 30 дней
    wrong_words = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == False).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id).all()
    print(wrong_words)
    
    if wrong_words is None:
        flash('Слов для повторения нет!')
        redirect(url_for('learning.words'))

    current_word = random.choice(wrong_words)

    words_for_choose = Word.query.filter(Word.id != current_word.id).order_by(func.random()).limit(3).all()
    words_for_choose.append(current_word)
    random.shuffle(words_for_choose)
    print('word ' + current_word.word_ru)
    eng_translation = get_translation_for_word(current_word.word_ru)
    print('translation ' + eng_translation)
    image_url = get_photo(eng_translation)
    print('url ' + image_url)
    return render_template('learning/test.html', page_title=title, image_url=image_url, words_for_choose=words_for_choose, current_word=current_word, question_type=question_type)

@blueprint.route('/inputting')
def inputting_word():
    """ Режим ввода """

    title = 'Введите слово'
    # Слова, в которых пользователь допустил ошибку за последние 30 дней
    words_for_inputting = db.session.query(Word).join(Answer, Word.id == Answer.word_id
                            ).filter(Answer.is_correct_answer == False).filter(datetime.now() - timedelta(days=30) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id).all()
    
    if words_for_inputting is None:
        flash('Слов для повторения нет!')
        redirect(url_for('learning.words'))

    current_word = random.choice(words_for_inputting)
    word_id = current_word.id
    print('word ' + current_word.word_ru)
    eng_translation = get_translation_for_word(current_word.word_ru)
    print('translation ' + eng_translation)
    image_url = get_photo(eng_translation)
    print('url ' + image_url)
    form = AnswerForm()
    form.word_id.data = word_id
    return render_template('learning/inputting.html', page_title=title, image_url=image_url, current_word=current_word, form=form)

@blueprint.route('/process-answer', methods=['POST'])
def process_answer():
    question_type = 'inputting'
    form = AnswerForm()
    
    if form.validate_on_submit():
            new_word = form.answer.data
            word_id = int(form.word_id.data)
            is_correct = unicodedata.normalize('NFC', new_word.lower()) == unicodedata.normalize('NFC', Word.query.get(word_id).word_cz)
            new_answer = Answer(word_id=word_id, is_correct_answer=is_correct, answered_at=datetime.now(), user_id=current_user.id, question_type=question_type)
            db.session.add(new_answer)
            db.session.commit()
            if is_correct:
                flash('Верно')
            else:
                flash (f'Ошибка, правильный ответ: {Word.query.get(word_id).word_cz}') 
            return redirect(url_for('learning.inputting_word'))
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

    result = request.args.get('id')
    answer_word = request.args.get('answer')
    question_type = request.args.get('qt')
    is_correct = answer_word == result
    new_answer = Answer(word_id=result, is_correct_answer=is_correct, answered_at=datetime.now(), user_id=current_user.id, question_type=question_type)
    db.session.add(new_answer)
    db.session.commit()
    if is_correct:
        flash('Верно')
    else:
        word = Word.query.get(result)
        flash (f'Ошибка, правильный ответ: {word.word_cz if question_type == "test_cz" else word.word_ru}') 
    return redirect(url_for('learning.test', question_type=question_type))
from datetime import datetime, timedelta
import unicodedata
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import  current_user, login_required
import random
from sqlalchemy import func, and_

from webapp.db import db
from webapp.learning.forms import AnswerForm
from webapp.learning.models import Word, Answer
from webapp.lesson.models import LessonWord
from webapp.lesson.photo import get_photo
from webapp.lesson.translate_word import get_translation_for_word

blueprint = Blueprint('lesson', __name__, url_prefix='/lesson')
@login_required
@blueprint.route('/start_new_words')
def lesson_start_new_words():

    new_words = Word.query.join(LessonWord, and_(Word.id == LessonWord.word_id, LessonWord.user_id == current_user.id), isouter=True).filter(LessonWord.word_id.is_(None)).limit(10)
    words_for_lesson = []
    for word in new_words:
        words_for_lesson.append({'word_id': word.id, 'user_id': current_user.id, 'current_step': 1, 'updated_at': datetime.now()})
    db.session.bulk_insert_mappings(LessonWord, words_for_lesson)
    db.session.commit()

    return redirect(url_for('lesson.lesson'))

@blueprint.route('/start_repeating')
def lesson_start_repeating():

    new_words = Word.query.join(LessonWord, Word.id == LessonWord.word_id).join(Answer, Word.id == Answer.word_id).filter(Answer.is_correct_answer == False
                            ).filter(datetime.now() - timedelta(days = 5) < Answer.answered_at).filter(Answer.user_id == current_user.id).group_by(Answer.word_id).order_by(func.random()).limit(10)
    words_for_lesson = []
    for word in new_words:
        words_for_lesson.append({'word_id': word.id, 'user_id': current_user.id, 'current_step': 1, 'updated_at': datetime.now()})
    db.session.bulk_insert_mappings(LessonWord, words_for_lesson)
    db.session.commit()

    return redirect(url_for('lesson.lesson'))
    
@blueprint.route('/')
def lesson():
    
    title = 'Выберите верный перевод слова'

    record = db.session.query(Word, LessonWord.current_step).join(LessonWord, Word.id == LessonWord.word_id).filter(LessonWord.user_id == current_user.id
                                                ).filter(LessonWord.current_step < 4).order_by(LessonWord.current_step, func.random()).first()
    
    print(record)
    if record == None:
        flash('Урок закончен')
        return redirect(url_for('learning.words'))
    
    current_word = record.Word

    print('word ' + current_word.word_ru)
    eng_translation = get_translation_for_word(current_word.word_ru)
    print('translation ' + eng_translation)
    image_url = get_photo(eng_translation)
    print('url ' + image_url)

    if record.current_step == 1 or record.current_step == 2:
        words_for_choose = Word.query.filter(Word.id != record.Word.id).order_by(func.random()).limit(3).all()
        words_for_choose.append(record.Word)
        random.shuffle(words_for_choose)

        if record.current_step == 1:
            return render_template('lesson/test_cz.html', page_title=title, image_url=image_url, words_for_choose=words_for_choose, current_word=current_word)
        
        if record.current_step == 2:
            return render_template('lesson/test_ru.html', page_title=title, image_url=image_url, words_for_choose=words_for_choose, current_word=current_word)
        
    if record.current_step == 3:
        form = AnswerForm()
        form.word_id.data = record.Word.id
        return render_template('lesson/inputting.html', current_word=current_word, image_url=image_url, record=record, form=form)

@blueprint.route('/check_choose')
def check_choose():
    result = request.args.get('id')
    answer_word = request.args.get('answer')
    question_type = request.args.get('qt')
    is_correct = answer_word == result
    new_answer = Answer(word_id=result, is_correct_answer=is_correct, answered_at=datetime.now(), user_id=current_user.id, question_type=question_type)
    db.session.add(new_answer)
    db.session.commit()
    if is_correct:
        lesson_word = LessonWord.query.filter(LessonWord.word_id == result).filter(LessonWord.current_step < 3).first()
        lesson_word.current_step += 1
        db.session.commit()
        current_app.logger.info('Верно. new current step ' + str(lesson_word.current_step))
        flash('Верно')
    else:
        current_app.logger.info('Ошибка.')
        flash('Ошибка')
    return redirect(url_for('lesson.lesson'))

@blueprint.route('/check-inputting', methods=['POST'])
def check_inputting():
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
                lesson_word = LessonWord.query.filter(LessonWord.word_id == word_id).filter(LessonWord.current_step == 3).first()
                lesson_word.current_step += 1
                db.session.commit()
                flash('Верно')
            else:
                flash('Ошибка')
            return redirect(url_for('lesson.lesson'))
    else:
        for field, errors in form.errors.items():
             for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
					getattr(form, field).label.text, 
					error
				))
        return redirect(url_for('learning.words')) 
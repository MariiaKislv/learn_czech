from flask import Blueprint, flash, redirect, render_template, url_for

from webapp.admin.forms import WordForm
from webapp.db import db
from webapp.learning.models import Word
from webapp.user.decorators import admin_required


blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
@admin_required
def admin_index():
	title = 'Панель управления'
	form = WordForm()
	return render_template('admin/index.html', page_title=title, form=form)

@blueprint.route('/process-add', methods=['POST'])
def process_add():
	form = WordForm()
    
	if form.validate_on_submit():
		new_word = Word(word_ru=form.word_ru.data, word_cz=form.word_cz.data, picture='', description='')
		db.session.add(new_word)
		db.session.commit()
		flash('Слово добавлено')
		return redirect(url_for('admin.admin_index'))
	else:
		for field, errors in form.errors.items():
			for error in errors:
				flash('Ошибка в поле "{}": - {}'.format(
					getattr(form, field).label.text, 
					error
				))
		return redirect(url_for('user.register'))
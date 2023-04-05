from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import  current_user, login_required, login_user, logout_user

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp import db

blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
	if current_user.is_authenticated:
		return redirect(url_for('word.words'))
	title = 'Авторизация'
	login_form = LoginForm()
	return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter(User.username == form.username.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, remember=form.remember_me.data)
			flash('Вы вошли на сайт')
			return redirect(url_for('word.words'))
	flash('Неправильное имя пользователя или пароль')
	return redirect(url_for('user.login'))

@blueprint.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('start'))

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = "Регистрация"
    form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
	form = RegistrationForm()
    
	if form.validate_on_submit():
		new_user = User(username=form.username.data, email=form.email.data, role='user')
		new_user.set_password(form.password.data)
		db.session.add(new_user)
		db.session.commit()
		flash('Вы успешно зарегистрировались!')
		return redirect(url_for('user.login'))
	else:
		for field, errors in form.errors.items():
			for error in errors:
				flash('Ошибка в поле "{}": - {}'.format(
					getattr(form, field).label.text, 
					error
				))
		return redirect(url_for('user.register'))
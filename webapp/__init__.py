from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from webapp.db import db
from webapp.user.models import User
from webapp.admin.views import blueprint as admin_blueprint
from webapp.user.views import blueprint as user_blueprint
from webapp.learning.views import blueprint as learning_blueprint
from webapp.lesson.views import blueprint as lesson_blueprint

def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')
	toolbar = DebugToolbarExtension(app)
	db.init_app(app)
	migrate = Migrate(app, db, render_as_batch=True)
	csrf = CSRFProtect(app)

	login_manager = LoginManager()
	login_manager.init_app(app)
	login_manager.login_view = 'user.login'

	app.register_blueprint(admin_blueprint)
	app.register_blueprint(learning_blueprint)
	app.register_blueprint(lesson_blueprint)
	app.register_blueprint(user_blueprint)
	

	@app.route('/')
	def start():
		title = 'Изучение чешского языка'
		return render_template('index.html', page_title=title)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(user_id)

	return app
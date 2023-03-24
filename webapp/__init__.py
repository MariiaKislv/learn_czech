from flask import Flask

from webapp.db import db
from webapp.word.views import blueprint as word_blueprint

def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')
	db.init_app(app)

	app.register_blueprint(word_blueprint)

	return app
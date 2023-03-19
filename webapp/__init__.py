from flask import Flask, render_template

from webapp.model import db, Words


def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')
	db.init_app(app)

	@app.route('/')
	def index():
		title = 'Список слов'
		words_list = Words.query.all()
		return render_template('index.html', page_title=title, words_list=words_list)

	return app
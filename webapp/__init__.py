from flask import Flask, render_template
import random

from webapp.model import db, Words


def create_app():
	app = Flask(__name__)
	app.config.from_pyfile('config.py')
	db.init_app(app)

	@app.route('/')
	def words():
		title = 'Список слов'
		words_list = Words.query.all()
		return render_template('words.html', page_title=title, words_list=words_list)
	
	@app.route('/learning')
	def word():
		title = 'Изучение слова'
		words_list = Words.query.all()
		current_word = random.choice(words_list)
		other_worlds = list(filter(lambda word: word.id != current_word.id, words_list))
		random.shuffle(other_worlds)
		words_for_choose = other_worlds[:3]
		words_for_choose.append(current_word)
		random.shuffle(words_for_choose)
		return render_template('word.html', page_title=title, words_for_choose=words_for_choose, current_word=current_word)

	return app
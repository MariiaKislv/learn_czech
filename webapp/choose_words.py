from flask import Flask
from model import db, Words

import random

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    return app

def choose_words():
    words_for_choose = []
    words_czech = Words.query.all()
    for word in range(3):
        words_for_choose.append(random.choice(words_czech.word_cz))
    print(words_for_choose)
    

create_app()
choose_words()
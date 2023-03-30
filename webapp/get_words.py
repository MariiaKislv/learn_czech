import csv

from webapp.db import db
from webapp.word.models import Word

def get_word():
    with open('words.csv', 'r', encoding='utf-8') as f:
        fields = ['word_ru', 'word_cz']
        reader = csv.DictReader(f, fields, delimiter=',')
        words_data = []
        for row in reader:
            # print(row)
            save_word(row['word_ru'], row['word_cz'])
       

def save_word(word_ru, word_cz):
	word_exists = Word.query.filter(Word.word_ru == word_ru).count()
	print(word_exists)
	if not word_exists:
		new_word = Word(word_ru=word_ru, word_cz=word_cz, picture='', description='')
		db.session.add(new_word)
		db.session.commit()
                

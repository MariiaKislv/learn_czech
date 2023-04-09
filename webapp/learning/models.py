from webapp.db import db
from webapp.user.models import User

class Word(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True)
    word_ru = db.Column(db.String, nullable=False)
    word_cz = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    def __repr__(self):
        return '<Word {} {}>'.format(self.word_ru, self.word_cz)
    
class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey(Word.id), index=True, nullable=False)
    is_correct_answer = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True, nullable=False)
    question_type = db.Column(db.String, nullable=False)
      
    def __repr__(self):
        return '<Answer {} {}>'.format(self.word_id, self.is_correct_answer)

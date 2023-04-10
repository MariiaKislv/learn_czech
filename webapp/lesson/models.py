from webapp.db import db
from webapp.user.models import User
from webapp.learning.models import Word

class LessonWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey(Word.id), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True, nullable=False)
    current_step = db.Column(db.Integer, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

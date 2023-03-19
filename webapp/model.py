from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Words(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_ru = db.Column(db.String, nullable=False)
    word_cz = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    description = db.Column(db.String)

    def __repr__(self):
            return '<Words {} {}>'.format(self.word_ru, self.word_cz)

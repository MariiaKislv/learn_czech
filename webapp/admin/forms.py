from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class WordForm(FlaskForm):
    word_ru = StringField('Слово на русском', validators=[DataRequired()], render_kw={"class": "form-control"})
    word_cz = StringField('Слово на чешском', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
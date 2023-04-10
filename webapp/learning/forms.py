from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField

class AnswerForm(FlaskForm):
    answer = StringField('Введите ответ', render_kw={"class": "form-control mx-3"})
    word_id = HiddenField('Введите ответ', render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})
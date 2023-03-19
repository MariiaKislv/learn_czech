from webapp import create_app
from webapp.get_words import get_word

app = create_app()
with app.app_context():
    get_word()
from flask import Flask
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SECRET_KEY'] = 'my_super_secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "База данных создана! Теперь можно делать регистрацию."

if __name__ == '__main__':
    app.run(debug=True)
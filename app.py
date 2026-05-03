from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, News
from forms import RegisterForm, LoginForm, NewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_lyceum_secret_key_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    db_news = News.query.order_by(News.id.desc()).all()

    # Если база пуста, показываем демо-контент
    if not db_news:
        latest_news = [
            {"title": "Эволюция AI в 2026 году", "content": "Нейросети теперь интегрированы в каждый браузер.",
             "author": {"username": "TechDaily"}}
        ]
        yearly_news = [
            {"title": "Итоги года: Прорыв в квантах",
             "content": "Ученые достигли стабильности кубитов при комнатной температуре.",
             "author": {"username": "ScienceHub"}},
            {"title": "Глобальное потепление 2026", "content": "Мировые лидеры подписали новое соглашение по экологии.",
             "author": {"username": "EcoWatch"}},
            {"title": "Марс: Первый жилой модуль", "content": "SpaceX успешно доставила оборудование для первой базы.",
             "author": {"username": "MarsToday"}}
        ]
        return render_template('index.html', latest_news=latest_news, yearly_news=yearly_news, is_demo=True)

    # Распределяем: первые 3 — свежие, следующие 3 — важные за год
    latest = db_news[:3]
    yearly = db_news[3:6]
    return render_template('index.html', latest_news=latest, yearly_news=yearly, is_demo=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Этот email уже занят', 'danger')
            return render_template('register.html', form=form)
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_hash == form.password.data:
            login_user(user)
            flash('С возвращением!', 'success')
            return redirect(url_for('index'))
        flash('Неверный email или пароль', 'danger')
    return render_template('login.html', form=form)


@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        news = News(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(news)
        db.session.commit()
        flash('Опубликовано!', 'success')
        return redirect(url_for('index'))
    return render_template('add_news.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
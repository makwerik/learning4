from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db = SQLAlchemy(app)


class Posts(db.Model):
    """
    Класс для ДБ с постами.
    Плюс использован магический метод, который будет выбирать нам определнну запись
    и выдавать её id
    """
    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    announcement = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Posts %r>" % self.id


@app.route('/')
def home():
    """
    Функция главной страницы с оторажением данных из БД
    """
    show_posts = Posts.query.order_by(Posts.date).all()
    return render_template('home.html', show_posts=show_posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create-posts', methods=['POST', 'GET'])
def create_post():
    """
    Функция добавляющая посты в БД
    """
    if request.method == 'POST':
        heading = request.form['heading']
        announcement = request.form['announcement']
        text = request.form['text']
        posts = Posts(heading=heading, announcement=announcement, text=text)
        try:
            db.session.add(posts)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка добавления статьи'
    else:
        return render_template('create-post.html')


@app.route('/<int:id>')
def read_post(id):
    """
    Функция для отображения полной информации о статье
    """
    show_post = Posts.query.get(id)
    return render_template('/<int:id>.html', show_post=show_post)


@app.route('/<int:id>/delete')
def delete_post(id):
    """
    Удаление статьи из БД
    """
    delete_p = Posts.query.get_or_404(id)
    try:
        db.session.delete(delete_p)
        db.session.commit()
        return redirect('/')
    except:
        return "Ошибка удаления записи"


@app.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    """
    Редактирование статьи в БД
    """
    update_p = Posts.query.get(id)
    if request.method == 'POST':
        update_p.heading = request.form['heading']
        update_p.announcement = request.form['announcement']
        update_p.text = request.form['text']
        try:
            db.session.commit()
            return redirect(f'/{id}')
        except:
            return "Ошибка обновления статьи"
    else:
        return render_template('update-post.html', update_p=update_p)


if __name__ == '__main__':
    app.run(debug=True)

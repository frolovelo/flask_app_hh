from datetime import datetime

from flask_login import UserMixin
from sweater import db, manager_login
import json
from sqlalchemy import TypeDecorator, Text


class JsonType(TypeDecorator):
    """Собственный тип данных SQLAlchemy для хранения JSON в базе данных."""
    impl = Text

    def process_bind_param(self, value, dialect):
        """Преобразует значение Python в формат JSON перед сохранением в базе данных."""
        if value is not None:
            value = json.dumps(value, ensure_ascii=False)
        return value

    def process_result_value(self, value, dialect):
        """Преобразует JSON-представление значения из базы данных обратно в Python-объект."""
        if value is not None:
            value = json.loads(value)
        return value


class Vacancy(db.Model):
    """БД Вакансий"""
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(300), nullable=False)
    exclude = db.Column(db.String(300))
    region = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    vacancy_json = db.Column(JsonType)
    likes = db.Column(db.Integer, default=0)
    date_create = db.Column(db.DateTime, default=datetime.now)


class User(db.Model, UserMixin):
    """БД Пользователей"""
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(30), nullable=False, unique=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    def has_liked_post(self, post_id: int):
        """
        Проверяет, поставил ли пользователь "лайк" определенной записи.

        :param post_id: Идентификатор записи вакансии.

        :return: True, если пользователь поставил "лайк" этой записи, в противном случае - False.
        :rtype: bool
        """
        return Like.query.filter_by(user_id=self.id, post_id=post_id).first() is not None


class Like(db.Model):
    """БД Вакансий"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('likes', lazy=True))
    post = db.relationship('Vacancy', backref=db.backref('liked_by', lazy=True))


@manager_login.user_loader
def load_user(user_id: int):
    """
    Загружает пользователя из базы данных на основе id.

    :param user_id: id пользователя, который требуется загрузить.

    :return: Объект пользователя - если найден, иначе None.
    :rtype: User or None
    """
    return User.query.get(user_id)

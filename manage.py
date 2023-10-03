"""Миграция БД"""
from flask_migrate import Migrate
from flask_script import Manager
# Migration Alembic want this row :)
# Version Flask-Migration downgrade if you have exception!!!
from sweater.models import User, Vacancy, Like
from sweater import app, db

migrate = Migrate(app, db)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()

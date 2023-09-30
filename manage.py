"""Миграция БД"""
from sweater import app, db
# Migration Alembic want this row :)
# Version Flask-Migration dawngrade!!!
from sweater.models import User, Vacancy, Like
from flask_migrate import Migrate
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
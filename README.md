# Flask_app_hh

**Flask_app_hh** - *веб-приложение*, помогающее найти необходимые *ключевые навыки*
для определенной вакансии.

Вы можете взглянуть здесь: <a href="https://frolofelo.ru/">frolofelo.ru</a> 
(Хостится на домашнем сервере Ubuntu + nginx + gunicorn, доступен с 11:00 до 23:00)

![Static Badge](https://img.shields.io/badge/python-3.11-blue)
![Static Badge](https://img.shields.io/badge/Flask-2.3.2-blue)
![Static Badge](https://img.shields.io/badge/PostgreSQL-blue)
![Static Badge](https://img.shields.io/badge/SQLAlchemy-2.0.2-red)
![Static Badge](https://img.shields.io/badge/Jinja2-3.1.2-red)
![Static Badge](https://img.shields.io/badge/pylint_score-9%2C5-green)

# Основные разделы
### 1. Поиск навыков
Например, мы хотим найти, какие навыки нужны для ***Python-разработчика***.

И мы точно знаем, что не хотим заниматься определенным родом деятельности - 
для этого можно исключить следующие слова: ***1С, Аналитик, Преподаватель***.

От объёма выборки зависит кол-во обработанных вакансий: от 24 до 120 шт.

<p align="center">
<img style="width: 400px" src="https://i.postimg.cc/1zZSG5d3/photo-2023-09-30-23-16-52.jpg" alt="Ключевые навыки" border="0">
</p>

### 2. Результаты поиска
Небольшая диаграмма наглядно даёт понять топ-7 ключевых навыков - как минимум, их лучше указать в резюме, 
но лучше всего - знать!

Также выдаётся таблица топ-15 навыков для более полной картины.
<details><summary>Тех. часть</summary>

   1. Таблица создана при помощи jinja2.
   2. Диаграмма создана при помощи matplotlib.
   3. Поля "Вакансии" и "Исключения" приводятся к единому формату:
      * Сортируются по алфавиту
      * Смена регистра
      * Избавление от лишних пробелов
   4. Если такой же запрос был менее месяца назад - результат будет взят из бд. 

</details>
<p align="center">
<img style="width: 600px" src="https://i.postimg.cc/Gt9PXRf4/photo-2023-09-30-23-44-43.jpg" alt="Ключевые навыки" border="0">
</p>

### 3. Все записи вакансий 
Во вкладке "Все записи" - мы можем увидеть все поиски по ключевым навыкам не только с вашего аккаунта.

<details><summary>Тех. часть</summary>

   1. Реализована пагинация для постраничной выдачи записей.
   2. Система лайков - используется для ранжирования записей в выдаче.
   3. Поисковая строка - при желании найти похожие записи.
   4. При нажатии на кнопку "Читать далее" - открывается полное представление записи. 

</details>
<p align="center">
<img style="width: 600px" src="https://i.postimg.cc/Nf1JN6Fc/2023-10-01-193534.png" alt="Ключевые навыки" border="0">
</p>


## Структура проекта
* [wsgi](wsgi.py) - точка входа
* [manage](manage.py) - миграция бд на сервер
* [requirements](requirements.txt) - зависимости
* [sweater](sweater) - компоненты веб-сервиса
  * \_\_init\_\_ - конфигурация SQLAlchemy 
  * [routes](sweater/routes.py) - маршруты
  * [bd_usage](sweater/bd_usage.py) - взаимодействие с PostgreSQL
  * [hh](sweater/hh.py) - взаимодействие с api.hh.ru
  * [models](sweater/models.py) - модели/таблицы бд
  * [templates](sweater/templates) - html страницы
  * [static](sweater/static) 
    * [css](sweater/static/css) - cтили CSS
    * [img](sweater/static/img) - изображения
  

## Схема базы данных
<p align="center">
<img style="width: 600px" src="https://i.postimg.cc/3NPf0Wd3/2023-10-01-193046.png" alt="Ключевые навыки" border="0">
</p>

## TO-DO

- [x] MVP 
- [ ] Использование   ```asyncio``` и ```aiohttp``` при запросах к API
- [ ] Смена пароля и никнейма в лк
- [ ] Подключение аутентификации по email
- [ ] Переезд на django/fastAPI
- [ ] Расширение функционала
- [ ] Использование cookie
- [ ] Защита от sql-инъекций 



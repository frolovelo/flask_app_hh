"""Маршруты приложения"""
from flask import request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sweater import app, db
from sweater.models import User, Vacancy, Like
from sweater.hh import get_static, get_areas, get_image
from sweater.bd_usage import create_vacancy, check_old_vacancy, clear_format


@app.route("/index")
@app.route("/")
def index():
    """Главная страница"""
    return render_template("index.html")


# @app.route("/create", methods=['POST', 'GET'])
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         text = request.form['text']
#
#         post = Post(text=text, title=title)
#
#         try:
#             db.session.add(post)
#             db.session.commit()
#             return redirect('/posts')
#         except Exception as ex:
#             print(ex)
#             return 'Произошла ошибка c бд'
#
#     else:
#         return render_template("create.html")


@app.route('/posts')
@login_required
def posts():
    """Пагинация всех записей вакансий"""
    page = request.args.get('page', 1, type=int)  # Получение номера страницы из URL, по умолчанию 1
    per_page = 5  # Количество результатов на странице

    user = current_user
    print(f'{request.args=}')
    show_my_vacancies = request.args.get('my_vacancies', type=bool)

    search_query = request.args.get('search_query', '')

    if show_my_vacancies:
        # Если параметр true, показать только вакансии, созданные текущим пользователем
        title = 'Мои записи'
        base_query = Vacancy.query.filter_by(author_id=user.id)
    else:
        title = 'Все записи'
        base_query = Vacancy.query

    # Выполните поиск вакансий по названию с учетом регистра
    if search_query:
        base_query = base_query.filter(Vacancy.name.ilike(f'%{search_query}%'))

    # Добавляем параметр my_vacancies к URL вручную для ссылок на предыдущую и следующую страницу
    url_params = {'page': page}
    if show_my_vacancies:
        url_params['my_vacancies'] = True
    if search_query:
        url_params['search_query'] = search_query
    vacancy_pagination = (
        base_query.order_by(Vacancy.likes.desc())
        .paginate(page=page, per_page=per_page)
    )

    # Список, чтобы хранить информацию о том, лайкал ли пользователь каждый пост на текущей странице
    liked_posts = [user.has_liked_post(vacancy.id) for vacancy in vacancy_pagination.items]
    return render_template("posts.html",
                           vacancy_pagination=vacancy_pagination,
                           liked_posts=liked_posts,
                           page_title=title,
                           User=User,
                           **url_params)


@app.route('/post/<int:post_id>')
@login_required
def show_post(post_id):
    """Показывает отдельную запись вакансии"""
    vacancy = Vacancy.query.filter_by(id=post_id).first()
    if not vacancy:
        return render_template('error.html'), 404
    image = get_image(vacancy.vacancy_json)
    return render_template('statistic.html',
                           image=image,
                           vacancy=vacancy,
                           col=vacancy.quantity // 24 * 24)


@app.route('/like_post/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    """'Лайк' от пользователя"""
    vacancy = Vacancy.query.get_or_404(post_id)
    user = current_user

    # Проверяем, был ли лайк от данного пользователя уже учтен
    existing_like = Like.query.filter_by(user=user, post=vacancy).first()

    if existing_like:
        # Если лайк уже был поставлен данным пользователем, удаляем его
        db.session.delete(existing_like)
        vacancy.likes -= 1  # Уменьшаем количество лайков
        liked = False
    else:
        # Если лайка от данного пользователя для данного поста не существует, добавляем его
        like = Like(user=user, post=vacancy)
        db.session.add(like)
        vacancy.likes += 1  # Увеличиваем количество лайков
        liked = True

    db.session.commit()

    return jsonify({'likes': vacancy.likes, 'liked': liked})


#
#
# @app.route('/delete-post/<int:post_id>')
# @login_required
# def delete_post(post_id):
#     all_post = Post.query.all()
#     for post in all_post:
#         if post.id == post_id:
#             db.session.delete(post)
#             db.session.commit()
#             flash(f'Удалена запись {post.id}: {post.title}')
#             return redirect(url_for('posts'))


@app.route('/login', methods=["GET", "POST"])
def login_page():
    """Вход пользователя в аккаунт"""
    login = request.form.get('login')
    password = request.form.get('password')
    if request.method == "POST":
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('Пароль неверный/Аккаунт не найден')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация пользователя"""
    nickname = request.form.get('nickname')
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if password != password2:
            flash('Пароли не совпадают!')
        elif User.query.filter_by(login=login).first():
            flash('Логин занят!')
        elif User.query.filter_by(nickname=nickname).first():
            flash('Никнейм занят!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(nickname=nickname, login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            flash('Регистрация успешна! Войдите в аккаунт:')
            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/check_nickname_availability', methods=['POST'])
def check_nickname_availability():
    """Проверяет доступность никнейм при регистрации"""
    nickname = request.form.get('nickname')
    user = User.query.filter_by(nickname=nickname).first()
    if user:
        return jsonify({'available': False})
    return jsonify({'available': True})


@app.route('/check_login_availability', methods=['POST'])
def check_login_availability():
    """Проверяет доступность логина при регистрации"""
    login = request.form.get('login')
    user = User.query.filter_by(login=login).first()
    if user:
        return jsonify({'available': False})
    return jsonify({'available': True})


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """Выйти из аккаунта"""
    logout_user()
    flash("Вы вышли из аккаунта!")
    return redirect(url_for('index'))


@app.route('/account/')
@login_required
def account():
    """Личный кабинет"""
    return render_template('account.html')


@app.after_request
def redirect_to_signin(response):
    """Переадресация, если пользователь не вошёл"""
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


@app.route('/search-skills', methods=["POST", "GET"])
@login_required
def search_skills():
    """Поиск навыков по вакансиям"""
    if request.method == "GET":
        area = get_areas()
        return render_template('search-skills.html', area=area)

    name_vacancy = request.form.get('name_vacancy')
    temp = int(request.form.get('temp'))
    area = request.form.get('area')
    name_exclude = request.form.get('name_exclude')
    if any(i in ";!./?" for i in name_vacancy) or any(i in ";!./?" for i in name_exclude):
        flash('Используйте только запятые при разделении вакансий!')
        area = get_areas()
        return render_template('search-skills.html', area=area)

    area = area.split()
    name_vacancy, name_exclude = clear_format(name_vacancy, name_exclude)
    old_vacancy = check_old_vacancy(name_vacancy, area, temp * 24, name_exclude)
    if old_vacancy:
        image = get_image(old_vacancy.vacancy_json)
        return render_template('statistic.html',
                               image=image,
                               vacancy=old_vacancy,
                               col=old_vacancy.quantity // 24 * 24)

    vacancy_json, area, count, name_exclude = get_static(name_vacancy,
                                                         pages=temp,
                                                         region=area,
                                                         name_exclude=name_exclude)
    if count < 0:
        flash('Произошла ошибка при запросе, попробуйте позже!')
        area = get_areas()
        return render_template('search-skills.html', area=area)
    if len(vacancy_json) == 0:
        flash('Вакансий по запросу не найдено...')
        area = get_areas()
        return render_template('search-skills.html', area=area)
    vacancy = create_vacancy(current_user.id, name_vacancy, name_exclude, area, count, vacancy_json)
    image = get_image(vacancy.vacancy_json)
    return render_template('statistic.html',
                           image=image,
                           vacancy=vacancy,
                           col=vacancy.quantity // 24 * 24)


@app.errorhandler(404)
def page_not_found():
    """404"""
    return render_template('error.html'), 404


@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """Удаляет аккаунт и его записи из БД"""
    user_to_del = User.query.filter_by(id=current_user.id).first()

    if user_to_del:
        # Удаление всех лайков, связанных с пользователем (ON CASCADE было бы написать в бд проще)
        Like.query.filter_by(user_id=current_user.id).delete()
        Vacancy.query.filter_by(author_id=current_user.id).delete()

        # Удаление пользователя из базы данных
        db.session.delete(user_to_del)
        db.session.commit()
        logout_user()  # Выход пользователя из системы
        flash('Аккаунт удален!')
        return jsonify({'message': 'Аккаунт успешно удален'}), 200

    flash('Произошла ошибка, пользователь не удален...')
    return jsonify({'message': 'Ошибка удаления аккаунта'}), 500

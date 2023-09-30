from datetime import datetime, timedelta
from sweater.models import Vacancy
from sweater import db


def clear_format(name: str, exclude: str):
    """
    Делает единый формат для хранения вакансий в бд.
    Удаляет лишние пробелы и делает первую букву заглавной.

    :param name: Строка с именами, разделенными запятыми.
    :param exclude: Строка с исключениями, разделенными запятыми.

    :return: Кортеж из двух строк: отформатированное имя и отформатированный список исключений.
    :rtype: tuple
    """
    name = ', '.join(sorted([i.strip() for i in name.split(',') if i.strip() != '']))
    name = name[0].upper() + name.lower()[1:]
    if exclude:
        exclude = ', '.join(sorted([i.strip() for i in exclude.split(',') if i.strip() != '']))
        exclude = exclude[0].upper() + exclude.lower()[1:]
    return name, exclude


def create_vacancy(author_id: int, name: str, exclude: str, region: str, quantity: int, vacancy_json: dict):
    """
    Создает запись о вакансии в базе данных.

    :param author_id: Идентификатор автора вакансии.
    :param name: Название вакансии.
    :param exclude: Исключения для вакансии, разделенные запятыми.
    :param region: Регион для вакансии.
    :param quantity: Количество вакансий.
    :param vacancy_json: JSON-представление вакансии.

    :return: Объект вакансии, если создание прошло успешно, в противном случае - False.
    :rtype: Vacancy or False
    """
    vacancy = Vacancy(author_id=author_id,
                      name=name,
                      exclude=exclude,
                      region=region,
                      quantity=quantity,
                      vacancy_json=vacancy_json)
    try:
        db.session.add(vacancy)
        db.session.commit()
        return vacancy
    except Exception as ex:
        print(ex)
        return False


def check_old_vacancy(name: str, region: str, quantity: int, exclude: str):
    """
    Проверяет наличие старых записей о вакансии в базе данных на основе заданных параметров.

    :param name: Название вакансии.
    :param region: Регион для вакансии.
    :param quantity: Количество вакансий.
    :param exclude: Исключения для вакансии, разделенные запятыми.

    :return: Запись о вакансии, если найдена, в противном случае - None.
    :rtype: Vacancy or None
    """
    if not len(exclude):
        exclude = 'не заданы'
    region = region[0]

    current_datetime = datetime.now()
    one_month_ago = current_datetime - timedelta(days=30)

    existing_vacancy = Vacancy.query.filter_by(
        name=name,
        region=region,
        quantity=quantity,
        exclude=exclude
    ).filter(Vacancy.date_create >= one_month_ago).first()
    print('Нашёл:', existing_vacancy)
    return existing_vacancy

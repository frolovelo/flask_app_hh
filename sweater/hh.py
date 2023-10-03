"""Взаимодействие с HH.RU.API"""
import base64
import io
import textwrap
import time

from collections import Counter
import requests
import pandas as pd
import matplotlib.pyplot as plt


def time_score(func):
    """Замер времени выполнения"""
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(time.time() - start)
        return res

    return wrapper


@time_score
def get_areas() -> dict[str, int]:
    """
    Запрашивает актуальные регионы + id

    :return: {Имя региона: id}
    """
    url = 'https://api.hh.ru/areas'
    response = requests.get(url)
    data = response.json()
    dct = {x['id']: x['name'] for x in data}
    for i in data:
        for j in i['areas']:
            dct[j['id']] = j['name']
    return dct


@time_score
def get_static(name_vacancy: str,
               pages: int = 1,
               per: int = 24,
               region: list[str] = None,
               name_exclude: str = None):
    """
    Запрос к hh.api для получения ключевых навыков по вакансии
    Максимум 120 вакансий - ограничение бесплатного api

    :param name_vacancy: Названия вакансий через запятую.
    :param pages: Кол-во страниц.
    :param per: Вакансий на странице.
    :param region: Название региона и id.
    :param name_exclude: Слова исключения.

    :return: Отсортированный словарь навыков,
    Название региона,
    Кол-во обработанных вакансий,
    Слова исключения
    """

    name_area = region[0]
    area_id = region[1]
    count = 0
    dct = Counter()
    name_vacancy = ' OR '.join([f'"{i.strip()}"' for i in name_vacancy.split(',')])

    if name_exclude:
        name_vacancy += ''.join([f' NOT {i.strip()}' for i in name_exclude.split(',')])
    else:
        name_exclude = 'не заданы'

    url = 'https://api.hh.ru/vacancies'
    params = {'text': name_vacancy, 'per_page': per, 'area': area_id, 'page': None}
    for i in range(1, pages + 1):
        params['page'] = i
        response = requests.get(url, params=params)
        data = response.json()
        vacancy_ids = [item['id'] for item in data['items']]

        for vacancy_id in vacancy_ids:
            response = requests.get(f'https://api.hh.ru/vacancies/{vacancy_id}')
            data = response.json()
            count += 1
            if "key_skills" in data:
                key_skills = [skill['name'].strip() for skill in data['key_skills']]
                dct.update(key_skills)
            else:
                break

    dct = dict(dct)
    lst_sorted_top15 = sorted(dct.items(), key=lambda x: -x[1])[:15]
    sorted_dict = dict(lst_sorted_top15)
    return sorted_dict, name_area, count, name_exclude


# j = 'Python Backend Developer'
# a, b, c, d = get_static(j, pages=1, region=('Россия', '113'))
# print(c)  # 2,9 сек - 1 x 24 - начальный вариант


@time_score
def get_image(dct: dict, quantity: int = 7):
    """
    Создаёт диаграмму навыков

    :param dct: Словарь с навыками {Навык: Кол-во}.
    :param quantity: Кол-во навыков для отрисовки.

    :return: Строку base64
    """
    lst_sorted_top7 = [i for i in dct.items()][:quantity]
    head = ['Навык', 'Кол-во упоминаний']
    df = pd.DataFrame(lst_sorted_top7, columns=head)

    explode = [0.1 for _ in range(len(df['Навык']))]
    plt.pie(df['Кол-во упоминаний'],
            labels=[textwrap.fill(label, 17, replace_whitespace=True) for label in df['Навык']],
            autopct='%1.0f%%',
            startangle=120,
            wedgeprops={"edgecolor": "black",
                        'linewidth': 1,
                        'antialiased': True},
            explode=explode,
            textprops={'fontsize': 10})

    plt.axis('equal')
    buffer = io.BytesIO()
    plt.savefig(buffer,
                format='png',
                transparent=True)

    # Конвертируем буфер в строку base64 и получаем данные изображения
    buffer.seek(1)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8').replace('\n', '')
    plt.close()
    return image_base64

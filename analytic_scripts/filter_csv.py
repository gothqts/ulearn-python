import pandas as pd
from pandas import DataFrame

# Скрипт фильтрации исходного csv файла
choices = '|'.join(
    ['project manager', 'менеджер проект', 'менеджер it проект', 'менеджер ит проект', 'менеджер интернет проект',
     'проджект менеджер', 'проект менеджер', 'проектный менеджер', 'менеджер по проект',
     'менеджер по сопровождению проект', 'управление проект', 'управлению проект', 'project менедж',
     'администратор проект', 'менеджер проектів', 'менеджер it продукт', 'менеджер it product'])
dict_currency = {'USD': 68.67, 'RUB': 1, 'RUR': 1, 'KZT': 0.1484, 'BYR': 28.32, 'UAH': 1.86, 'EUR': 74.34}

for chunk in pd.read_csv('vacancies.csv', chunksize=10 ** 6):
    chunk: DataFrame
    chunk['salary_from'].fillna(0, inplace=True)
    chunk['salary_to'].fillna(0, inplace=True)
    # Фильтрация по вакансии
    # chunk = chunk[chunk['name'].str.contains(choices)]
    chunk['salary'] = (chunk['salary_from'] + chunk['salary_to']) * 0.5 * chunk['salary_currency'].map(dict_currency)
    chunk['year'] = chunk['published_at'].apply(lambda x: x[:4])
    chunk.to_csv(
        'Название файла в который нужно сохранить фильтрованный csv файл',
        mode='a', index=False,
        columns=['salary', 'year', 'area_name']
    )

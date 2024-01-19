import pandas as pd

# Скрипт для фильтрации на скиллы
for chunk in pd.read_csv(
        'vacancies.csv',
        chunksize=10 ** 6,
        usecols=['name', 'key_skills', 'published_at']
):
    chunk['year'] = chunk['published_at'].apply(lambda x: x[:4])
    chunk.dropna(subset=['key_skills'], inplace=True)
    chunk.to_csv('skills.csv', columns=['name', 'key_skills', 'year'], index=False, mode='a')

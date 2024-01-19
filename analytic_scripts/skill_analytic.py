import pandas as pd

choices: str = '|'.join(
    ['project manager', 'менеджер проект', 'менеджер it проект', 'менеджер ит проект', 'менеджер интернет проект',
     'проджект менеджер', 'проект менеджер', 'проектный менеджер', 'менеджер по проект',
     'менеджер по сопровождению проект', 'управление проект', 'управлению проект', 'project менедж',
     'администратор проект', 'менеджер проектів', 'менеджер it продукт', 'менеджер it product'])

file_name: str = 'Название файла где столбы - name, key_skills, year'

data = pd.read_csv(file_name, usecols=['key_skills', 'year'])
# Фильтрация для столбца name
# data = data[data['name'].str.contains(choices)]
data = data[data['key_skills'].notnull()]
groups = data.groupby(['year'])

for year, group in groups:
    formatted_year = str(year[0])
    current_skills_array = []
    for index, row in group.iterrows():
        for skill in row['key_skills'].split('\n'):
            current_skills_array.append(skill)
    DATA: pd.DataFrame = pd.DataFrame({'skills': current_skills_array})
    data: pd.DataFrame = DATA['skills'].value_counts().head(20).to_frame()
    data.plot(kind='bar', fontsize=18, figsize=(30, 22), rot=30, grid=True).get_figure().savefig(
        'Папка в которую необходимо сохранить png - файлы /skills_{}.png'.format(formatted_year))

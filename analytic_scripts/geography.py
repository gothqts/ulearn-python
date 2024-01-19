from typing import List

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

# Аналитики для страницы география
data: DataFrame = pd.read_csv('manager_vacancies.csv', usecols=['area_name', 'salary'])
TOTAL_VACANCIES = data.shape[0]

area_name_groups = data.groupby(['area_name'])


class Stat:
    def __init__(self, area_name: str, salary: float, share: float):
        self.area_name: str = area_name
        self.salary: float = round(salary, 2)
        self.share: float = round(share, 6)

    def __str__(self):
        return f'{self.area_name=} - {self.salary=} - {self.share=}'


x_axis_cities, y_axis = [], []

stat_array: List[Stat] = []

for area_name, group in area_name_groups:
    vacancies_share = group.shape[0] / TOTAL_VACANCIES
    if vacancies_share < 0.01:
        continue
    formatted_area_name = str(area_name[0])
    group['salary'] = pd.to_numeric(group['salary'], downcast='float', errors='coerce')
    average_salary = group['salary'].mean(numeric_only=True, skipna=True)
    stat_array.append(Stat(formatted_area_name, average_salary, vacancies_share))
    x_axis_cities.append(formatted_area_name)
    y_axis.append(average_salary)

stat_array.sort(key=lambda x: x.salary, reverse=True)
stat_array.sort(key=lambda x: x.share, reverse=True)

matplotlib.rcParams.update({'font.size': 6})
plt.xticks(rotation=27)
plt.bar(x_axis_cities, y_axis)
plt.savefig('manager_salary.png')

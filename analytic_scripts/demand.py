import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('manager_vacancies.csv',  usecols=['salary', 'year'])
groups = data.groupby(['year'])
years, salary, vacancies = list(), list(), list()

for year, group in groups:
    group['salary'] = pd.to_numeric(group['salary'], downcast='float', errors='coerce')
    average_salary = round(group['salary'].mean(numeric_only=True, skipna=True), 2)
    vacancies_amount = group.shape[0]
    try:
        year = int(str(year[0]))
        average_salary = average_salary
        years.append(year)
        salary.append(average_salary)
        vacancies.append(vacancies_amount)
    except Exception:
        continue

bar1 = plt.bar(years, salary)
plt.savefig('manager_average_salary.png')

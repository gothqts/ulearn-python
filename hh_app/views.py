from django.shortcuts import render

_VACANCY_NAME = 'Менеджер IT-проекта'


def main_page(request):
    return render(request, 'main.html', context={"vacancy_name": _VACANCY_NAME})


def demand(request):
    return render(request, 'demand.html', context={"vacancy_name": _VACANCY_NAME})

def geography(request):
    return render(request, 'geography.html', context={"vacancy_name": _VACANCY_NAME})

def skills(request):
    return render(request, 'skills.html', context={"vacancy_name": _VACANCY_NAME})


def vacancies(request):
    return render(request, 'vacancies.html', context={"vacancy_name": _VACANCY_NAME})

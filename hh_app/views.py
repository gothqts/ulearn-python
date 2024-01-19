from datetime import date, timedelta
from typing import List, Optional

from django.shortcuts import render

from .models import *
from .skill import SkillTableData
from .vacancies_hh.parser import Parser
from .vacancies_hh.vacancy import Vacancy

_VACANCY_NAME = 'Менеджер IT-проекта'


class DataYearRange:
    RANGE_START: int = 2003
    RANGE_END: int = 2023


def main_page(request):
    return render(request, 'main.html', context={"vacancy_name": _VACANCY_NAME})


def demand(request):
    position_data = PositionYearStat.objects.filter(position_name=_VACANCY_NAME)
    all_vacancies_data = CommonYearStat.objects.all()
    try:
        demand_graphs: Optional[DemandGraph] = DemandGraph.objects.first()
    except Exception:
        demand_graphs = None
    return render(
        request,
        'demand.html',
        context={
            'demand_graph': demand_graphs,
            'position_data': position_data,
            'all_vacancies_data': all_vacancies_data,
            'vacancy_name': _VACANCY_NAME
        }
    )


def geography(request):
    city_stats = CityStat.objects.all()
    position_city_stats = PositionCityStat.objects.filter(vacancy_name=_VACANCY_NAME)
    geography_graph: GeographyGraph = GeographyGraph.objects.first()
    return render(
        request,
        'geography.html',
        context={
            'salary_png': geography_graph.salary,
            'geography_graph': geography_graph,
            'vacancy_name': _VACANCY_NAME,
            'city_statistic': city_stats,
            'position_city_stats': position_city_stats
        }
    )


def skills(request):
    skill_graph = SkillGraph.objects.all()
    year_skill_stats = []
    for year in range(DataYearRange.RANGE_START, DataYearRange.RANGE_END + 1):
        common = CommonSkillStat.objects.filter(year=year)[:20]
        position = PositionSkillStat.objects.filter(year=year, position_name=_VACANCY_NAME)[:20]
        if not common or not position:
            continue
        year_skill_stats.append(SkillTableData(year, common, position))
    return render(
        request,
        'skills.html',
        context={
            'year_skill_stats': year_skill_stats,
            'vacancy_name': _VACANCY_NAME,
            'graphs': skill_graph
        }
    )


def vacancies(request):
    _date = date.today()
    vacancy_list: List[Vacancy] = Parser(
        search_query=_VACANCY_NAME, date_from=_date - timedelta(days=1), date_to=_date,
    ).get_vacancies()
    return render(
        request,
        'vacancies.html',
        context={
            'vacancy_name': _VACANCY_NAME,
            'date': str(_date),
            'vacancies': vacancy_list
        }
    )

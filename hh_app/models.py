from django.db import models

# Create your models here.
# Максимальная длина строк в БД
_CHAR_SEQUENCE_MAX_LENGTH = 64


class PositionYearStat(models.Model):
    year: int = models.IntegerField(
        verbose_name='Год', primary_key=True
    )
    position_name: str = models.CharField(
        verbose_name='Название вакансии', max_length=_CHAR_SEQUENCE_MAX_LENGTH)
    position_salary: float = models.FloatField(
        verbose_name='Средняя зарплата по выбранной профессии'
    )
    position_vacancies: int = models.IntegerField(
        verbose_name='Количество вакансий по выбранной профессии'
    )

    def __str__(self) -> str:
        return f'Статистика по вакансии {self.position_name} за {self.year} год'

    class Meta:
        db_table = 'position_year_stats'
        verbose_name = 'Статистика по вакансии по годам'
        verbose_name_plural = 'Статистика по вакансиям по годам'


class CommonYearStat(models.Model):
    year: int = models.IntegerField(
        verbose_name='Год', primary_key=True
    )
    average_salary: float = models.FloatField(
        verbose_name='Средняя зарплата',
    )
    vacancies_amount: int = models.IntegerField(
        verbose_name='Количество вакансий',
    )

    def __str__(self) -> str:
        return f'Статистика за {self.year} год'

    class Meta:
        db_table: str = 'common_year_stats'
        verbose_name: str = 'Статистика за год'
        verbose_name_plural: str = 'Статистика по годам'


class CityStat(models.Model):
    city: str = models.CharField(
        verbose_name='Город', primary_key=True,
        max_length=_CHAR_SEQUENCE_MAX_LENGTH)
    salary: float = models.FloatField(verbose_name='Средняя зарплата')
    vacancy_percentage: float = models.FloatField(verbose_name='Доля вакансий')

    def __str__(self) -> str:
        return f'Статистика по городу {self.city}'

    class Meta:
        db_table: str = 'city_stats'
        verbose_name: str = 'Статистика по городу'
        verbose_name_plural: str = 'Статистика по городам'


class PositionCityStat(models.Model):
    city: str = models.CharField(
        verbose_name='Город', primary_key=True,
        max_length=_CHAR_SEQUENCE_MAX_LENGTH)
    salary: float = models.FloatField(verbose_name='Средняя зарплата')
    vacancy_percentage: float = models.FloatField(verbose_name='Доля вакансий')
    vacancy_name: str = models.CharField(
        verbose_name='Название вакансии',
        max_length=_CHAR_SEQUENCE_MAX_LENGTH
    )

    def __str__(self) -> str:
        return f'Статистика по вакансии {self.vacancy_name} в городе {self.city}'

    class Meta:
        db_table: str = 'position_city_stats'
        verbose_name: str = 'Статистика по городу и вакансии'
        verbose_name_plural: str = 'Статистика по городам и вакансиям'


class CommonSkillStat(models.Model):
    year: int = models.SmallIntegerField(verbose_name='Год', default=2005)
    skill_name: str = models.CharField(
        verbose_name='Навык', max_length=_CHAR_SEQUENCE_MAX_LENGTH
    )
    notification_amount: int = models.IntegerField(
        verbose_name='Количество упоминаний'
    )

    def __str__(self) -> str:
        return f'Статистика по навыку "{self.skill_name}"'

    class Meta:
        db_table: str = 'common_skill_stats'
        verbose_name: str = 'Статистика по навыку'
        verbose_name_plural: str = 'Статистика по навыкам'


class PositionSkillStat(models.Model):
    year: int = models.SmallIntegerField(verbose_name='Год', default=2005)
    skill_name: str = models.CharField(
        verbose_name='Навык', max_length=_CHAR_SEQUENCE_MAX_LENGTH
    )
    notification_amount: int = models.IntegerField(
        verbose_name='Количество упоминаний'
    )
    position_name: str = models.CharField(
        verbose_name='Название вакансии', max_length=_CHAR_SEQUENCE_MAX_LENGTH
    )

    def __str__(self) -> str:
        return f'Статистика по навыку {self.skill_name}, вакансии {self.position_name}'

    class Meta:
        db_table: str = 'position_skill_stats'
        verbose_name: str = 'Статистика по навыкам по вакансии'
        verbose_name_plural: str = 'Статистика по навыкам по вакансиям'


class DemandGraph(models.Model):
    __DIRECTORY__ = 'demand/'
    """
    Графики для страницы "Востребованность"
    """
    salary_graph = models.ImageField(
        verbose_name='График зарплат',
        upload_to=__DIRECTORY__
    )
    vacancies_graph = models.ImageField(
        verbose_name='График вакансий',
        upload_to=__DIRECTORY__
    )
    position_salary_graph = models.ImageField(
        verbose_name='График зарплат для должности',
        upload_to=__DIRECTORY__
    )
    position_vacancies_graph = models.ImageField(
        verbose_name='График вакансий для должности',
        upload_to=__DIRECTORY__
    )

    class Meta:
        db_table: str = 'demand_graphs'
        verbose_name: str = 'Графики "Востребованность"'
        verbose_name_plural: str = verbose_name


class GeographyGraph(models.Model):
    __DIRECTORY__ = 'geography'
    """
    Графики для страницы "География"
    """
    salary = models.ImageField(
        verbose_name='График зарплат',
        upload_to=__DIRECTORY__
    )
    percentage = models.ImageField(
        verbose_name='Доли вакансий',
        upload_to=__DIRECTORY__
    )
    position_salary = models.ImageField(
        verbose_name='График зарплат для должности',
        upload_to=__DIRECTORY__
    )
    position_share = models.ImageField(
        verbose_name='Доли вакансий для должности',
        upload_to=__DIRECTORY__
    )

    class Meta:
        db_table: str = 'geography_graphs'
        verbose_name: str = 'Графики "География"'
        verbose_name_plural: str = verbose_name


class SkillGraph(models.Model):
    __DIRECTORY__ = 'skills/'

    year = models.IntegerField(
        verbose_name='Год'
    )
    common_graph = models.ImageField(
        verbose_name='Графики по навыкам',
        upload_to=__DIRECTORY__
    )
    position_graph = models.ImageField(
        verbose_name='Графики по навыкам для вакансии',
        upload_to=__DIRECTORY__
    )

    class Meta:
        db_table = 'skill_graphs'
        verbose_name = 'График с навыками'
        verbose_name_plural = 'Графики с навыками'

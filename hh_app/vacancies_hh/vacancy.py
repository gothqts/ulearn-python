import re
from datetime import date
from typing import Any, Optional


class Salary:
    _SALARY_FORMAT: str = '{salary:.2f} {currency}'
    _SALARY_NOT_SPECIFIED: str = 'Не указана'

    def __init__(self, _from: Any, _to: Any, _currency: Optional[str]):
        """
        :param _from: Нижняя граница зарплаты
        :param _to: Верхняя граница зарплаты
        :param _currency: Валюта измерений
        """
        self.salary_from: float = self.__parse_float(_from)
        self.salary_to: float = self.__parse_float(_to)
        self.currency: str = _currency

        self.__check_salary_currency()

    def __parse_float(self, arg: Any) -> float:
        """
        Парсит полученный аргумент к числу с плавающей запятой / возвращает 0.0 при ошибке
        :param arg: Аргумент
        :return: Число с плавающей запятой
        """
        try:
            return float(arg)
        except Exception:
            return 0.0

    def __check_salary_currency(self) -> None:
        """
        Проверяет валюту и при необходимости переводит в рубли
        :return: None
        """
        if self.currency == 'RUB':
            return None
        else:
            # TODO: Запрос к API ЦБ РФ
            pass

    def __str__(self) -> str:
        """
        :return: Среднее значение + Валюта в строковом виде
        """
        if not (self.salary_from or self.salary_to or self.currency):
            return self._SALARY_NOT_SPECIFIED
        average: float = (self.salary_from + self.salary_to) * 0.5
        return self._SALARY_FORMAT.format(salary=average, currency=self.currency)

    @property
    def str(self) -> str:
        """Метод для jinja2"""
        return str(self)


class Vacancy:
    def __init__(
            self,
            name: str,
            description: str,
            key_skills: str,
            company: str,
            salary: 'Salary',
            area_name: str,
            published_at: date
    ):
        """
        :param name: Название вакансии
        :param description: Описание
        :param key_skills: Навыки
        :param company: Компания
        :param salary: Зарплата
        :param area_name: Регион
        :param published_at: Дата публикации
        """
        self.name: str = name
        self.description: str = self.__clear_description(description)
        self.key_skills: str = key_skills
        self.company: str = company
        self.salary: 'Salary' = salary
        self.area_name: str = area_name
        self.published_at: date = published_at

    def __clear_description(self, description: str) -> str:
        """Очищает описание от html-тегов"""
        return self.__shorter(" ".join(re.compile(r'<[^>]+>').sub('', description).strip().split()))

    def __shorter(self, text) -> str:
        """Форматирует описание к 100 символам"""
        return text[:100] + '...' if len(text) > 100 else text

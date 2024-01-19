from concurrent.futures import ThreadPoolExecutor
from datetime import date
from typing import List, Any, Optional, Callable

import requests

from .vacancy import Vacancy, Salary

_VACANCIES_LIMIT: int = 10
_URL_NAME = (
    "https://api.hh.ru/vacancies"
    "?specialization=1"
    "&text={search_query}"
    "&date_from={date_from}"
    "&date_to={date_to}"
    "&order_by=publication_time"
    f"&items_on_page={_VACANCIES_LIMIT}"
)


class Parser:
    def __init__(
            self,
            search_query: str,
            date_from: date,
            date_to: date
    ):
        """
        :param search_query: Строка с запросом для hh
        :param date_from: Начало диапазона поиска
        :param date_to: Конец диапазона поиска
        """
        self.__url = _URL_NAME.format(
            search_query=search_query,
            date_from=str(date_from),
            date_to=str(date_to)
        )

    def get_vacancies(self) -> List[Vacancy]:
        """
        :return: Список вакансий
        """
        json_data: List[dict] = requests.get(url=self.__url).json().get('items')
        vacancy_responses: List[dict] = self.__get_json_list(json_data[:10])
        vacancies: List[Vacancy] = []
        for response in vacancy_responses:
            vacancies.append(self.__parse_vacancy(response))
        return vacancies

    def __parse_vacancy(self, data: dict[Any, Any]) -> Vacancy:
        """
        :param data: Вакансия в json формате
        :return: Вакансию в формате Vacancy
        """
        salary: Salary = self.__parse_salary(data.get('salary'))
        return Vacancy(
            name=data.get('name'),
            description=data.get('description'),
            key_skills=self.__get_skill_string(data.get('key_skills')),
            company=data.get('employer').get('name'),
            salary=salary,
            area_name=data.get('area').get('name'),
            published_at=date.fromisoformat(data.get('published_at')[:10]),
        )

    def __parse_salary(self, data: Optional[dict]) -> Salary:
        """
        :param data: json с данными о зарплате
        :return: зарплату в формате Salary
        """
        if not data:
            return Salary(0, 0, None)
        return Salary(
            _from=data.get('from'),
            _to=data.get('to'),
            _currency=data.get('currency')
        )

    def __get_skill_string(self, data: List[dict]) -> str:
        """
        :param data: Список с навыками в формате json
        :return: Строку с навыками, разделенными запятой
        """
        return ', '.join([skill.get('name') for skill in data][:10])

    def __get_json_list(self, data: List[dict]) -> List[dict]:
        """
        Возвращает список словарей полученных от доп. GET-запроса к странице вакансии
        :param data: Список словарей, из которых берется URL-вакансии
        :return:
        """
        urls = [vacancy.get('url') for vacancy in data]

        def send_request(url: str) -> dict:
            """
            Делает дополнительный запрос и возвращает результат в виде словаря
            :param url: URL-адрес вакансии
            :return: Словарь данных
            """
            return requests.get(url).json()

        return AsyncRequestSender(send_request, urls).get_response_list()


class AsyncRequestSender:
    def __init__(self, sender_func: Callable, urls: List[str]):
        """
        :param sender_func: Функция для потока
        :param urls: Список URL-адресов
        """
        self.sender_func: Callable = sender_func
        self.urls: List[str] = urls

    def get_response_list(self) -> List[Any]:
        """
        :return: Возвращает список возвращаемых значений функции sender_func
        """
        futures = []
        with ThreadPoolExecutor() as executor:
            for url in self.urls:
                futures.append(executor.submit(self.sender_func, url))
            return [future.result() for future in futures]

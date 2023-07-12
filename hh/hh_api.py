import requests
from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    """
    Абстрактный метод для получения данных о вакансиях.
    keyword (str): Ключевое слово для поиска вакансий.
    count (int): Количество вакансий, которое нужно получить.
    """
    @abstractmethod
    def get_request(self, keyword, count):
        pass


class HH(VacancyAPI):
    """
    Класс для получения данных о вакансиях через API(HH).
    keyword (str): Ключевое слово для поиска вакансий.
    count (int): Количество вакансий, которое нужно получить.
    """
    def get_request(self, keyword, count):
        items_per_page = 100
        pages = (count - 1) // items_per_page + 1
        response_data = []
        for page in range(pages):
            params = {
                "text": keyword,
                "page": page,
                "per_page": items_per_page
            }
            data = requests.get('https://api.hh.ru/vacancies', params=params)
            response_data += data.json()['items']
            # Проверяем, достаточно ли уже получено вакансий
            if len(response_data) >= count:
                response_data = response_data[:count]
                break

        return response_data

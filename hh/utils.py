from hh.vacancy import Vacancy


def get_vacancies(hh_api, keyword, count):
    """
    Получает и возвращает список вакансий по ключевым словам.
    """
    vacancies = hh_api.get_request(keyword, count)
    return [
        Vacancy(
            employer=item['employer']['name'],
            name=item['name'],
            salary=item['salary']['to'] if item['salary'] else None,
            description=item['snippet']['responsibility'],
            link=item['alternate_url']
        ) for item in vacancies
    ]

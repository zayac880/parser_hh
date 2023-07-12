import psycopg2 as psycopg2

from config import config


class DBManager:
    """
    Класс для управления базой данных вакансий.
    """

    def __init__(self):
        """
        Инициализация объекта DBManager.
        """

        self.params = config()

    def connect(self):
        """
        Установление соединения с базой данных.

        :return: Объект соединения с базой данных.
        """
        return psycopg2.connect(**self.params)

    def create_database(self):
        """
        Создание базы данных, если она не существует.
        """
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.params['database']}'")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {self.database}")

        cursor.close()
        conn.close()

    def create_tables(self):
        """
        Создание таблицы в базе данных, если она не существует.
        """
        conn = self.connect()
        cursor = conn.cursor()

        # Создание таблицы
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name TEXT,
                salary INTEGER,
                description TEXT,
                link TEXT,
                employer TEXT
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получение списка компаний и количества вакансий по каждой компании.

        :return: Список кортежей в формате (название_компании, количество_вакансий).
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT employer, COUNT(id) FROM vacancies
            GROUP BY employer
        ''')

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    def get_all_vacancies(self):
        """
        Получение всех вакансий из базы данных.

        :return: Список кортежей в формате (название_компании, название_вакансии, зарплата, ссылка).
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT employer, name, salary, link
            FROM vacancies
        ''')

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    def get_avg_salary(self):
        """
        Получение средней зарплаты по вакансиям.

        :return: Средняя зарплата.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT AVG(salary) FROM vacancies
        ''')

        result = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return result

    def get_vacancies_with_higher_salary(self):
        """
        Получение вакансий с зарплатой выше средней.

        :return: Список кортежей в формате (название_компании, название_вакансии, зарплата, ссылка).
        """
        avg_salary = self.get_avg_salary()

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT employer, name, salary, link
            FROM vacancies
            WHERE salary > %s
        ''', (avg_salary,))

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    def get_vacancies_with_keyword(self, keyword):
        """
        Получение вакансий с заданным ключевым словом в названии.

        :param keyword: Ключевое слово.
        :return: Список кортежей в формате (название_компании, название_вакансии, зарплата, ссылка).
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT employer, name, salary, link
            FROM vacancies
            WHERE LOWER(name) LIKE LOWER(%s)
        ''', ('%' + keyword + '%',))

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    def get_vacancies_with_employers(self, employers_string):
        """
        Получение вакансий от выбранных компаний.

        :param employers_string: Строка с названиями компаний, разделенными запятыми.
        :return: Список кортежей в формате (название_компании, название_вакансии, зарплата, ссылка).
        """
        conn = self.connect()
        cursor = conn.cursor()

        employers = employers_string.split(',')

        patterns = ['%' + employer.strip() + '%' for employer in employers]
        query = '''
            SELECT employer, name, salary, link
            FROM vacancies
            WHERE employer ILIKE ANY (ARRAY[{}])
        '''.format(', '.join(['%s'] * len(patterns)))

        cursor.execute(query, patterns)

        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return results

    def insert_vacancies(self, vacancies):
        """
        Вставка списка вакансий в базу данных.

        :param vacancies: Список объектов вакансий для вставки.
        """
        conn = self.connect()
        cursor = conn.cursor()

        for vacancy in vacancies:
            cursor.execute('''
                INSERT INTO vacancies (employer, name, salary, description, link)
                VALUES (%s, %s, %s, %s, %s)
            ''', (vacancy.employer, vacancy.name, vacancy.salary, vacancy.description, vacancy.link))

        conn.commit()

        cursor.close()
        conn.close()

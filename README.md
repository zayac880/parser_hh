# Проект kurs_work

Проект kurs_work представляет собой программу для работы с базой данных вакансий, используя API HeadHunter.

## Как запустить проект

1. Установите необходимые зависимости, выполнив команду:
poetry install
2. Создайте базу данных:
- Запустите скрипт `main.py`:
  ```
  python main.py
  ```

## Как работать с программой

После запуска программы вам будет предложено выбрать одну из следующих опций:

1. Список всех компаний и количество объявлений
- Выводит список всех компаний и количество объявлений (загружает из БД).

2. Поиск вакансий
- Позволяет ввести ключевое слово для поиска вакансий на HeadHunter.
- Запрашивает количество вакансий для отображения.
- Выводит результаты поиска: название компании, название вакансии и ссылку на вакансию.
- Предлагает сохранить найденные вакансии в базу данных.

3. Средняя зарплата по вакансиям
- Выводит среднюю зарплату по всем вакансиям (загружает из БД).

4. Вакансии с зарплатой выше средней
- Выводит список вакансий с зарплатой выше средней (загружает из БД).

5. Вакансии по ключевому слову "python"
- Выводит список вакансий, содержащих ключевое слово "python" (загружает из БД).

6. Вакансии от выбранных компаний
- Вводите имена компаний через запетую.
- Выводит список вакансий от выбранных компаний (загружает из БД).

0. Выход
- Завершает выполнение программы.
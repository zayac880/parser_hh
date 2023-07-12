from hh.hh_api import HH
from hh.utils import get_vacancies
from db_manager import DBManager


def main():
    hh_api = HH()
    # Подключения к базе данных
    db_manager = DBManager()

    # Создание базы данных
    db_manager.create_database()

    # Создание таблицы
    db_manager.create_tables()

    while True:
        print("Меню:")
        print("1. Список всех компаний и количество объявлений")
        print("2. Поиск вакансий")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print('5. Вакансии по ключевому слову "python"')
        print('6. Вакансии от выбранных компаний')
        print("0. Выход")

        choice = input("Выберите опцию: ")

        if choice == "1":
            companies_vacancies_count = db_manager.get_companies_and_vacancies_count()
            print("Количество вакансий по сохраненным компаниям:")
            for company, vacancy_count in companies_vacancies_count:
                print(f"{company}: {vacancy_count}")
        elif choice == "2":
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            count = int(input("Введите количество вакансий для отображения: "))
            vacancies = get_vacancies(hh_api, keyword, count)
            print("Поиск вакансий:")
            for vacancy in vacancies:
                print(f"Название компании: {vacancy.employer}")
                print(f"Название вакансии: {vacancy.name}")
                print(f"Ссылка на вакансию: {vacancy.link}")
                print("---")

            save_choice = input("Сохранить вакансии? (да/нет): ")
            if save_choice.lower() == "да":
                if vacancies:
                    db_manager.insert_vacancies(vacancies)
                    print("Список вакансий сохранен в базе данных.")
                else:
                    print("Нет доступных вакансий для сохранения.")
        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary}")
        elif choice == "4":
            vacancies_higher_salary = db_manager.get_vacancies_with_higher_salary()
            print("Вакансии с зарплатой выше средней:")
            for vacancy in vacancies_higher_salary:
                print(f"Название компании: {vacancy[0]}")
                print(f"Название вакансии: {vacancy[1]}")
                print(f"Зарплата: {vacancy[2]}")
                print(f"Ссылка на вакансию: {vacancy[3]}")
                print("---")
        elif choice == "5":
            keyword = "python"
            vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
            print('Вакансии с ключевым словом "python":')
            for vacancy in vacancies_with_keyword:
                print(f"Название компании: {vacancy[0]}")
                print(f"Название вакансии: {vacancy[1]}")
                print(f"Зарплата: {vacancy[2]}")
                print(f"Ссылка на вакансию: {vacancy[3]}")
                print("---")
        elif choice == "6":
            employers = input("Введите имена компаний через пробел: ")
            vacancies_with_employers = db_manager.get_vacancies_with_employers(employers)
            print("Вакансии от выбранных компаний:")
            for vacancy in vacancies_with_employers:
                print(f"Название компании: {vacancy[0]}")
                print(f"Название вакансии: {vacancy[1]}")
                print(f"Зарплата: {vacancy[2]}")
                print(f"Ссылка на вакансию: {vacancy[3]}")
                print("---")
        elif choice == "0":
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == '__main__':
    main()

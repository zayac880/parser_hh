-- SQL-команда для создания таблиц
-- Создание таблицы "vacancies"
CREATE TABLE vacancies (
    id SERIAL PRIMARY KEY,
    name TEXT,
    salary INTEGER,
    description TEXT,
    link TEXT,
    employer TEXT
);

--Получение всех вакансий из базы данных
SELECT employer, name, salary, link FROM vacancies;

--Получение списка компаний и количества вакансий по каждой компании
SELECT employer, COUNT(id) FROM vacancies GROUP BY employer;

--Получение средней зарплаты по вакансиям.
SELECT AVG(salary) FROM vacancies;


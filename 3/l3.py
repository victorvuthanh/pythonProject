#1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать
# функцию, записывающую собранные вакансии в созданную БД.

#2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной
# платой больше введённой суммы (необходимо анализировать оба поля зарплаты). Для тех,
# кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов с рейтингом
# не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а запрос
# проверяет оба поля)

#3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

from pprint import pprint
from pymongo import MongoClient
import kurs
salary = int(input('Ввод зарплату (RUB):'))
usd_rub = kurs.currency.check_currency()
client = MongoClient('127.0.0.1', 27017)
db = client['vacancies1']
jobs = db.jobs

for i in jobs.find({'currency': 'руб.', '$or': [{'salary_min': {'$gte': salary}}, {'salary_max': {'$gte': salary}}]}):
    pprint(i)
for j in jobs.find(
        {'currency': 'USD', '$or': [{'salary_min': {'$gte': salary / usd_rub}}, {'salary_max': {'$gte': salary / usd_rub}}]}):
    pprint(j)



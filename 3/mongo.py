import hashlib
import json

import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint


from pymongo import MongoClient

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
url = 'https://hh.ru'

params = {'clusters': 'true', 'area': '1', 'ored_clusters': 'true', 'enable_snippets': 'true', 'salary': '',
           'st': 'searchVacancy', 'text': 'python', 'items_on_page':'20'}

response_max = requests.get(url + '/search/vacancy', params=params, headers=headers)
soup_max = bs(response_max.text, 'html.parser')
max_page = int(soup_max.find(text= '...').parent.find(rel="nofollow").text)

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies1']
jobs = db.jobs


vacancy_list = []



for x in range(max_page):
    params['page'] = f'{x}'
    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'html.parser')
    vacancys = soup.find_all('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    for vacancy in vacancys:
        vacancy_data = {}
        info = vacancy.find(target="_blank")
        name = info.text
        link = info['href']
        _id = hashlib.sha1(link.encode('utf-8')).hexdigest()
        vacancy_data['_id'] = _id
        vacancy_data['name'] = name
        vacancy_data['link'] = link


        try:
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text

            if salary[:2] == 'от':
                salary_max = None
                salary_min = int(salary[3:salary.rfind(' ')].replace('\u202f', ''))
            elif salary[:2] == 'до':
                salary_min = None
                salary_max = int(salary[3:salary.rfind(' ')].replace(u'\u202f', ''))
            else:
                salary_min = int(salary[:salary.find(' – ')].replace('\u202f', ''))
                salary_max = int(salary[salary.find(' – ') + 3:salary.rfind(' ')].replace('\u202f', ''))
            currency = salary[salary.rfind(' ') + 1:]
            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['currency'] = currency
            vacancy_list.append(vacancy_data)
            jobs.insert_one(vacancy_data)
        except:
            continue



pprint(vacancy_list)

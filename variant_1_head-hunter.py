import requests
import re
from bs4 import BeautifulSoup
from pprint import pprint
import pandas as pd

input_text = input("Введите интересующую вакансию: ")
url = 'https://hh.ru'
page = 0
vacancies_list = []

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}


def take_salary(web_salary):
    m = False
    if web_salary != "" and web_salary is not None:
        if web_salary.startswith("от"):
            s_min = web_salary[3:].replace('\u202f', " ")
            end = None
        elif web_salary.startswith("до"):
            end = web_salary[3:].replace('\u202f', " ")
            s_min = None
        else:
            web_salary = web_salary.replace('\u202f', " ")
            s_min, end = web_salary.split(" – ")
        if end is None:
            end = s_min
            s_min = None
            m = True
        if s_min != None:
            s_min = int(s_min.replace(" ", ""))
        s_max = end.replace(" ", "")
        s_max = re.findall(r'\d+', end)
        s_max = int(''.join(s_max))
        cur = re.findall(r'[а-я]', end)
        if len(cur) != 0:
            cur = str(''.join(cur))
        else:
            cur = re.findall(r'[a-zA-Z]', end)
            cur = str(''.join(cur))
        if m:
            s_min = s_max
            s_max = None
        return {'a_min_salary': s_min,
                'b_max_salary': s_max,
                'x_currency': cur}


print("Поиск результатов...")
while True:
    params = {'clusters': 'true',
              'ored_clusters': 'true',
              'enable_snippets': 'true',
              'salary': '',
              'text': f"${input_text}",
              'page': page
              }

    response = requests.get(url + '/search/vacancy', params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item'})

    next_button = dom.find_all('a', {'class': 'bloko-button'})
    if not next_button:
        break

    for vacancy in vacancies:
        vacancy_data = {}
        name = vacancy.find('div', {'class': 'vacancy-serp-item__info'}).getText()
        employer = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).getText()
        employer = employer.replace(u'\xa0', " ")
        try:
            web_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        except:
            web_salary = None
        salary = take_salary(web_salary)
        vacancy_ref = vacancy.find('a', {'class': 'bloko-link'})['href']
        vacancy_data['name'] = name
        vacancy_data['salary'] = salary
        vacancy_data['employer'] = employer
        vacancy_data['info'] = vacancy_ref
        vacancy_data['site'] = response.url
        vacancies_list.append(vacancy_data)
    page += 1

df = pd.DataFrame(vacancies_list)
print(df.head(5).to_string())
df.to_csv('vacancies.csv', sep=',', encoding='utf-8')

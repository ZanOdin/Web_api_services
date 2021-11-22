from pprint import pprint
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies']
vacancies = db.vacancies
# vacancies.drop()
print(vacancies.estimated_document_count())

# for doc in vacancies.find({}):
#     pprint(doc)


def filter_salary(vacancies_document):
    while True:
        try:
            x = int(input("Введите числовое значение заработной платы в рублях: "))
            break
        except:
            print("Это не число...")
    for doc in vacancies_document.find({
       'salary': {'$elemMatch': {'$or': [
            {'$and': [{'x_currency': "руб"}, {'a_min_salary': {'$gte': x}}]},
            {'$and': [{'x_currency': "руб"}, {'b_max_salary': {'$gte': x}}]}
       ]}}
    }):
        pprint(doc)


filter_salary(vacancies)

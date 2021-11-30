# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy2911


    def process_item(self, item, spider):
        if item['salary']:
            final_salary = self.process_salary(item['salary'])
            item['min_salary'] = final_salary[0]
            item['max_salary'] = final_salary[1]
            item['currency'] = final_salary[2]
        else:
            item['min_salary'] = None
            item['max_salary'] = None
            item['currency'] = None
        del item['salary']

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        if (salary != None) & (salary != "По договорённости"):
            if salary[0].replace(" ", "") == "от":
                try:
                    min = int(salary[1].replace("\xa0", ""))
                    try:
                        max = int(salary[3].replace("\xa0", ""))
                        cur = salary[5]
                    except:
                        cur = salary[3]
                        max = None
                except:
                    min = int(salary[2].replace("\xa0руб.", "").replace("\xa0", ""))
                    cur = salary[2][-4:]
                    max = None
            elif salary[0] == "до":
                try:
                    max = int(salary[1].replace("\xa0", ""))
                    cur = salary[3]
                except:
                    max = int(salary[2].replace("\xa0руб.", "").replace("\xa0", ""))
                    cur = salary[2][-4:]
                min = None
            elif self.num_there(salary[0]):
                min = int(salary[0].replace("\xa0", ""))
                max = None
                try:
                    max = int(salary[4].replace("\xa0", ""))
                    cur = salary[6]
                except:
                    max = None
                    cur = None
            else:
                min = None
                max = None
                cur = None
        return min, max, cur

    # "\xa0" in salary[0]
    def num_there(self, s):
        return any(i.isdigit() for i in s)

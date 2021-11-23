from pprint import pprint
import requests
from lxml import html
from pymongo import MongoClient

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_mongo = db.news

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
url = 'https://lenta.ru'

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)
# После начальной ссылки дома здесь, всё равно ищет все новости...
news_web = dom.xpath(
    "//section[contains(@class, 'b-yellow-box js-yellow-box')]/div[contains(@class, 'b-yellow-box__wrap')]")

news_list = []
#  or contains(@class, 'b-link-external')
for news in news_web:
    news_title = news.xpath(".//div[@class='item']/a[contains(@href, '/news/2021/') or contains(@class, "
                            "'b-link-external')]/text()")
    news_href = news.xpath(".//a[contains(@href, '/news/2021') or contains(@class, 'b-link-external')]/@href")

i = 0
while True:
    if len(news_title) == i:
        break
    news_info = {}
    news_info['title'] = news_title[i].replace("\xa0", " ")
    news_info['ns_link'] = url + news_href[i]

    # Date
    date_response = requests.get(url + news_href[i], headers=headers)
    date_dom = html.fromstring(date_response.text)
    news_date = date_dom.xpath("//div[contains(@class, 'b-topic__info')]")
    one_date = "Неизвестная дата"
    for date in news_date:
        if date.xpath("//time[contains(@class, 'g-date')]"):
            one_date = date.xpath("//time[contains(@class, 'g-date')]/text()")
    news_info['site'] = url
    news_info['date'] = one_date
    news_list.append(news_info)
    i += 1

    result = news_mongo.find_one({'title': news_info['title']})
    if result is None:
        news_mongo.insert_one(news_info)

pprint(news_list)
print(f"Количество новостей в БД: {news_mongo.estimated_document_count()}")

# По правде говоря, работа с BeautifulSoup показалась куда-интереснее

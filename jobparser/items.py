# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from platform import processor

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def process_price(price):
    try:
        price = int(price.replace(' ', ''))
    except Exception as e:
        print(e)
    finally:
        return price


class LeroyparserItem(scrapy.Item):

    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(process_price))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()

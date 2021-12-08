# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    # define the fields for your item here like:
    main_user = scrapy.Field()
    follower_id = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()


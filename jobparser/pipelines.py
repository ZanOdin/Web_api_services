# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


import scrapy
from scrapy.pipelines.images import ImagesPipeline
import hashlib
from w3lib.util import to_bytes


YEAR = '2021'


class LeroyparserPipeline:
    def process_item(self, item, spider):
        return item


class LeroyPhotosPipeline(ImagesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, download_func, settings)
        self.name = ""

    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
# Если долго мучиться - что-нибудь получится :)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        name = item['name'].split(" ")[0]
        self.name = name
        return item

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return 'full/%s/%s.jpg' % (self.name[:10], image_guid)

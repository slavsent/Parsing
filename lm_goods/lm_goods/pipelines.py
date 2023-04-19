# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import os
from urllib.parse import urlparse


class LmGoodsPipeline:
    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.parser_db_goods

    def process_item(self, item, spider):
        collection = self.mongo_db[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print(f"The item with id {item['_id']} already exists. ")

        return item


class LmPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                print(f'######{img}######')
                try:
                    yield Request(img)
                except Exception as err:
                    print(err)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f"{item['name']}/{os.path.basename(urlparse(request.url).path)}"

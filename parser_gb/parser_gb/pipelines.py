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


class ParserGbPipeline:

    def __init__(self):
        client = MongoClient('localhost:27017')
        self.mongo_db = client.parser_db_course

    def process_item(self, item, spider):
        collection = self.mongo_db['gb_ru']
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            print(f"The item with id {item['_id']} already exists. ")
        return item

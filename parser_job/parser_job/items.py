# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserJobItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    salary_from = scrapy.Field()
    salary_to = scrapy.Field()
    salary_cur = scrapy.Field()
    salary_info = scrapy.Field()
    _id = scrapy.Field()

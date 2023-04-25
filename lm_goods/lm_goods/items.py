# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


def clean_price(value):
    try:
        value = int(value[0].replace(' ', ''))
        value = list(value)
    except Exception:
        return value
    return value


class LmGoodsItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(clean_price), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(lambda x: ('https:' + x)))
    _id = scrapy.Field()

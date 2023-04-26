import scrapy
from scrapy.http import HtmlResponse
import os
import dotenv
from parser_gb.items import ParserGbItem
from scrapy.loader import ItemLoader


dotenv.load_dotenv()


class GbRuSpider(scrapy.Spider):
    name = "gb_ru"
    allowed_domains = ["gb.ru"]
    start_urls = ["https://gb.ru/"]
    start_urls_login = "https://gb.ru/login"
    username = os.getenv('USER_GB')
    usr_password = os.getenv('PASS_GB')


    def parse(self, response: HtmlResponse):
        csrf = 'uGOGU4XjTx9kOg8UkoTGtTm6EsSCTTvK/2PbKMXrtLV8iNxfc1N7TtzIxX5lK44s3GfbsKCrwIO98CZDZEXEqw=='

        yield scrapy.FormRequest(
            self.start_urls_login,
            method='POST',
            callback=self.after_login,
            formdata={'user_email': self.username, 'user_password': self.usr_password},
            headers={'csrf-token': csrf}
        )


    def after_login(self, response: HtmlResponse):
        yield response.follow('https://gb.ru', callback=self.parse_data)

    def parse_data(self, response: HtmlResponse):

        courses_links = response.xpath("//a[@class='direction-card']/@href").getall()
        for link in courses_links:
            yield response.follow(f'https://gb.ru{link}', callback=self.parse_course)
            #print(f'\n***************\n{link}\n******************\n')

    def parse_course(self, response: HtmlResponse):
        loader = ItemLoader(item=ParserGbItem(), response=response)

        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('course', "//span[@class='direction-card__title-text ui-text-body--1 ui-text--bold']//text()")
        yield loader.load_item()


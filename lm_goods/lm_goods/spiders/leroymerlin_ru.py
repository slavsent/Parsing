import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from lm_goods.items import LmGoodsItem


class LeroymerlinRuSpider(scrapy.Spider):
    name = "leroymerlin_ru"
    # allowed_domains = ["tddomovoy.ru"]
    allowed_domains = ["www.magazinbt.ru"]

    # start_urls = ["https://tddomovoy.ru/catalog/bytovaya-tekhnika/tovary-dlya-ukhoda-za-odezhdoy-i-obuvyu/mashinki-dlya-strizhki-katyshkov/"]
    start_urls = ["https://www.magazinbt.ru/blinnitsi"]

    def parse(self, response: HtmlResponse):
        # goods_links = response.xpath("//div[@class='goods-card__rslides-wrapper']/ul/li/a/@href").getall()
        goods_links = response.xpath(
            "//a[contains(@class, 'stretched-link text-body card-link font-weight-bold')]/@href").getall()

        for link in goods_links:
            yield response.follow(link, callback=self.parse_goods)
            # print(f'\n***************\n{link}\n******************\n')

        # print(f'\n***************\n{goods_links}\n******************\n')

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=LmGoodsItem(), response=response)

        loader.add_xpath('name', '//h1/text()')
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[@class='text-danger price text-nowrap']//text()")
        # loader.add_xpath('photos', "//a[contains(@class, 'd-block text-center')]/@href")
        loader.add_xpath('photos', "//img[contains(@class, 'img-fluid d-block mx-auto')]/@src")
        yield loader.load_item()

        # goods_name = response.css("h1::text").get()
        # goods_url = response.url
        # goods_price = response.xpath("//span[@class='text-danger price text-nowrap']//text()").getall()
        # goods_foto = response.xpath("//img[contains(@class, 'img-fluid d-block mx-auto')]/@src").getall()
        # yield LmGoodsItem(
        #    name=goods_name,
        #    url=goods_url,
        #    price=goods_price,
        #    photos=goods_foto
        # )
        # print(f'\n#############\n{goods_name}\n{goods_url}\n{goods_price}\n{goods_foto}\n################\n')

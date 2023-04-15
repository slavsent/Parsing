import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class HhRuSpider(scrapy.Spider):
    name = "hh_ru"
    allowed_domains = ["hh.ru"]
    # start_urls = ['https://spb.hh.ru/search/vacancy?area=88&search_field=company_name&search_field=description&text=python&no_magic=true&L_save_area=true&search_period=30&items_on_page=20']

    start_urls = ['https://hh.ru/search/vacancy?area=1&ored_clusters=true&text=python&search_period=30']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@data-qa='serp-item__title']/@href").getall()
        for link in vacancies_links:
            yield response.follow(link, callback=self.parse_vacancy)
            # print(f'\n***************\n{link}\n******************\n')

        # print(f'\n***************\n{vacancies_links}\n******************\n')

    def parse_vacancy(self, response: HtmlResponse):
        vacancies_name = response.css("h1::text").get()
        vacancies_url = response.url
        vacancies_salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()

        vacancies_salary_to = ''
        vacancies_salary_from = 0
        vacancies_salary_currency = 'руб.'
        currency = ['руб.', 'EUR', 'USD']
        if vacancies_salary[0] == 'з/п не указана':
            vacancies_salary_from = 0
            vacancies_salary_to = 0
            vacancies_salary_currency = 'руб.'
            vacancies_salary_info = vacancies_salary[0]
        else:
            if 'от ' not in vacancies_salary:
                vacancies_salary_from = 0
            if ('до ' not in vacancies_salary) or (' до ' not in vacancies_salary):
                vacancies_salary_to = ''
            for i in range(len(vacancies_salary) - 1):

                if vacancies_salary[i] == 'от ':
                    vacancies_salary_from = int(vacancies_salary[i + 1].replace("\xa0", ''))
                if vacancies_salary[i] == 'до ' or vacancies_salary[i] == ' до ':
                    vacancies_salary_to = int(vacancies_salary[i + 1].replace("\xa0", ''))
                if vacancies_salary[i] == '-':
                    vacancies_salary_from = int(vacancies_salary[i - 1].replace("\xa0", ''))
                    vacancies_salary_to = int(vacancies_salary[i + 1].replace("\xa0", ''))
                if vacancies_salary[i] in currency:
                    vacancies_salary_currency = vacancies_salary[i]
            vacancies_salary_info = vacancies_salary[-1]

        yield ParserJobItem(
            name=vacancies_name,
            url=vacancies_url,
            salary_from=vacancies_salary_from,
            salary_to=vacancies_salary_to,
            salary_cur=vacancies_salary_currency,
            salary_info=vacancies_salary_info
        )
        # print(f'\n#############\n{vacancies_name}\n{vacancies_url}\n{vacancies_salary}\n################\n')

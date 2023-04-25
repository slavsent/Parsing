import scrapy
from scrapy.http import HtmlResponse
from parser_job.items import ParserJobItem


class SuperjobRuSpider(scrapy.Spider):
    name = "superjob_ru"
    allowed_domains = ["superjob.ru"]
    start_urls = ["https://www.superjob.ru/vacancy/search/?keywords=Python"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='_1IHWd _6Nb0L _37aW8 _17KD8 f-test-button-dalshe f-test-link-Dalshe']/@href").get()
        if next_page:
            full_next_page = f'https://www.superjob.ru{next_page}'
            yield response.follow(full_next_page, callback=self.parse)

        vacancies_links = response.xpath("//span[@class='_1c5Bu _1Yga1 _1QFf5 _2MAQA _1m76X _3UZoC _3zdq9 _1_71a']/a/@href").getall()
        for link in vacancies_links:
            link_full = f'https://www.superjob.ru{link}'
            yield response.follow(link_full, callback=self.parse_vacancy)
            # print(f'\n***************\n{link}\n******************\n')

        # print(f'\n***************\n{vacancies_links}\n******************\n')

    def parse_vacancy(self, response: HtmlResponse):
        vacancies_name = response.css("h1::text").get()
        vacancies_url = response.url
        vacancies_salary = response.xpath("//span[@class='_2eYAG _1m76X _3UZoC _3iH_l']//text()").getall()

        # print(f'\n#############\n{vacancies_name}\n{vacancies_url}\n{vacancies_salary}\n################\n')

        vacancies_salary_to = ''
        vacancies_salary_from = 0
        vacancies_salary_currency = 'USD'
        vacancies_salary_info = ''
        if vacancies_salary[0] == 'По договорённости' or len(vacancies_salary) == 0:
            vacancies_salary_from = 0
            vacancies_salary_to = 0
            vacancies_salary_currency = 'руб.'
            if len(vacancies_salary) != 0:
                vacancies_salary_info = vacancies_salary[0]
        else:
            if ('от' not in vacancies_salary) and ('до' not in vacancies_salary) and ('—' not in vacancies_salary):

                vacancies_salary_from = int(vacancies_salary[0].replace("\xa0", ''))
                if (vacancies_salary[2] == '₽') or (vacancies_salary[-1] == '₽'):
                    vacancies_salary_currency = 'руб.'
            else:
                for i in range(len(vacancies_salary)):

                    if vacancies_salary[i] == 'от':
                        vacancies_salary_from = int(vacancies_salary[i + 2].replace("\xa0", '')[:-1:])
                        if vacancies_salary[i + 2].replace("\xa0", '')[-1] == '₽':
                            vacancies_salary_currency = 'руб.'
                    if vacancies_salary[i] == 'до' or vacancies_salary[i] == ' до ':
                        vacancies_salary_to = int(vacancies_salary[i + 2].replace("\xa0", '')[:-1:])
                        if vacancies_salary[i + 2].replace("\xa0", '')[-1] == '₽':
                            vacancies_salary_currency = 'руб.'
                    if vacancies_salary[i] == '—':
                        vacancies_salary_from = int(vacancies_salary[i - 2].replace("\xa0", ''))
                        vacancies_salary_to = int(vacancies_salary[i + 2].replace("\xa0", ''))
                        if vacancies_salary[i + 4] == '₽':
                            vacancies_salary_currency = 'руб.'

        yield ParserJobItem(
            name=vacancies_name,
            url=vacancies_url,
            salary_from=vacancies_salary_from,
            salary_to=vacancies_salary_to,
            salary_cur=vacancies_salary_currency,
            salary_info=vacancies_salary_info
        )

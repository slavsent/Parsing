from lxml import html
from pprint import pprint
import requests


def jobs_suoperjob(name_job, pages=0):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    dict_jobs = {}
    j = 0
    for num_page in range(0, pages + 1):
        if num_page == 0:
            str_page = ''
        else:
            str_page = f'?page={num_page+1}'
        url = f'https://www.superjob.ru/vakansii/{name_job}.html{str_page}'

        req = requests.get(url=url, headers=headers)
        root = html.fromstring(req.text)
        jobs = root.xpath("//div[@class='_3-q4I _4J5rK _2-wuk _3lgWg']")

        for el in jobs:
            name_jobs = el.xpath("./div/div/div/span/a/span[@class='_1Ijga']/text()")
            name_jobs = ', '.join(name_jobs)
            link_jobs = el.xpath("./div/div/div/span/a/@href")
            link_jobs = f'https://www.superjob.ru{link_jobs[0]}'
            salary = el.xpath("./div/div[2]/div/div/span/text()")
            if len(salary) <= 1:
                salary_min = ''
                salary_max = ''
            elif len(salary) == 4:
                if salary[0] == 'от':
                    salary_max = ''
                    salary_min = ''.join(salary[2].split('\xa0')[:2:]).replace(' ', '')
                elif salary[0] == 'до':
                    salary_min = ''
                    salary_max = ''.join(salary[2].split('\xa0')[:2:]).replace(' ', '')
                else:
                    salary_max = ''
                    salary_min = ''.join(salary[0].split('\xa0')[:2:]).replace(' ', '')
            elif len(salary) == 8:
                salary_min = ''.join(salary[0].split('\xa0')[:2:]).replace(' ', '')
                salary_max = ''.join(salary[4].split('\xa0')[:2:]).replace(' ', '')
            dict_jobs[f'superjob_{name_job}_{j}'] = {
                'name': name_jobs,
                'site_job': 'superjob.ru',
                'link-jobs': link_jobs,
                'salary_min': salary_min,
                'salary_max': salary_max,
            }
            j += 1
    return dict_jobs


if __name__ == '__main__':
    print('Page 1')
    print(jobs_suoperjob('elektrik', 0))
    print('Page 2')
    print(jobs_suoperjob('elektrik', 1))
    print('Page 3')
    print(jobs_suoperjob('elektrik', 2))


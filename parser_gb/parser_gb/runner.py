from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.gb_ru import GbRuSpider
from pymongo import MongoClient


def order_to_bd():
    client = MongoClient('localhost:27017')
    db = client.parser_db_course
    print('Есть такие направления:')
    j = 1
    for el_db in db.gb_ru.find():
        print(f"{j}. {el_db['name']}")
        j += 1
    while True:
        course_select = input('Введите номер направление по которому хотите посмотреть курсы или exit: ')
        if course_select == 'exit':
            break
        try:
            course_select = int(course_select)
        except ValueError:
            print('Вы ввели не цифру')
            continue
        i = 1
        for el_db in db.gb_ru.find():
            if i == int(course_select):
                print('Список программ по направлению:')
                print(', \n'.join(el_db['course']))
                print(f'Доп информация по ссылке: {el_db["url"]}')
            i += 1


if __name__ == '__main__':
    my_select = input('Нужен паринг нажмите y: ')
    if my_select == 'y':
        configure_logging()
        settings = get_project_settings()
        runner = CrawlerRunner(settings)
        runner.crawl(GbRuSpider)

        reactor.run()

    input_select = input('Хотите сделать запрос к БД(y/n): ')
    if input_select == 'y':
        order_to_bd()
    print('Программа завершена')

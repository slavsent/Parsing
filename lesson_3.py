import requests
from bs4 import BeautifulSoup as bs


def parsing_quotes_to_scrape(pages=1):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    if 0 <= pages <= 1:
        pages = 0
    elif pages >= 40:
        pages = 40
    list_data = []
    for num_page in range(0, pages + 1):
        if num_page == 0:
            str_page = ''
        else:
            str_page = f'/page/{num_page + 1}/'
        url = f'https://quotes.toscrape.com{str_page}'

        req = requests.get(url=url, headers=headers)
        soup = bs(req.text, 'html.parser')
        data_scrape = soup.find_all('div', attrs={'itemtype': "http://schema.org/CreativeWork"})
        for el in data_scrape:
            name_scrape = el.find('span', attrs={'class': 'text', 'itemprop': 'text'}).text
            author_scrape = el.find('small', attrs={'class': 'author'}).text
            tag_scrape = el.select('a')
            tags_scrape = []
            for tag in tag_scrape:
                tags_scrape.append(tag.string)
            dict_data = {
                'text': name_scrape,
                'author': author_scrape,
                'tags': tags_scrape
            }

            list_data.append(dict_data)
    return list_data


if __name__ == '__main__':
    print('Page 1')
    print(parsing_quotes_to_scrape(0), len(parsing_quotes_to_scrape(0)))
    print('Page 2')
    print(parsing_quotes_to_scrape(1), len(parsing_quotes_to_scrape(1)))
    print('Page 3')
    print(parsing_quotes_to_scrape(3), len(parsing_quotes_to_scrape(3)))

import csv
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
import time
from random import randrange
from tqdm.auto import tqdm

ua = UserAgent()
headers = {'User-Agent': ua.random}


def get_html(url, params=None):
    response = requests.get(url, headers=headers, params=params)
    return response


# получаем ссылки товаров на текущей странице
def get_items_list(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('div', class_='product-thumb')
    items_list = [item.find('div', class_='image').find('a').get('href') for item in items]
    return items_list


# создаем csv-фаил с указанными полями, создаем безконечный цикл (если страница не указана в ручную)
# и получаем информацию с по конкретному обьекту, записывая данные в csv-файл
def main(page=1):
    with open('data.csv', 'w', newline='', encoding='cp1251') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            (
                'Название',
                'Картинка',
                'Цена',
                'Производитель',
                'Характеристики'
            )
        )

    while True:
        url = f'https://www.dahua.market/kamery-videonablyudeniya/?page={page}'
        html = get_html(url)
        if len(get_items_list(html.text)):
            for item in tqdm(get_items_list(html.text)):
                time.sleep(randrange(1, 3))
                html = get_html(item)
                soup = BS(html.text, 'html.parser')
                name = soup.find('div', class_='col-sm-9').find('h1').get_text().strip()
                image = soup.find('a', class_='thumbnail imglink').get('href')
                manufactor = soup.find('a', attrs={"itemprop": "manufacturer"}).get_text()
                price = soup.find('span', class_='autocalc-product-price').get_text().replace('₽', "")
                info = soup.find('div', class_='tab-pane active').get_text().split()
                formated_info = ' '.join(info)
                with open('data.csv', 'a', errors='replace', newline='', encoding='cp1251') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        (
                            name,
                            image,
                            price,
                            manufactor,
                            formated_info
                        )
                    )

            print(f'Спарсили страницу {page}')
            page += 1
        else:
            print('Done!')
            break


# в мейн можно указать с какой страницы начинаем парсить, по умолчанию 1
if __name__ == '__main__':
    main()

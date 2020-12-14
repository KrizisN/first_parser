import requests
from bs4 import BeautifulSoup
import csv

HOST = 'https://www.work.ua/'
URL = 'https://www.work.ua/ru/jobs-kharkiv-python+developer/'
CARD_CSV = 'card.csv'

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link')
    vacancies = []

    for item in items:
        vacancies.append(
            {
                'title': str(item.find('a').get_text(strip=True)).replace(',',''),
                'organisations': str(item.find('div', class_='add-top-xs').find('span').find('b').get_text(strip=True)).replace(',',''),
                'link': HOST + item.find('h2').find('a').get('href'),
                'description': str(item.find('p', class_='overflow text-muted add-top-sm add-bottom').get_text(strip=True)).replace(',',''),
                'date': item.find('div', class_='pull-right').find('span', class_='text-muted small').get_text()
            }
        )
    return vacancies


def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Вакансия', 'Организация', 'Ссылка', 'Описание', 'Дата'])
        for item in items:
            writer.writerow([item['title'], item['organisations'], item['link'], item['description'], item['date']])


def parser():
    html = get_html(URL)
    paginate = int(input('Кол-в страниц для парсинга'))
    vacancies = []
    if html.status_code == 200:
        for page in range(1, paginate):
            html = get_html(URL, params={'page': page})
            vacancies.extend(get_content(html.text))
        save_doc(vacancies, CARD_CSV)
    else:
        print('Error')


if __name__ == '__main__':
    parser()
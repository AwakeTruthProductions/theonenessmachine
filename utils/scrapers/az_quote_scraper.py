import csv
from datetime import datetime
import re
import requests
import sys
from bs4 import BeautifulSoup
import urllib.parse as uparser


def scrape(url):
    print('scraping ' + url)
    today = datetime.now().strftime('%m%d%Y')
    file_name = f'utils/data/csv/{today}.csv'
    page = requests.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'html.parser')
        quotes_ul = soup.find('ul', class_='list-quotes')
        quotes_div = quotes_ul.find_all('div', class_='wrap-block')

        with open(file_name, 'a+', newline='') as quote_file:
            writer = csv.writer(quote_file, delimiter=',')
            for quote in quotes_div:
                a = quote.p.find('a', class_='title')
                author = a.attrs['data-author']
                clean_quote_list = [
                    str(el).replace('<br/>', '') for el in a.contents
                ]
                quote_text = ''.join(clean_quote_list)
                writer.writerow([author, quote_text])

        page_div = soup.find('div', class_='pager')
        next_li = page_div.find('li', class_='next')
        if 'inactive' not in next_li['class']:
            next_path = next_li.a['href']
            next_url = uparser.urljoin(url, next_path)
            next_page = requests.get(next_url)
            if next_page.status_code == 200:
                scrape(next_url)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        scrape(sys.argv[1])

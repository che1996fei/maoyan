import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import time
import json


def get_one_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('dd')
    for item in items:
        index = item.find(name='i', class_='board-index').get_text()
        name = item.find(name='p', class_='name').get_text()
        start = item.find(name='p', class_='star').get_text().strip()
        time = item.find(name='p', class_='releasetime').string
        score = item.find(name='p', class_='score').get_text()
        yield {
                'index': index,
                'name': name,
                'star': start,
                'time': time,
                'score': score
            }

def write_to_file(conten):
    with open('result1.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(conten, ensure_ascii=False) + '\n')
        f.close()

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
        time.sleep(1)

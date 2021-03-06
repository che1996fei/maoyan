import requests
from requests.exceptions import RequestException
import re
import time
import json

# 请求网页
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None
#获取文本
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                          +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S) #将正则字符串转为正则表达式对象，包括换行符
    items = re.findall(pattern, html) #用findall()进行匹配
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5]+item[6]
        }

#写入文件
def write_to_file(conten):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(conten, ensure_ascii=False) + '\n') #用dump()方法将JSON对象转为文本字符串，并且输出为中文
        f.close()

def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset) #构建url
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    #进行迭代
    for i in range(10):
        main(i * 10)
        time.sleep(1) #增加延时等待

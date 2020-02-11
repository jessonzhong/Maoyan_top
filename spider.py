import json
import requests
from requests.exceptions import RequestException
import re

# from multiprocessing import Pool


headers = {
    'Content-Type': 'text/plain; charset=UTF-8',
    'Origin': 'https://maoyan.com',
    'Referer': 'https://maoyan.com/board/4',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 Edg/80.0.361.48'
}


# 请求单页源码
def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# 解析单页内容
def parse_one_page(html):
    # 正则解析提取信息
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '排名': item[0],
            '图片': item[1],
            '标题': item[2],
            '主演': item[3].strip()[3:],
            '上映时间': item[4].strip()[5:],
            '评分': item[5] + item[6]
        }


# 保存排名信息到本地
def write_to_file(content):
    with open('top100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    # pool = Pool()  # 编写进程池
    # pool.map(main, [i*10 for i in range(10)])  # 多线程爬取

    for i in range(10):  # for循环爬取
        main(i*10)

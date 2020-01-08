import csv
import requests
import time
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

start_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1974808274&containerid=1076031974808274&since_id=4456639333301952'
common_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1974808274&containerid=1076031974808274&since_id={}'
requests_headers = {
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Referer': 'https://m.weibo.cn/u/1974808274',
    'User-Agent': ua.random,
    'X-Requested-With': 'XMLHttpRequest',
    'X-XSRF-TOKEN': 'f4a008'
}


def spider(url=start_url):
    ret = requests.get(url=url, headers=requests_headers).json()
    return ret


def change_url(ret):
    since_id = ret['data']['cardlistInfo']['since_id']
    next_url = common_url.format(since_id)
    global start_url
    start_url = next_url


def get_data(ret):
    text_list = []
    cards = ret['data']['cards']
    for card in cards:
        text = card['mblog']['text']
        if '女乘客' in text:
            text_list.append([text])
    return text_list


def save_data(file_name, data_list):
    """
    保存数据
    :param file_name: 文件名，不需要加后缀
    :param data_list: 写入的值,格式：[[],[],[],[],[]]
    """
    f_name = file_name + ".csv"
    with open(f_name, "a", newline="", encoding="utf-8") as f:
        c = csv.writer(f)
        for i in data_list:
            c.writerow(i)


def start():
    i = 0
    while i < 1000:
        print(f'----------------{i}----------------')
        ret = spider(start_url)
        change_url(ret)
        data = get_data(ret)
        save_data('1', data)
        time.sleep(0.5656)
        i += 1


if __name__ == '__main__':
    start()

# -*- coding: utf-8 -*-
import csv
import time
import re
import os
import sys
import requests
from lxml import html

"""
爬不同的微博换个id就行，40行，cookie貌似不用换
"""
proxy = {}

etree = html.etree

# 用的是熊猫代理 http://www.xiongmaodaili.com/ ，按量提取，每次提取1个ip，json格式，买3块钱的就差不多了
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=3f3a3212bb8129e0d70d325c41bed8c7&orderNo=GL20200223101445SA8mbNNF&count=1&isTxt=0&proxyType=1'

# 过期了就换一下
cookie = 'ALF=1585289771; _T_WM=24942942014; WEIBOCN_FROM=1110005030; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZf1bXoi1rXXtq6YEUsDSteo8t1CEuPk4SG2Eis-g-RrOg.; SUB=_2A25zUn9XDeRhGeVI7lER9CvFyD6IHXVQvQEfrDV6PUJbktANLVPfkW1NTAX_rD7YTm16TrDhv9dNGLwzafOdPIgl; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=00xZQkwwDqf5l8; SSOLoginState=1582698247; MLOGIN=1; _ga=GA1.2.852180565.1582702609; _gid=GA1.2.1190095481.1582702609; M_WEIBOCN_PARAMS=oid%3D4469177786494007%26luicode%3D20000061%26lfid%3D4469177786494007%26uicode%3D20000061%26fid%3D4469177786494007; XSRF-TOKEN=b7fa37'

header = {
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://m.weibo.cn/status/It1D4rfo3',
    'mweibo-pwa': '1',
    'x-xsrf-token': 'b7fa37',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'cookie': cookie,
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'http://gl.sach.gov.cn/?from=singlemessage&isappinstalled=0',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36'
}

url = 'https://m.weibo.cn/api/statuses/repostTimeline'


def spider(page):
    param = {
        # 这个id要抓包获取，代表那条微博
        'id': '4469177786494007',
        # 'id': '4469112517984891',
        'page': page
    }
    need_list = []

    def get_ret(count):
        # noinspection PyBroadException
        try:
            ret = requests.get(url=url, params=param, headers=header, proxies=proxy, timeout=6).json()
            return ret
        except Exception:
            time.sleep(1)
            change_proxy(3)
            return get_ret(count - 1)

    ret = get_ret(3)
    ok = ret['ok']
    if ok == 1:
        data = ret['data']['data']
        for d in data:
            html = d['text']
            root = etree.HTML(html)
            text = root.xpath("string(/)")
            print(text)
            if '//<a' in html:
                forward_user_name = d['user']['screen_name']  # 转发人昵称
                p = re.compile(r'//@(.*?)[:：]', re.S)
                forwarded_user_names = p.findall(text)  # 被转发人昵称列表
                forwarded_user_name = forwarded_user_names[0]  # 被转发人昵称
            else:
                forward_user_name = d['user']['screen_name']  # 转发人昵称
                forwarded_user_name = d['retweeted_status']['user']['screen_name']  # 被转发人昵称
                forwarded_user_names = [forwarded_user_name]

            verified = d['user']['verified']  # 是否认证
            created_at = d['created_at']  # 创建时间
            need = [forward_user_name, forwarded_user_name, text, verified, created_at, forwarded_user_names]
            print(need)
            need_list.append(need)
        return need_list


def get_path(file_name):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    return path


def save_data(filename, data):
    path = get_path(filename + '.csv')
    if os.path.isfile(path):
        is_exist = True
    else:
        is_exist = False
    with open(path, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            c.writerow(['转发人', '被转发人', '转发内容', '是否认证', '创建时间', '转发人列表'])
        for line in data:
            c.writerow(line)


def change_proxy(retry_count):
    if retry_count < 0:
        return

    result = requests.get(proxy_url).json()
    if result['msg'] == 'ok':
        ip = result['obj'][0]['ip']
        port = result['obj'][0]['port']
        proxies = {"http": "http://" + ip + ":" + port, "https": "http://" + ip + ":" + port}

        global proxy
        proxy = proxies

        print(f"代理ip为更改为：{proxies}")
        return proxies
    else:
        time.sleep(1)
        print('切换代理失败，重新尝试。。。')
        change_proxy(retry_count - 1)


if __name__ == '__main__':
    change_proxy(1)
    for i in range(0, 35082):
        data = spider(i)
        if data is not None:
            save_data('武汉中心医院1', data)
            print(f'第{i}页保存成功~~~~~~~~~~~~~~~~~~~~~~~~~~~')

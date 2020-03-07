# -*- coding: utf-8 -*-
import csv
import time
import re
import os
import sys
import requests
from lxml import html
from constants import proxy_url
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

"""
爬不同的微博换个id就行，40行，cookie貌似不用换
"""
proxy = {}

etree = html.etree

total_page = 1

# 过期了就换一下
cookie = '_T_WM=24942942014; _ga=GA1.2.852180565.1582702609; ALF=1585704328; WEIBOCN_FROM=1110005030; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZffgVwD82S9myNPVJt_eEnoefx53PouFijK-aVb_1g-D8.; SUB=_2A25zWBDwDeRhGeVI7lER9CvFyD6IHXVQorC4rDV6PUJbktANLWb8kW1NTAX_rCCldEMhGPVde7CQFgHTGj32A3uI; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0TPlxq9jgirh_U; SSOLoginState=1583112352; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4467076221310347%26luicode%3D20000061%26lfid%3D4467076221310347%26uicode%3D20000061%26fid%3D4467076221310347; XSRF-TOKEN=f9955a'

header = {
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://m.weibo.cn/status/It1D4rfo3',
    'mweibo-pwa': '1',
    'x-xsrf-token': 'b7fa37',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'cookie1': cookie,
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'http://gl.sach.gov.cn/?from=singlemessage&isappinstalled=0',
    'User-Agent':  ua.random,
}

url = 'https://m.weibo.cn/api/statuses/repostTimeline'


def spider(page, wb_id):
    param = {
        # 这个id要抓包获取，代表那条微博
        'id': str(wb_id),
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
    print(wb_id)
    print(ret)
    ok = ret['ok']

    global total_page
    if ok == 0 and total_page == 1:
        total_page += 1
        print(f"总页数改为{total_page}")

    if ok == 1:
        total_page = ret['data']['max']
        print(f"###########################总页数{total_page}###########################")

        data = ret['data']['data']
        for d in data:
            html = d['text']
            root = etree.HTML(html)
            text = root.xpath("string(/)")
            # if '//<a' in html:
            #     forward_user_name = d['user']['screen_name']  # 转发人昵称
            #     p = re.compile(r'//@(.*?)[:：]', re.S)
            #     forwarded_user_names = p.findall(text)  # 被转发人昵称列表
            #     forwarded_user_name = forwarded_user_names[0] if forwarded_user_names else ''  # 被转发人昵称
            # else:
            #     forward_user_name = d['user']['screen_name']  # 转发人昵称
            #     forwarded_user_name = d['retweeted_status']['user']['screen_name']  # 被转发人昵称
            #     forwarded_user_names = [forwarded_user_name]

            created_at = d['created_at']  # 创建时间

            # 用户信息
            user_id = d['user']['id']  # 用户id
            user_name = d['user']['screen_name']  # 用户id

            gender = '女' if d['user']['gender'] == 'f' else '男'  # 性别

            follow_count = d['user']['follow_count']  # 关注

            followers_count = d['user']['followers_count']  # 粉丝

            verified = d['user']['verified']  # 是否认证

            try:
                verified_type = d['user']['verified_type']  # 认证类型
            except:
                verified_type = ''
            try:
                verified_type_ext = d['user']['verified_type_ext']  # 认证类型的什么东东
            except:
                verified_type_ext = ''
            try:
                verified_reason = d['user']['verified_reason']  # 认证原因
            except:
                verified_reason = ''

            need = [wb_id, text, created_at,
                    user_id, user_name, gender, follow_count, followers_count, verified, verified_type, verified_type_ext, verified_reason]
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
            c.writerow(['wb_id', '转发内容', '转发时间',
                    'user_id', 'user_name', '性别', '关注', '粉丝', '是否认证', '认证类别', 'verified_type_ext', 'verified_reason'])
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

    csv_name = '《双黄连对新型冠状病毒不具针对性》的转发'

    with open('1.txt', 'r') as f:
        content = f.read().splitlines()
        wei_id_list = content

    for wei_id in wei_id_list:
        data = spider(page=1, wb_id=wei_id)
        if data is not None:
            save_data(csv_name, data)
            print(f'{wei_id}第1页保存成功~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        for i in range(2, total_page+1):
            data = spider(page=i, wb_id=wei_id)
            if data is not None:
                save_data(csv_name, data)
                print(f'总页数{total_page}，{wei_id}第{i}页保存成功~~~~~~~~~~~~~~~~~~~~~~~~~~~')

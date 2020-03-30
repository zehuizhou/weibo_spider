# -*- coding: utf-8 -*-
import csv
import random
import time
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

csv_name = '评论2'

# 过期了就换一下
cookie = '_ga=GA1.2.852180565.1582702609; _T_WM=73519821653; ALF=1586567249; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfx9sFLhxylFwW9xIYaJQRN7GBUNu2KoH9zBLGoDwWNGI.; SUB=_2A25zbnFYDeRhGeVI7lER9CvFyD6IHXVQkR8QrDV6PUJbktANLXPTkW1NTAX_rI1ydt90vkSc50P2r0bhDS3tfIrI; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0A05ytqQN9_yCf; WEIBOCN_FROM=1110005030; MLOGIN=1; M_WEIBOCN_PARAMS=uicode%3D20000061%26fid%3D4467107636950632%26oid%3D4467107636950632; XSRF-TOKEN=12370a'

header = {
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://m.weibo.cn/status/IscD7sd2K',
    'mweibo-pwa': '1',
    'x-xsrf-token': '3360ad',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'cookie': cookie,
    'accept': 'application/json, text/plain, */*',
    'Referer': 'https://m.weibo.cn/status/IscD7sd2K',
    'User-Agent':  ua.random,
}


def spider(wb_id):
    """
    传入微博id
    :param wb_id:
    :return:
    """
    max_id = ''

    while True:
        if max_id == '':
            url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(wb_id, wb_id)
        else:
            url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0&max_id={}".format(str(wb_id), str(wb_id), str(max_id))

        def get_ret(count):
            # noinspection PyBroadException
            try:
                ret = requests.get(url=url, headers=header, proxies=proxy, timeout=6).json()
                time.sleep(random.uniform(6, 8.5))
                print(ret)
                return ret
            except Exception:
                # change_proxy(3)
                time.sleep(3)
                return get_ret(count - 1)

        ret = get_ret(3)

        ok = ret['ok']
        if ok == 0 or max_id == 0:
            break

        if ok == 1:
            max_id = ret['data']['max_id']
            print(f"###########################max_id改为{max_id}###########################")

            max_id_type = ret['data']['max_id_type']
            print(f"###########################max_id_type改为{max_id_type}###########################")

            total_page = ret['data']['max']
            print(f"###########################总页数{total_page}###########################")

            data = ret['data']['data']
            for d in data:
                html = d['text']
                root = etree.HTML(html)
                text = root.xpath("string(/)")

                created_at = d['created_at']  # 创建时间
                time_list = created_at.split(' ')
                week = time_list[0]
                month_dict = {
                    'Jan': '01',
                    'Feb': '02',
                    'Mar': '03',
                    'Apr': '04',
                    'May': '05',
                    'Jun': '06',
                    'Jul': '07',
                    'Aug': '08',
                    'Sept': '09',
                    'Oct': '10',
                    'Nov': '11',
                    'Dec': '12',
                }
                created_at_new = time_list[5] + '-' + month_dict[time_list[1]] + '-' + time_list[2]+' '+time_list[3]

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
                    verified_type_ext = d['user']['verified_type_ext']  # verified_type_ext
                except:
                    verified_type_ext = ''
                try:
                    verified_reason = d['user']['verified_reason']  # 认证原因
                except:
                    verified_reason = ''

                need = [wb_id, text, created_at, created_at_new, week,
                        user_id, user_name, gender, follow_count, followers_count, verified, verified_type, verified_type_ext, verified_reason]
                print(need)

                save_data(filename=csv_name, data=[need])
                print(f'max_id {max_id} 保存成功')


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
            c.writerow(['wb_id', '评论内容', '转发时间', 'created_at_new', 'week',
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
    """
    4466929533834665
    4466986551438138
    """
    # change_proxy(1)

    # with open('1.txt', 'r') as f:
    #     content = f.read().splitlines()
    #     wei_id_list = content
    wei_id_list = ['4467107636950632']
    for wei_id in wei_id_list:
        spider(wei_id)
        print(f'微博{wei_id}保存成功~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')



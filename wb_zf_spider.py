# -*- coding: utf-8 -*-
import time
import requests
from lxml import html
from constants import change_proxy, save_to_csv, app_cookie
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

"""
爬不同的微博换个id就行，40行，cookie貌似不用换
"""
proxy = {}

etree = html.etree

total_page = 1

header = {
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://m.weibo.cn/status/It1D4rfo3',
    'mweibo-pwa': '1',
    'x-xsrf-token': 'b7fa37',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'cookie1': app_cookie,
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
            item = {}
            html = d['text']
            root = etree.HTML(html)
            item['微博id'] = '`' + wb_id
            item['转发内容'] = root.xpath("string(/)")
            # if '//<a' in html:
            #     forward_user_name = d['user']['screen_name']  # 转发人昵称
            #     p = re.compile(r'//@(.*?)[:：]', re.S)
            #     forwarded_user_names = p.findall(text)  # 被转发人昵称列表
            #     forwarded_user_name = forwarded_user_names[0] if forwarded_user_names else ''  # 被转发人昵称
            # else:
            #     forward_user_name = d['user']['screen_name']  # 转发人昵称
            #     forwarded_user_name = d['retweeted_status']['user']['screen_name']  # 被转发人昵称
            #     forwarded_user_names = [forwarded_user_name]

            item['创建时间'] = d['created_at']  # 创建时间
            # 用户信息
            item['用户id'] = d['user']['id']
            item['用户昵称'] = d['user']['screen_name']
            item['性别'] = '女' if d['user']['gender'] == 'f' else '男'
            item['关注'] = d['user']['follow_count']
            item['粉丝'] = d['user']['followers_count']
            item['是否认证'] = d['user']['verified']
            item['认证类型'] = d['user']['verified_type'] if 'verified_type' in d['user'] else ''
            item['认证详情'] = d['user']['verified_reason'] if 'verified_reason' in d['user'] else ''
            item['verified_type_ext'] = d['user']['verified_type_ext'] if 'verified_type_ext' in d['user'] else ''

            print(item)
            need_list.append(item)
        return need_list


if __name__ == '__main__':
    change_proxy(1)

    csv_name = '《双黄连对新型冠状病毒不具针对性》的转发.csv'

    with open('1.txt', 'r') as f:
        content = f.read().splitlines()
        wei_id_list = content

    for wei_id in wei_id_list:
        data = spider(page=1, wb_id=wei_id)
        if data is not None:
            save_to_csv(csv_name, data)
            print(f'{wei_id}第1页保存成功~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        for i in range(2, total_page+1):
            data = spider(page=i, wb_id=wei_id)
            if data is not None:
                save_to_csv(csv_name, data)
                print(f'总页数{total_page}，{wei_id}第{i}页保存成功~~~~~~~~~~~~~~~~~~~~~~~~~~~')

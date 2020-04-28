#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-02-04 17:14
#  @Author  : July
import re
import os
import csv
import time
import requests
from retrying import retry
from constants import proxy_url, app_header, app_url
from lxml import html
import random

etree = html.etree

proxy = {}
# '4490719299787262'
since_id = None


# @retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000)
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


def save_data(filename, data):
    if os.path.isfile(filename):
        is_exist = True
    else:
        is_exist = False
    with open(filename, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            """need = [user_id, user_name, created_at, source,
                    content, reposts_count, comments_count, attitudes_count,
                    pics_url, video_url, retweeted_status, 'retweeted_content', retweeted_url,
                    topic_num, topics]"""
            c.writerow(['用户id', '昵称', '发表时间', '发布设备', 'scheme_url', '正文', '转发数', '评论数', '点赞数',
                        '图片链接', '视频链接', '是否转发', '转发内容', '转发链接', '话题数', '话题', '微博链接', 'since_id'])
        for line in data:
            c.writerow(line)


def spider(uid):
    global since_id
    app_param = {
        # 'uid': 2803301701,
        'type': 'uid',
        'value': uid,
        'containerid': '107603'+str(uid),
        'since_id': since_id
    }

    def get_ret(c):

        if c < 0:
            return
        try:
            ret = requests.get(url=app_url, headers=app_header, params=app_param, proxies=proxy, timeout=6).json()
            print(ret)
            a = ret['data']['cardlistInfo']['since_id']
            return ret
        except:
            time.sleep(random.uniform(1, 3))
            change_proxy(3)
            return get_ret(c - 1)

    ret = get_ret(3)

    since_id = ret['data']['cardlistInfo']['since_id']
    print(f'since_id改为 {since_id} ，上一次的数据还未保存，请使用前一个since_id')
    need_list = []
    cards = ret['data']['cards']
    for card in cards:
        if card['card_type'] == 9:
            user_id = card['mblog']['user']['id']  # 用户id
            user_name = card['mblog']['user']['screen_name']  # 用户名称
            created_at = card['mblog']['created_at']  # 发布时间
            source = card['mblog']['source']  # 发布工具
            scheme_url = card['scheme']
            wb_id = card['mblog']['id']
            wb_url = 'https://m.weibo.cn/detail/' + str(wb_id)

            reposts_count = card['mblog']['reposts_count']  # 转发数
            comments_count = card['mblog']['comments_count']  # 评论数
            attitudes_count = card['mblog']['attitudes_count']  # 点赞数
            app_detail_url = 'https://m.weibo.cn/statuses/extend?id=' + str(wb_id)

            html = card['mblog']['text']
            root = etree.HTML(html)
            content = root.xpath("string(//*)")  # 微博内容

            pics_url = ''
            if card['mblog']['pic_num'] != 0:
                try:
                    pics = card['mblog']['pics']
                    for pic in pics:
                        tupian = pic['url']
                        pics_url = pics_url + tupian + os.linesep + '   '  # 图片链接
                except:
                    pics_url = ''

            try:
                video_url = card['mblog']['page_info']['media_info']['stream_url']  # 视频链接
            except KeyError:
                video_url = ''

            # 转发内容
            retweeted_status = '否'
            retweeted_url = ''
            retweeted_content = ''
            if 'retweeted_status' in card['mblog']:
                retweeted_status = '是'
                # retweeted_url = 'https://m.weibo.cn/detail/' + str(card['mblog']['retweeted_status']['id'])
                retweeted_url = 'https://m.weibo.cn/statuses/extend?id=' + str(card['mblog']['retweeted_status']['id'])

                def get_re_detail_ret(c):
                    if c < 0:
                        return
                    try:
                        re_detail_ret = requests.get(url=retweeted_url, headers=app_header, proxies=proxy, timeout=6).json()
                        print(f'########################re_detail_ret{re_detail_ret}')
                        time.sleep(random.uniform(0.3, 1.2))
                        return re_detail_ret
                    except:
                        change_proxy(3)
                        return get_ret(c - 1)

                re_detail_ret = get_re_detail_ret(2)
                try:
                    html = re_detail_ret['data']['longTextContent']  # 正文
                    root = etree.HTML(html)
                    retweeted_content = root.xpath("string(//*)")
                except:
                    print(f'获取微博详情失败，详情内容为detail_ret{re_detail_ret}')
                    html = card['mblog']['retweeted_status']['text']
                    root = etree.HTML(html)
                    retweeted_content = root.xpath("string(//*)")

            if '全文' in content:
                # 微博详情页
                def get_detail_ret(c):
                    if c < 0:
                        return
                    try:
                        detail_ret = requests.get(url=app_detail_url, headers=app_header, proxies=proxy, timeout=6).json()
                        print(detail_ret)
                        time.sleep(random.uniform(0.3, 1.2))
                        return detail_ret
                    except:
                        change_proxy(3)
                        return get_ret(c - 1)

                detail_ret = get_detail_ret(2)
                try:
                    html = detail_ret['data']['longTextContent']  # 正文
                    root = etree.HTML(html)
                    content = root.xpath("string(//*)")
                except:
                    print(f'获取微博详情失败，详情内容为detail_ret{detail_ret}')

            topic_num = int(content.count('#') / 2)  # 话题数
            p = re.compile(r'[#](.*?)[#]', re.S)
            topics = '\n'.join(p.findall(content))  # 话题

            need = [user_id, user_name, created_at, source, scheme_url,
                    content, reposts_count, comments_count, attitudes_count,
                    pics_url, video_url, retweeted_status, retweeted_content, retweeted_url,
                    topic_num, topics,
                    wb_url, since_id]
            print(need)
            need_list.append(need)

    return need_list


if __name__ == '__main__':
    change_proxy(1)
    while True:
        data = spider(1265357020)
        save_data('素走世界.csv', data)
        print("########################存储成功########################")

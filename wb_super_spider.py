#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-02-04 17:14
#  @Author  : July
import re
import os
import time
import requests
from constants import app_header, save_to_csv, change_proxy
from lxml import html
import random

etree = html.etree

# 第几页的标识，获取最新的就用None
since_id = None


def spider():
    global since_id
    url = 'https://m.weibo.cn/api/container/getIndex?current_page[]=6&current_page[]=6&' \
          'since_id={}&jumpfrom=weibocom&sudaref=weibo.com&' \
          'containerid=100808a518bfa8e3872f9d0b2999bc774480ae_-_feed'.format(since_id)

    def get_ret(c):

        if c < 0:
            return
        try:
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())
            res = requests.get(url=url, headers=app_header, proxies=proxy, timeout=6).json()
            time.sleep(random.uniform(1, 3.5))
            print(res)
            a = res['data']['pageInfo']['since_id']
            return res
        except:
            time.sleep(random.uniform(1, 3))
            change_proxy(3)
            return get_ret(c - 1)

    res = get_ret(3)

    since_id = res['data']['pageInfo']['since_id']
    print(f'since_id改为 {since_id} ，上一次的数据还未保存，请使用前一个since_id')

    need_list = []
    cards = res['data']['cards'][0]['card_group']
    for card in cards:
        if card['card_type'] == '9':
            item = {}
            item['微博id'] = '`' + card['mblog']['id']
            item['发布时间'] = card['mblog']['created_at']
            text = card['mblog']['text']
            ht = etree.HTML(text)
            item['内容'] = ht.xpath("string(//*)")
            item['来源'] = card['mblog']['source']
            item['转发数'] = card['mblog']['reposts_count']  # 转发数
            item['评论数'] = card['mblog']['comments_count']  # 评论数
            item['点赞数'] = card['mblog']['attitudes_count']  # 点赞数
            item['微博链接'] = card['scheme']
            item['scheme_url'] = card['scheme']
            item['since_id'] = '`' + str(res['data']['pageInfo']['since_id'])
            print(item)
            need_list.append(item)

    return need_list


if __name__ == '__main__':
    change_proxy(1)
    while True:
        data = spider()
        save_to_csv('微博超话', data)
        print("########################存储成功########################")

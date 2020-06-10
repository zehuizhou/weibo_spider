#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-02-04 17:14
#  @Author  : July
import re
import os
import time
import requests
from constants import app_header, app_url, save_to_csv, change_proxy
from lxml import html
import random

etree = html.etree

proxy = {}

# 第几页的标识，获取最新的就用None
since_id = None


def spider(uid):
    global since_id
    app_param = {        # 'uid': 2803301701,

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
            item = {}
            """
            ['用户id', '昵称', '发表时间', '发布设备', 'scheme_url', '正文', '转发数', '评论数', '点赞数',
                        '图片链接', '视频链接', '是否转发', '转发内容', '转发链接', '话题数', '话题', '微博链接', 'since_id']
            """
            item['用户id'] = card['mblog']['user']['id']
            item['用户名称'] = card['mblog']['user']['screen_name']  # 用户名称
            item['发布时间'] = card['mblog']['created_at']  # 发布时间
            item['发布工具'] = card['mblog']['source']  # 发布工具
            item['scheme_url'] = card['scheme']
            wb_id = card['mblog']['id']
            item['微博id'] = '`' + card['mblog']['id']
            item['微博链接'] = 'https://m.weibo.cn/detail/' + str(wb_id)

            item['转发数'] = card['mblog']['reposts_count']  # 转发数
            item['评论数'] = card['mblog']['comments_count']  # 评论数
            item['点赞数'] = card['mblog']['attitudes_count']  # 点赞数
            app_detail_url = 'https://m.weibo.cn/statuses/extend?id=' + str(wb_id)

            html = card['mblog']['text']
            root = etree.HTML(html)
            content = root.xpath("string(//*)")  # 微博内容
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
            item['微博内容'] = content
            item['话题数'] = int(content.count('#') / 2)  # 话题数
            p = re.compile(r'[#](.*?)[#]', re.S)
            item['话题'] = '\n'.join(p.findall(content))  # 话题

            pics_url = ''
            if card['mblog']['pic_num'] != 0:
                try:
                    pics = card['mblog']['pics']
                    for pic in pics:
                        tupian = pic['url']
                        pics_url = pics_url + tupian + os.linesep + '   '  # 图片链接
                except:
                    pics_url = ''
            item['图片链接'] = pics_url
            try:
                video_url = card['mblog']['page_info']['media_info']['stream_url']  # 视频链接
            except KeyError:
                video_url = ''
            item['视频链接'] = video_url


            # 转发内容
            retweeted_status = '否'
            retweeted_url = ''
            retweeted_content = ''
            if 'retweeted_status' in card['mblog']:
                retweeted_status = '是'
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
            item['是否转发'] = retweeted_status
            item['转发链接'] = retweeted_url
            item['转发内容'] = retweeted_content
            item['since_id'] = '`' + str(since_id)  # 防止Excel科学计数

            print(item)
            need_list.append(item)

    return need_list


if __name__ == '__main__':
    change_proxy(1)
    while True:
        data = spider(5022145652)
        save_to_csv('pxxh', data)
        print("########################存储成功########################")

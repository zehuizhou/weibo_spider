# -*- coding: utf-8 -*-
import time
import requests
from lxml import html
from constants import change_proxy, save_to_csv, app_cookie, app_header_cookie
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

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


def spider(page, wb_id):
    url = 'https://m.weibo.cn/api/attitudes/show'

    param = {
        # 这个id要抓包获取，代表那条微博
        'id': str(wb_id),
        'page': page
    }
    need_list = []

    def get_ret(count):
        # noinspection PyBroadException
        try:
            if count<0:
                return
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())
            ret = requests.get(url=url, params=param, headers=app_header_cookie, proxies=proxy, timeout=6).json()
            time.sleep(1)
            print(ret)
            return ret
        except Exception:
            time.sleep(1)
            change_proxy(3)
            return get_ret(count - 1)
    ret = get_ret(2)

    ok = ret['ok']
    if ok == 0:
        return
    if ok == 1:
        max = ret['data']['max']

        if page == 1:
            global total_page
            total_page = max
            if total_page > 50:
                total_page = 50
            print(f"###########################总页数{total_page}###########################")
        data = ret['data']['data']
        if data is not None:
            for d in data:
                item = {}

                item['微博id'] = '`' + wb_id
                item['创建时间'] = d['created_at']  # 创建时间
                item['点赞id'] = d['id']
                item['来源'] = d['source']
                # 用户信息
                item['用户id'] = d['user']['id']
                item['用户昵称'] = d['user']['screen_name']
                item['follow_me'] = d['user']['follow_me']
                item['粉丝'] = d['user']['followers_count']
                item['following'] = d['user']['following']
                item['remark'] = d['user']['remark']
                item['profile_image_url'] = d['user']['profile_image_url']
                item['profile_url'] = d['user']['profile_url']

                item['是否认证'] = d['user']['verified']
                item['认证类型'] = d['user']['verified_type'] if 'verified_type' in d['user'] else ''
                item['认证详情'] = d['user']['verified_reason'] if 'verified_reason' in d['user'] else ''
                item['verified_type_ext'] = d['user']['verified_type_ext'] if 'verified_type_ext' in d['user'] else ''

                print(item)
                need_list.append(item)
            return need_list


if __name__ == '__main__':
    change_proxy(1)

    csv_name = '毛不易点赞.csv'

    with open('ids', 'r') as f:
        content = f.read().splitlines()
        ids = ['4509979665275482']

    for wei_id in ids:
        data = spider(page=1, wb_id=wei_id)
        if data is not None:
            save_to_csv(csv_name, data)
            print(f'{wei_id}第1页保存成功~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        for i in range(2, total_page+1):
            data = spider(page=i, wb_id=wei_id)
            if data is not None:
                save_to_csv(csv_name, data)
                print(f'总页数{total_page}，{wei_id}第{i}页保存成功~~~~~~~~~~~~~~~~~~~~~~~~~~~')

        print(f'{wei_id} 保存成功'.center(70, '-'))
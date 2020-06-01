# -*- coding: utf-8 -*-
import random
import time
import requests
from lxml import html
from constants import save_to_csv, change_proxy, app_cookie, app_header_cookie
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

etree = html.etree

cname = '毛不易评论.csv'

header = {
    'x-requested-with': 'XMLHttpRequest',
    'referer': 'https://m.weibo.cn/status/IscD7sd2K',
    'mweibo-pwa': '1',
    'x-xsrf-token': '3360ad',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'cookie': app_cookie,
    'accept': 'application/json, text/plain, */*',
    'Referer': 'https://m.weibo.cn/status/IscD7sd2K',
    'User-Agent':  ua.random,
}


def spider(wb_id):
    max_id = ''
    max_id_type = 0
    while True:
        if max_id == '':
            url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(wb_id, wb_id)
        else:
            url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type={}&max_id={}".format(str(wb_id), str(wb_id), str(max_id_type), str(max_id))

        def get_ret(count):
            try:
                with open('pro.txt', 'r') as f:
                    proxy = eval(f.read())
                ret = requests.get(url=url, headers=header, proxies=proxy, timeout=6).json()
                time.sleep(random.uniform(0.2, 1.5))
                print(ret)
                return ret
            except Exception as e:
                print(e)
                change_proxy(3)
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
                item = {}

                h = d['text']
                root = etree.HTML(h)
                item['微博id'] = '`' + wb_id
                item['bid'] = '`' + d['bid']
                item['评论id'] = '`' + d['id']
                item['评论内容'] = root.xpath("string(/)")
                item['点赞'] = d['like_count']
                created_at = d['created_at']  # 创建时间
                time_list = created_at.split(' ')
                month_dict = {
                    'Jan': '01',
                    'Feb': '02',
                    'Mar': '03',
                    'Apr': '04',
                    'May': '05',
                    'Jun': '06',
                    'Jul': '07',
                    'Aug': '08',
                    'Sep': '09',
                    'Oct': '10',
                    'Nov': '11',
                    'Dec': '12',
                }
                item['评论时间'] = time_list[5] + '-' + month_dict[time_list[1]] + '-' + time_list[2]+' '+time_list[3]
                item['星期'] = time_list[0]
                # 用户信息
                item['用户id'] = d['user']['id']
                item['用户名'] = d['user']['screen_name']
                item['性别'] = '女' if d['user']['gender'] == 'f' else '男'
                item['关注'] = d['user']['follow_count']
                item['粉丝'] = d['user']['followers_count']
                item['是否认证'] = d['user']['verified']
                item['认证类型'] = d['user']['verified_type'] if 'verified_type' in d['user'] else ''
                item['认证详情'] = d['user']['verified_reason'] if 'verified_reason' in d['user'] else ''
                item['verified_type_ext'] = d['user']['verified_type_ext'] if 'verified_type_ext' in d['user'] else ''
                print(item)
                csv_name = cname
                save_to_csv(file_name=csv_name, list_dict=[item])
            print(str(max_id)+' 保存成功')


if __name__ == '__main__':
    change_proxy(1)

    with open('ids', 'r') as f:
        content = f.read().splitlines()
        ids = content

    for i in ids:
        spider(i)
        print(f'{i} 保存成功'.center(70, '-'))

import re
import time
import requests
from lxml import html
import os
import datetime
import string
# from retrying import retry
from constants import *
# import pysnooper
import sys
import csv

etree = html.etree

total_page = 50


def get_path(file_name):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    return path


def save_data(filename, data):
    # now = datetime.datetime.now().replace()
    # now = str(now)[0:10].replace('-', '').replace(' ', '').replace(':', '')
    path = get_path(filename + '.csv')
    if os.path.isfile(path):
        is_exist = True
    else:
        is_exist = False
    with open(path, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            c.writerow(['微博id', '微博内容', '转发内容', '时间', '评论数', '转发数', '点赞数', '微博链接', '用户名', '用户个人主页链接',
                        '表情数', '所有图片数', '图片链接（包括转发）', '视频链接（包括转发）', '@数', '主题数', '主题', '地点', '用户id',
                        '性别', '关注', '粉丝', '是否认证', '认证类型', '认证ext', '认证详情',
                        '所在地'])
        for line in data:
            c.writerow(line)


# @retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000)
def change_proxy(retry_count):
    if retry_count < 0:
        return

    result = requests.get(proxy_url).json()
    if result['msg'] == 'ok':
        ip = result['obj'][0]['ip']
        port = result['obj'][0]['port']
        proxies = {"http": "http://" + ip + ":" + port, "https": "http://" + ip + ":" + port}

        with open('pro.txt', 'w') as f:
            f.write(str(proxies))

        print(f"代理ip为更改为：{proxies}")
        return proxies
    else:
        time.sleep(1)
        print('切换代理失败，重新尝试。。。')
        change_proxy(retry_count - 1)


class WbSpider:
    def __init__(self, keyword, start_time, end_time, page):
        self.keyword = keyword
        self.start_time = start_time
        self.end_time = end_time
        self.page = page

    def web_requests(self, retry_count):
        param = {
            'scope': 'ori',
            'q': self.keyword,
            'typeall': '1',
            'suball': '1',
            'timescope': 'custom:' + self.start_time + ':' + self.end_time,
            'Refer': 'g',
            'page': self.page
        }
        if retry_count < 0:
            return
        try:
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())
            res_web = requests.get(url=web_url, headers=web_header, params=param, proxies=proxy,
                                   timeout=6).content.decode()
            root_web = etree.HTML(res_web)

            table_item = root_web.xpath("//div[@class='card-wrap']")
            assert table_item
            return root_web
        except:
            change_proxy(3)
            return self.web_requests(retry_count - 1)

    def get_web_data(self):
        web_html = self.web_requests(3)

        if self.page == 1:
            global total_page
            total_page = len(web_html.xpath("//ul[@class='s-scroll']/li"))
            if total_page == 0:
                total_page = 1
            print(f'总页数:{total_page}')

        table_item = web_html.xpath("//div[@class='card-wrap']")
        web_data_list = []
        for n in range(0, len(table_item)):
            try:
                # 微博数据：微博内容，定位，转发数，评论数，点赞数，发布时间，该微博的链接，图片及视频的个数及链接，话题数，@的个数，表情数
                user_name = table_item[n].xpath(".//div[@class='info']/div[2]/a/text()")[0]  # 用户名
                user_url = 'https:' + table_item[n].xpath(".//div[@class='info']/div[2]/a/@href")[0]  # 用户个人主页地址
                user_id = re.findall('.*weibo.com/(.*)refer_flag', user_url)[0].replace('?', '')
                content = table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content'])") \
                    if table_item[n].xpath(
                    "string(.//div[@class='content']/p[@node-type='feed_list_content_full'])") == '' \
                    else table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content_full'])")
                content = ''.join([i for i in content if i not in string.whitespace])  # 微博内容

                forword_content = table_item[n].xpath("string(.//div[@class='content']/div[@class='card-comment'])")
                forword_content = ''.join([i for i in forword_content if i not in string.whitespace])  # 转发内容

                date_time = table_item[n].xpath("string(.//div[@class='content']/p[@class='from']/a[1])")  # 发微博的时间
                date_time = ''.join([i for i in date_time if i not in string.whitespace])  # 发微博的时间
                comment_num = 0 \
                    if table_item[n].xpath("string (.//div[@class='card-act']/ul/li[3])").replace('评论', '') == ' ' \
                    else table_item[n].xpath("string(.//div[@class='card-act']/ul/li[3])").replace('评论 ', '')  # 评论数
                forward_num = 0 \
                    if table_item[n].xpath("string(.//div[@class='card-act']/ul/li[2])").replace('转发', '') == '  ' \
                    else table_item[n].xpath("string(.//div[@class='card-act']/ul/li[2])").replace('转发 ', '')  # 转发数
                up_num = 0 if table_item[n].xpath("string(.//div[@class='card-act']/ul/li[4])") == ' ' \
                    else table_item[n].xpath("string(.//div[@class='card-act']/ul/li[4])").replace(' ', '')  # 点赞数
                wb_url = 'https:' + table_item[n].xpath(".//div[@class='content']/p[@class='from']/a[1]/@href")[0]  # 微博地址
                wb_id = re.findall('.*/(.*)\?refer_flag', wb_url)[0]

                # 新增的
                face_num = len(table_item[n].xpath(".//div[@class='content']/p//img[@class='face']"))  # 表情数
                img_num = len(
                    table_item[n].xpath(".//div[@class='content']//img[@action-type='fl_pics']/@src"))  # 图片数，包括转发内容
                if img_num > 0:
                    img_urls = 'https:' + '\nhttps:'.join(
                        table_item[n].xpath(".//div[@class='content']//img[@action-type='fl_pics']/@src"))  # 图片地址
                else:
                    img_urls = ''

                zm = table_item[n].xpath(".//div[@class='content']//p//a/i")
                video_url = ''
                for z in zm:
                    if z.xpath("./text()")[0] == 'L':
                        video_url = z.xpath("./../@href")[0]
                        break

                aite_num = content.count('@')  # @数
                topic_num = content.count('#') / 2  # 话题数
                p = re.compile(r'[#](.*?)[#]', re.S)
                topics = '\n'.join(p.findall(content))  # 话题

                try:
                    em = table_item[n].xpath(".//div[@class='content']/p[@node-type='feed_list_content']/a/i/text()")[0] \
                        if table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content_full'])") == '' \
                        else table_item[n].xpath(".//div[@class='content']/p[@node-type='feed_list_content_full']/a/i/text()")[0]
                except:
                    em = ''

                if em == '2':
                    place = table_item[n].xpath(".//div[@class='content']/p[@node-type='feed_list_content']/a/i/../text()")[0].replace('2', '')  \
                        if table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content_full'])") == '' \
                        else table_item[n].xpath(".//div[@class='content']/p[@node-type='feed_list_content_full']/a/i/../text()")[0].replace('2', '')
                else:
                    place = ''

                web_data = [wb_id, content, forword_content, date_time, comment_num, forward_num, up_num, wb_url,
                            user_name, user_url,
                            face_num, img_num, img_urls, video_url, aite_num, topic_num, topics, place, user_id]

                web_data_list.append(web_data)
            except IndexError:
                break
        return web_data_list

    # @pysnooper.snoop("./log")
    def app_requests_userinfo(self, user_id, retry_count):
        app_param_userinfo = {
            'jumpfrom': 'weibocom',
            'sudaref': 'www.weibo.com',
            'type': 'uid',
            'value': user_id,
            'containerid': '100505' + user_id
        }

        if retry_count < 0:
            print('获取用户数据失败')
            assert 0
        try:
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())

            app_json = requests.get(url=app_url, headers=app_header, params=app_param_userinfo, proxies=proxy,
                                    timeout=6).json()
            if 'msg' in app_json:
                if app_json['msg'] == '这里还没有内容':
                    print('❤️这里还没有内容，使用带cookie的header')
                    app_json = requests.get(url=app_url, headers=app_header_cookie, params=app_param_userinfo,
                                            proxies=proxy,
                                            timeout=6).json()
                    if 'msg' in app_json:
                        print('❤' + app_json['msg'] + '默认赋值为['', '', '', '', '']')
                        return ['', '', '', '', '', '', '']

            assert app_json['data']['userInfo']
        except:
            change_proxy(3)
            return self.app_requests_userinfo(user_id, retry_count - 1)
        # 微博账号名称，具体认证信息，粉丝数，微博内容，定位，转发数，评论数，点赞数，发布时间，该微博的链接，图片及视频的个数及链接，话题数，@的个数，表情数。
        try:
            gender = '女' if app_json['data']['userInfo']['gender'] == 'f' else '男'  # 性别
        except:
            gender = ''
        try:
            follow_count = app_json['data']['userInfo']['follow_count']  # 关注
        except:
            follow_count = ''
        try:
            followers_count = app_json['data']['userInfo']['followers_count']  # 粉丝
        except:
            followers_count = ''
        try:
            verified = app_json['data']['userInfo']['verified']  # 是否认证
        except:
            verified = ''
        try:
            verified_type = app_json['data']['userInfo']['verified_type']  # 认证类型
        except:
            verified_type = ''
        try:
            verified_type_ext = app_json['data']['userInfo']['verified_type_ext']  # 认证类型的什么东东
        except:
            verified_type_ext = ''
        try:
            verified_reason = app_json['data']['userInfo']['verified_reason']  # 认证原因
        except:
            verified_reason = ''

        app_data = [gender, follow_count, followers_count,
                    verified, verified_type, verified_type_ext, verified_reason]
        return app_data

    def app_requests_cards(self, user_id, retry_count):
        app_param_cardsinfo = {
            'jumpfrom': 'weibocom',
            'sudaref': 'www.weibo.com',
            'type': 'uid',
            'value': user_id,
            'containerid': '230283' + user_id
        }

        if retry_count < 0:
            print('获取用户数据失败')
            assert 0

        try:
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())

            app_json = requests.get(url=app_url, headers=app_header, params=app_param_cardsinfo, proxies=proxy,
                                    timeout=6).json()
            print(app_json)
            if 'msg' in app_json:
                if app_json['msg'] == '这里还没有内容':
                    print('❤️这里还没有内容，使用带cookie的header')
                    app_json = requests.get(url=app_url, headers=app_header, params=app_param_cardsinfo,
                                            proxies=proxy, timeout=6).json()
                    if 'msg' in app_json:
                        print('❤' + app_json['msg'])
                        return ['']

            assert app_json['data']['cards']
        except:
            change_proxy(3)
            return self.app_requests_userinfo(user_id, retry_count - 1)

        place = ''
        card_group = app_json['data']['cards'][0]['card_group'][0]
        print(card_group)
        if 'item_name' in card_group:
            if card_group['item_name'] == '所在地':
                place = card_group['item_content']
                print(place)

        # 信息、公司、学校、感情状况、注册时间 这些需要登录
        # card_group = app_json['data']['cards'][1]['card_group']
        # print(card_group)
        # info, company, school, situation, register_time = '', '', '', '', ''
        # for card in card_group:
        #     if 'item_name' in card:
        #         if card['item_name'] == '信息':
        #             info = card['item_content']
        #         if card['item_name'] == '公司':
        #             company = card['item_content']
        #         if card['item_name'] == '学校':
        #             school = card['item_content']
        #         if card['item_name'] == '感情状况':
        #             situation = card['item_content']
        #         if card['item_name'] == '注册时间':
        #             register_time = card['item_content']

        # app_data_cardsinfo = [info, company, school, situation, register_time]

        app_data_cardsinfo = [place]
        return app_data_cardsinfo

    def start(self):
        all_data_list = []
        need = self.get_web_data()
        for n in need:
            web_data = n
            user_id = n[-1]
            app_data_userinfo = self.app_requests_userinfo(user_id=user_id, retry_count=2)
            app_data_cardsinfo = self.app_requests_cards(user_id=user_id, retry_count=2)
            print(web_data)
            print(app_data_userinfo)
            print(app_data_cardsinfo)
            print('-----------------------------------------')
            all_data = web_data + app_data_userinfo + app_data_cardsinfo
            all_data_list.append(all_data)
        return all_data_list


if __name__ == '__main__':
    change_proxy(1)

    date_list = ['2020-01-27-', '2020-01-28-',
                  '2020-01-29-', '2020-01-30-', '2020-01-31-', '2020-02-01-', '2020-02-02-', '2020-02-03-']

    # custom:2020-01-30-22:2020-01-30-23
    key = '#封城日记#'

    csv_name = '封城日记'

    for date in date_list:
        for num in range(0, 24):
            # 保存第一页数据，并修改总页数
            wb = WbSpider(keyword=key, start_time=date + str(num), end_time=date + str(num + 1), page=1)

            data = wb.start()
            save_data(csv_name, data)

            print('################################################')
            print(f"{date + str(num)}~{date + str(num + 1)}第1数据存储成功。。。。。。")
            print('################################################')

            # 保存剩下页数数据
            for i in range(2, total_page+1):
                wb = WbSpider(keyword=key, start_time=date+str(num), end_time=date+str(num+1), page=i)
                data = wb.start()
                save_data(csv_name, data)
                print('################################################')
                print(f"{date+str(num)}至{date+str(num+1)}第{i}页数据存储成功。。。。。。")
                print('################################################')

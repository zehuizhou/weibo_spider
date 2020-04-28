import re
import time
import requests
from lxml import html
import os
import datetime
import string
# from retrying import retry
from constants import change_proxy, save_to_csv, web_header, app_header, app_header_cookie, web_url, app_url
# import pysnooper
import sys
import csv

etree = html.etree

total_page = 1


class WbSpider:
    def __init__(self, keyword, start_time, end_time, page):
        self.keyword = keyword
        self.start_time = start_time
        self.end_time = end_time
        self.page = page

    def get_web_data(self, retry_count):
        param = {
            # 'scope': 'ori',  # 是否原创
            'q': self.keyword,
            'typeall': '1',  # 全部（和scope二选一）
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
            res_web = requests.get(url=web_url, headers=web_header, params=param, proxies=proxy, timeout=6).content.decode()
            root_web = etree.HTML(res_web)
            table_item = root_web.xpath("//div[@class='card-wrap']")
            assert table_item
        except Exception as e:
            print(e)
            change_proxy(3)
            return self.get_web_data(retry_count - 1)

        #######################################
        if self.page == 1:
            global total_page
            total_page = len(root_web.xpath("//ul[@class='s-scroll']/li"))
            if total_page == 0:
                total_page = 1
            print(f'总页数:{total_page}')

        table_item = root_web.xpath("//div[@class='card-wrap']")
        web_data_list = []
        for n in range(0, len(table_item)):
            try:
                web_item = {}
                user_url = 'https:' + table_item[n].xpath(".//div[@class='info']/div[2]/a/@href")[0]

                web_item['微博id'] = '`' + str(table_item[n].xpath("./@mid")[0])
                web_item['用户名'] = table_item[n].xpath(".//div[@class='info']/div[2]/a/text()")[0]

                web_item['个人主页链接'] = user_url
                web_item['用户id'] = re.findall('.*weibo.com/(.*)refer_flag', user_url)[0].replace('?', '')

                content = table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content'])") \
                    if table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content_full'])") == '' \
                    else table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content_full'])")
                web_item['内容'] = ''.join([c for c in content if c not in string.whitespace])  # 微博内容

                forward_content = table_item[n].xpath("string(.//div[@class='content']/div[@class='card-comment'])")
                web_item['转发内容'] = ''.join([c for c in forward_content if c not in string.whitespace])  # 转发内容

                date_time = table_item[n].xpath("string(.//div[@class='content']/p[@class='from']/a[1])")  # 发微博的时间
                date_time = ''.join([t for t in date_time if t not in string.whitespace])  # 发微博的时间
                if len(date_time) == 11:
                    date_time = str(datetime.datetime.now())[0:4] + '-' + date_time[0:2] + '-' + date_time[3:5] + ' ' + date_time[-5:]
                else:
                    date_time = date_time[0:4] + '-' + date_time[5:7] + '-' + date_time[8:10] + ' ' + date_time[-5:]
                web_item['时间'] = date_time
                web_item['评论数'] = 0 \
                    if table_item[n].xpath("string (.//div[@class='card-act']/ul/li[3])").replace('评论', '') == ' ' \
                    else table_item[n].xpath("string(.//div[@class='card-act']/ul/li[3])").replace('评论 ', '')  # 评论数
                web_item['转发数'] = 0 \
                    if table_item[n].xpath("string(.//div[@class='card-act']/ul/li[2])").replace('转发', '') == '  ' \
                    else table_item[n].xpath("string(.//div[@class='card-act']/ul/li[2])").replace('转发 ', '')  # 转发数
                web_item['点赞数'] = 0 if table_item[n].xpath("string(.//div[@class='card-act']/ul/li[4])") == ' ' \
                    else table_item[n].xpath("string(.//div[@class='card-act']/ul/li[4])").replace(' ', '')  # 点赞数
                web_item['微博链接'] = 'https:' + table_item[n].xpath(".//div[@class='content']/p[@class='from']/a[1]/@href")[0]  # 微博地址

                # 新增的
                web_item['表情数'] = len(table_item[n].xpath(".//div[@class='content']/p//img[@class='face']"))  # 表情数
                web_item['表情'] = '\n'.join(table_item[n].xpath(".//div[@class='content']/p//img[@class='face']/@title"))
                img_num = len(
                    table_item[n].xpath(".//div[@class='content']//img[@action-type='fl_pics']/@src"))  # 图片数，包括转发内容
                web_item['图片数'] = img_num
                web_item['图片链接'] = 'https:' + '\nhttps:'.join(table_item[n].xpath(".//div[@class='content']//img[@action-type='fl_pics']/@src")) if img_num else ''

                zm = table_item[n].xpath(".//div[@class='content']//p//a/i")
                video_url = ''
                for z in zm:
                    if z.xpath("./text()")[0] == 'L':
                        video_url = z.xpath("./../@href")[0]
                        break
                web_item['视频链接'] = video_url
                web_item['@数'] = content.count('@')
                web_item['@话题数'] = content.count('#') / 2
                p = re.compile(r'[#](.*?)[#]', re.S)
                web_item['@话题'] = '\n'.join(p.findall(content))

                try:
                    em = table_item[n].xpath(".//div[@class='content']/p[@node-type='feed_list_content']/a/i/text()")[0] \
                        if table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content_full'])") == '' \
                        else table_item[n].xpath(".//div[@class='content']/p[@node-type='feed_list_content_full']/a/i/text()")[0]
                except:
                    em = ''

                if em == '2':
                    location = table_item[n].xpath(".//div[@class='content']/p[@node-type='feed_list_content']/a/i/../text()")[0].replace('2', '')  \
                        if table_item[n].xpath("string(.//div[@class='content']/p[@node-type='feed_list_content_full'])") == '' \
                        else table_item[n].xpath(".//div[@class='content']/p[@node-type='feed_list_content_full']/a/i/../text()")[0].replace('2', '')
                else:
                    location = ''
                web_item['定位'] = location
                web_data_list.append(web_item)
            except IndexError:
                break
        return web_data_list

    def get_user_info(self, user_id, retry_count):
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

            app_json = requests.get(url=app_url, headers=app_header, params=app_param_userinfo, proxies=proxy, timeout=6).json()
            if 'msg' in app_json:
                if app_json['msg'] == '这里还没有内容':
                    print('❤这里还没有内容，使用带cookie的header')
                    app_json = requests.get(url=app_url, headers=app_header_cookie, params=app_param_userinfo, proxies=proxy, timeout=6).json()
                    if 'msg' in app_json:
                        print('❤' + app_json['msg'] + '默认赋值为['', '', '', '', '']')
                        return ['', '', '', '', '', '', '']

            assert app_json['data']['userInfo']
        except:
            change_proxy(3)
            return self.get_user_info(user_id, retry_count - 1)
        ###############################################################
        
        user_item = {}
        if app_json['data']['userInfo']['gender'] == 'f':
            gender = '女'
        elif app_json['data']['userInfo']['gender'] == 'm':
            gender = '男'
        else:
            gender = '其他'
        user_item['性别'] = gender
        user_item['关注'] = app_json['data']['userInfo']['follow_count']
        user_item['粉丝'] = app_json['data']['userInfo']['followers_count']

        user_item['是否认证'] = app_json['data']['userInfo']['verified']
        user_item['认证类型'] = app_json['data']['userInfo']['verified_type'] if 'verified_type' in app_json['data']['userInfo'] else ''
        user_item['verified_type_ext'] = app_json['data']['userInfo']['verified_type_ext'] if 'verified_type_ext' in app_json['data']['userInfo'] else ''
        user_item['认证说明'] = app_json['data']['userInfo']['verified_reason']  if 'verified_reason' in app_json['data']['userInfo'] else ''
        return user_item

    def get_cards_info(self, user_id, retry_count):
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

            app_json = requests.get(url=app_url, headers=app_header, params=app_param_cardsinfo, proxies=proxy, timeout=6).json()

            if 'msg' in app_json:
                if app_json['msg'] == '这里还没有内容':
                    print('❤这里还没有内容，使用带cookie的header')
                    app_json = requests.get(url=app_url, headers=app_header, params=app_param_cardsinfo, proxies=proxy, timeout=6).json()
                    if 'msg' in app_json:
                        print('❤' + app_json['msg'])
                        return ['']

            assert app_json['data']['cards']
        except:
            change_proxy(3)
            return self.get_user_info(user_id, retry_count - 1)

        place = ''
        card_group = app_json['data']['cards'][0]['card_group'][0]

        if 'item_name' in card_group:
            if card_group['item_name'] == '所在地':
                place = card_group['item_content']

        place_item = {'所在地': place}
        return place_item

    def start(self):
        all_data_list = []
        need = self.get_web_data(retry_count=3)
        for n in need:
            all_data = {}
            web_info = n
            user_id = n['用户id']
            user_info = self.get_user_info(user_id=user_id, retry_count=5)
            place_info = self.get_cards_info(user_id=user_id, retry_count=3)

            all_data.update(web_info)
            all_data.update(user_info)
            all_data.update(place_info)
            print(web_info)
            print(user_info)
            print(place_info)
            all_data_list.append(all_data)
        return all_data_list


if __name__ == '__main__':
    change_proxy(1)
    # 日期要多加1天
    date_list = ['2018-01-01', '2018-01-02', '2018-01-03', '2018-01-04', '2018-01-05', '2018-01-06', '2018-01-07', '2018-01-08', '2018-01-09', '2018-01-10', '2018-01-11', '2018-01-12', '2018-01-13', '2018-01-14', '2018-01-15', '2018-01-16', '2018-01-17', '2018-01-18', '2018-01-19', '2018-01-20', '2018-01-21', '2018-01-22', '2018-01-23', '2018-01-24', '2018-01-25', '2018-01-26', '2018-01-27', '2018-01-28', '2018-01-29', '2018-01-30', '2018-01-31', '2018-02-01', '2018-02-02', '2018-02-03', '2018-02-04', '2018-02-05', '2018-02-06', '2018-02-07', '2018-02-08', '2018-02-09', '2018-02-10', '2018-02-11', '2018-02-12', '2018-02-13', '2018-02-14', '2018-02-15', '2018-02-16', '2018-02-17', '2018-02-18', '2018-02-19', '2018-02-20', '2018-02-21', '2018-02-22', '2018-02-23', '2018-02-24', '2018-02-25', '2018-02-26', '2018-02-27', '2018-02-28', '2018-03-01', '2018-03-02', '2018-03-03', '2018-03-04', '2018-03-05', '2018-03-06', '2018-03-07', '2018-03-08', '2018-03-09', '2018-03-10', '2018-03-11', '2018-03-12', '2018-03-13', '2018-03-14', '2018-03-15', '2018-03-16', '2018-03-17', '2018-03-18', '2018-03-19', '2018-03-20', '2018-03-21', '2018-03-22', '2018-03-23', '2018-03-24', '2018-03-25', '2018-03-26', '2018-03-27', '2018-03-28', '2018-03-29', '2018-03-30', '2018-03-31', '2018-04-01', '2018-04-02', '2018-04-03', '2018-04-04', '2018-04-05', '2018-04-06', '2018-04-07', '2018-04-08', '2018-04-09', '2018-04-10', '2018-04-11', '2018-04-12', '2018-04-13', '2018-04-14', '2018-04-15', '2018-04-16', '2018-04-17', '2018-04-18', '2018-04-19', '2018-04-20', '2018-04-21', '2018-04-22', '2018-04-23', '2018-04-24', '2018-04-25', '2018-04-26', '2018-04-27', '2018-04-28', '2018-04-29', '2018-04-30', '2018-05-01', '2018-05-02', '2018-05-03', '2018-05-04', '2018-05-05', '2018-05-06', '2018-05-07', '2018-05-08', '2018-05-09', '2018-05-10', '2018-05-11', '2018-05-12', '2018-05-13', '2018-05-14', '2018-05-15', '2018-05-16', '2018-05-17', '2018-05-18', '2018-05-19', '2018-05-20', '2018-05-21', '2018-05-22', '2018-05-23', '2018-05-24', '2018-05-25', '2018-05-26', '2018-05-27', '2018-05-28', '2018-05-29', '2018-05-30', '2018-05-31', '2018-06-01', '2018-06-02', '2018-06-03', '2018-06-04', '2018-06-05', '2018-06-06', '2018-06-07', '2018-06-08', '2018-06-09', '2018-06-10', '2018-06-11', '2018-06-12', '2018-06-13', '2018-06-14', '2018-06-15', '2018-06-16', '2018-06-17', '2018-06-18', '2018-06-19', '2018-06-20', '2018-06-21', '2018-06-22', '2018-06-23', '2018-06-24', '2018-06-25', '2018-06-26', '2018-06-27', '2018-06-28', '2018-06-29', '2018-06-30', '2018-07-01', '2018-07-02', '2018-07-03', '2018-07-04', '2018-07-05', '2018-07-06', '2018-07-07', '2018-07-08', '2018-07-09', '2018-07-10', '2018-07-11', '2018-07-12', '2018-07-13', '2018-07-14', '2018-07-15', '2018-07-16', '2018-07-17', '2018-07-18', '2018-07-19', '2018-07-20', '2018-07-21', '2018-07-22', '2018-07-23', '2018-07-24', '2018-07-25', '2018-07-26', '2018-07-27', '2018-07-28', '2018-07-29', '2018-07-30', '2018-07-31', '2018-08-01', '2018-08-02', '2018-08-03', '2018-08-04', '2018-08-05', '2018-08-06', '2018-08-07', '2018-08-08', '2018-08-09', '2018-08-10', '2018-08-11', '2018-08-12', '2018-08-13', '2018-08-14', '2018-08-15', '2018-08-16', '2018-08-17', '2018-08-18', '2018-08-19', '2018-08-20', '2018-08-21', '2018-08-22', '2018-08-23', '2018-08-24', '2018-08-25', '2018-08-26', '2018-08-27', '2018-08-28', '2018-08-29', '2018-08-30', '2018-08-31', '2018-09-01', '2018-09-02', '2018-09-03', '2018-09-04', '2018-09-05', '2018-09-06', '2018-09-07', '2018-09-08', '2018-09-09', '2018-09-10', '2018-09-11', '2018-09-12', '2018-09-13', '2018-09-14', '2018-09-15', '2018-09-16', '2018-09-17', '2018-09-18', '2018-09-19', '2018-09-20', '2018-09-21', '2018-09-22', '2018-09-23', '2018-09-24', '2018-09-25', '2018-09-26', '2018-09-27', '2018-09-28', '2018-09-29', '2018-09-30', '2018-10-01', '2018-10-02', '2018-10-03', '2018-10-04', '2018-10-05', '2018-10-06', '2018-10-07', '2018-10-08', '2018-10-09', '2018-10-10', '2018-10-11', '2018-10-12', '2018-10-13', '2018-10-14', '2018-10-15', '2018-10-16', '2018-10-17', '2018-10-18', '2018-10-19', '2018-10-20', '2018-10-21', '2018-10-22', '2018-10-23', '2018-10-24', '2018-10-25', '2018-10-26', '2018-10-27', '2018-10-28', '2018-10-29', '2018-10-30', '2018-10-31', '2018-11-01', '2018-11-02', '2018-11-03', '2018-11-04', '2018-11-05', '2018-11-06', '2018-11-07', '2018-11-08', '2018-11-09', '2018-11-10', '2018-11-11', '2018-11-12', '2018-11-13', '2018-11-14', '2018-11-15', '2018-11-16', '2018-11-17', '2018-11-18', '2018-11-19', '2018-11-20', '2018-11-21', '2018-11-22', '2018-11-23', '2018-11-24', '2018-11-25', '2018-11-26', '2018-11-27', '2018-11-28', '2018-11-29', '2018-11-30', '2018-12-01', '2018-12-02', '2018-12-03', '2018-12-04', '2018-12-05', '2018-12-06', '2018-12-07', '2018-12-08', '2018-12-09', '2018-12-10', '2018-12-11', '2018-12-12', '2018-12-13', '2018-12-14', '2018-12-15', '2018-12-16', '2018-12-17', '2018-12-18', '2018-12-19', '2018-12-20', '2018-12-21', '2018-12-22', '2018-12-23', '2018-12-24', '2018-12-25', '2018-12-26', '2018-12-27', '2018-12-28', '2018-12-29', '2018-12-30', '2018-12-31']

    # custom:2020-01-09-0:2020-01-10-0 key_list = ['600028', '601668', '601398', '601318', '601939', '601288',
    # '600104', '601988', '601628', '601390', '旅游']
    key_list = ['罗志祥']

    # csv_name = '人民币消毒'

    for key in key_list:
        for d in date_list:
            # 保存第一页数据，并修改总页数（只能通过第一次请求获取总页数）
            wb = WbSpider(keyword=key, start_time=d + '-0', end_time=d + '-24', page=1)
            data = wb.start()
            save_to_csv(file_name=key+'.csv', list_dict=data)
            print('################################################')
            print(f"{key} {d}第{1}页数据存储成功。。。。。。")
            print('################################################')

            # 保存剩下页数数据
            for i in range(2, total_page + 1):
                wb = WbSpider(keyword=key, start_time=d + '-0', end_time=d + '-24', page=i)
                data = wb.start()
                save_to_csv(file_name=key + '.csv', list_dict=data)
                print('################################################')
                print(f"{key} {d}第{i}页数据存储成功。。。。。。")
                print('################################################')

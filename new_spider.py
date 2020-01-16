import re
import time
import requests
from lxml import html
import string
from retrying import retry
from constants import *
import pysnooper

etree = html.etree

total_page = 50
proxy = ''


class WbSpider:
    def __init__(self, keyword, date, page):
        self.keyword = keyword
        self.date = date
        self.page = page

    @retry(stop_max_attempt_number=3, wait_random_min=1000, wait_random_max=5000)
    def change_proxy(self, retry_count):
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
            self.change_proxy(retry_count - 1)

    def web_requests(self, retry_count):
        param = {
            'q': self.keyword,
            'typeall': '1',
            'suball': '1',
            'timescope': 'custom:' + self.date + ':' + self.date,
            'Refer': 'g',
            'page': self.page
        }
        if retry_count < 0:
            return
        try:
            res_web = requests.get(url=web_url, headers=web_header, params=param, proxies=proxy, timeout=6).content.decode()
            root_web = etree.HTML(res_web)

            table_item = root_web.xpath("//div[@class='card-wrap']")
            assert table_item
            return root_web
        except:
            self.change_proxy(3)
            return self.web_requests(retry_count - 1)

    def get_web_data(self):
        web_html = self.web_requests(3)
        if web_html is None:
            web_html = self.web_requests(1)

        if self.page == 1:
            global total_page
            total_page = len(web_html.xpath("//ul[@class='s-scroll']/li"))
            if total_page == 0:
                total_page = 1
            print(f'总页数:{total_page}')

        table_item = web_html.xpath("//div[@class='card-wrap']")
        web_data_list = []
        for i in range(0, len(table_item)):
            try:
                # 微博数据
                user_name = table_item[i].xpath(".//div[@class='info']/div[2]/a/text()")[0]  # 用户名
                user_url = 'https:' + table_item[i].xpath(".//div[@class='info']/div[2]/a/@href")[0]  # 用户个人主页地址
                user_id = re.findall('.*weibo.com/(.*)refer_flag', user_url)[0].replace('?', '')
                content = table_item[i].xpath("string(.//p[@node-type='feed_list_content'])") \
                    if table_item[i].xpath("string(.//p[@node-type='feed_list_content_full'])") == '' \
                    else table_item[i].xpath("string(.//p[@node-type='feed_list_content_full'])")
                content = ''.join([i for i in content if i not in string.whitespace])  # 微博内容
                date_time = table_item[i].xpath("string(.//div[@class='content']/p[@class='from']/a[1])")  # 发微博的时间
                date_time = ''.join([i for i in date_time if i not in string.whitespace])[0:11]  # 发微博的时间
                comment_num = 0 \
                    if table_item[i].xpath("string (.//div[@class='card-act']/ul/li[3])").replace('评论', '') == ' ' \
                    else table_item[i].xpath("string(.//div[@class='card-act']/ul/li[3])").replace('评论 ', '')  # 评论数
                forward_num = 0 \
                    if table_item[i].xpath("string(.//div[@class='card-act']/ul/li[2])").replace('转发', '') == '  ' \
                    else table_item[i].xpath("string(.//div[@class='card-act']/ul/li[2])").replace('转发 ', '')  # 转发数
                up_num = 0 if table_item[i].xpath("string(.//div[@class='card-act']/ul/li[4])") == ' ' \
                    else table_item[i].xpath("string(.//div[@class='card-act']/ul/li[4])").replace(' ', '')  # 点赞数
                wb_url = 'https:' + table_item[i].xpath(".//div[@class='content']/p[@class='from']/a[1]/@href")[0]
                web_data = [content, date_time, comment_num, forward_num, up_num, wb_url, user_name, user_id]
                web_data_list.append(web_data)
            except IndexError:
                break
        return web_data_list

    @pysnooper.snoop("./log")
    def app_requests(self, user_id, retry_count):
        app_param = {
            'jumpfrom': 'weibocom',
            'sudaref': 's.weibo.com',
            'type': 'uid',
            'value': user_id
        }
        while retry_count < 0:
            return ['', '', '', '', '']
        try:
            app_json = requests.get(url=app_url, headers=app_header, params=app_param, proxies=proxy, timeout=6).json()
            assert app_json['data']['userInfo']
            gender = '女' if app_json['data']['userInfo']['gender'] == 'f' else '男'  # 性别
            follow_count = app_json['data']['userInfo']['follow_count']  # 关注
            followers_count = app_json['data']['userInfo']['followers_count']  # 粉丝
            verified = app_json['data']['userInfo']['verified']  # 是否认证
            verified_type = app_json['data']['userInfo']['verified_type']  # 认证类型
            app_data = [gender, follow_count, followers_count, verified, verified_type]
            return app_data
        except:
            self.change_proxy(3)
            return self.app_requests(user_id, retry_count - 1)

    def start(self):
        all_data_list = []
        web = self.get_web_data()
        for i in web:
            web_data = i[0:7]
            user_id = i[-1]
            app_data = self.app_requests(user_id=user_id, retry_count=3)
            print(web_data)
            print(app_data)
            print('-------------------------------')
            all_data = web_data + app_data
            all_data_list.append(all_data)
        return all_data_list


if __name__ == '__main__':
    for i in range(1, total_page):
        wb = WbSpider(keyword='张恒', date='20200116', page=i)
        wb.start()

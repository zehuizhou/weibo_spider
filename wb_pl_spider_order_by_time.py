# -*- coding: utf-8 -*-
import random
import sys
import time
import requests
from constants import save_to_csv, change_proxy, web_header
from fake_useragent import UserAgent
from parsel import Selector

ua = UserAgent(verify_ssl=False)


def spider():
    base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&'
    first_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id=4514598240442496&filter=all&from=singleWeiBo&__rnd=1592386336588'

    web_header.update({'Host': 'weibo.com'})
    url = first_url
    while True:
        def get_ret(count):
            if count < 0:
                sys.exit()
            try:
                with open('pro.txt', 'r') as f:
                    proxy = eval(f.read())
                r = requests.get(url=url, headers=web_header, proxies=proxy, timeout=6).json()
                print(r)
                assert 'action-data' in str(r)

                time.sleep(random.uniform(0.2, 2.5))
                return r
            except Exception as e:
                print(e)
                change_proxy(3)
                return get_ret(count - 1)

        res = get_ret(5)
        html = res['data']['html']
        root = Selector(html)
        action_data = root.xpath("//a[@action-type='click_more_comment']/@action-data").get('')
        if action_data == '':
            action_data = root.xpath("//div[@node-type='comment_loading']/@action-data").get('')
        url = base_url + action_data + '&from=singleWeiBo'

        div_list = root.xpath("//div[@class='list_box']/div[@class='list_ul']/div")
        for div in div_list:
            item = {}
            item['昵称'] = div.xpath(".//div[@class='WB_text']/a[1]/text()").get('')
            item['用户id'] = div.xpath(".//div[@class='WB_text']/a[1]/@usercard").get('').replace('id=', '')
            item['评论内容'] = div.xpath(".//div[@class='WB_text']/text()").getall()[1].strip().replace('：', '') if len(div.xpath(".//div[@class='WB_text']/text()").getall()) > 0 else ''
            item['评论时间'] = div.xpath(".//div[@class='WB_from S_txt2']/text()").get('')
            item['点赞数'] = div.xpath(".//span[@node-type='like_status']/em[2]/text()").get('').replace('赞', '0')
            item['链接'] = url
            print(item)
            save_to_csv(file_name='A_3.8W条评论', list_dict=[item])


if __name__ == '__main__':
    spider()

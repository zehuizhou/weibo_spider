import re
import requests
from lxml import html
import datetime
import string
from constants import change_proxy, save_to_csv, web_header, app_header, app_header_cookie, web_url, app_url

etree = html.etree

total_page = 1


class WbSpider:
    def __init__(self, keyword, start_time, end_time, page):
        self.keyword = keyword
        self.start_time = start_time
        self.end_time = end_time
        self.page = page

    def get_web_data(self, retry_count):
        # 发起请求
        param = {
            'scope': 'ori',  # 是否原创
            'q': self.keyword,
            # 'typeall': '1',  # 全部（和scope二选一）
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
            div_list = root_web.xpath("//div[@class='card-wrap']/div[@class='card']")
            assert div_list
        except Exception as e:
            print(e)
            change_proxy(3)
            return self.get_web_data(retry_count - 1)

        # 提取数据
        if self.page == 1:
            global total_page
            total_page = len(root_web.xpath("//ul[@class='s-scroll']/li"))
            if total_page == 0:
                total_page = 1
            print(f'总页数:{total_page}')

        div_list = root_web.xpath("//div[@class='card-wrap']/div[@class='card']")
        web_data_list = []
        for div in div_list:
            # 判断是否有“展开全文”
            is_full = div.xpath(".//div[@class='content']/p[@node-type='feed_list_content_full']")

            web_item = {}
            user_url = 'https:' + div.xpath(".//div[@class='info']/div[2]/a/@href")[0]

            web_item['微博id'] = '`' + str(div.xpath("./../@mid")[0])
            web_item['用户名'] = div.xpath(".//div[@class='info']/div[2]/a/text()")[0]

            web_item['个人主页链接'] = user_url
            web_item['用户id'] = re.findall('.*weibo.com/(.*)refer_flag', user_url)[0].replace('?', '')

            content = div.xpath("string(.//div[@class='content']/p[@node-type='feed_list_content_full'])") if is_full \
                else div.xpath("string(.//div[@class='content']/p[@node-type='feed_list_content'])")
            web_item['内容'] = ''.join([c for c in content if c not in string.whitespace])  # 微博内容

            forward_content = div.xpath("string(.//div[@class='content']/div[@class='card-comment'])")
            web_item['转发内容'] = ''.join([f for f in forward_content if f not in string.whitespace])  # 转发内容

            date_time = div.xpath("string(.//div[@class='content']/p[@class='from']/a[1])")  # 发微博的时间
            date_time = ''.join([t for t in date_time if t not in string.whitespace])  # 发微博的时间
            if len(date_time) == 11:
                date_time = str(datetime.datetime.now())[0:4] + '-' + date_time[0:2] + '-' + date_time[3:5] + ' ' + date_time[-5:]
            else:
                date_time = date_time[0:4] + '-' + date_time[5:7] + '-' + date_time[8:10] + ' ' + date_time[-5:]
            web_item['时间'] = date_time
            pl = div.xpath("string (.//div[@class='card-act']/ul/li[3])")
            web_item['评论数'] = re.findall('\d+', pl)[0] if re.findall('\d+', pl) else 0
            zf = div.xpath("string(.//div[@class='card-act']/ul/li[2])")
            web_item['转发数'] = re.findall('\d+', zf)[0] if re.findall('\d+', zf) else 0
            dz = div.xpath("string(.//div[@class='card-act']/ul/li[4])")
            web_item['点赞数'] = re.findall('\d+', dz)[0] if re.findall('\d+', dz) else 0
            web_item['微博链接'] = 'https:' + div.xpath(".//div[@class='content']/p[@class='from']/a[1]/@href")[0]
            web_item['表情数'] = len(div.xpath(".//div[@class='content']/p//img[@class='face']"))
            web_item['表情'] = '\n'.join(div.xpath(".//div[@class='content']/p//img[@class='face']/@title"))
            img_num = len(div.xpath(".//div[@class='content']//img[@action-type='fl_pics']/@src"))
            web_item['图片数'] = img_num
            web_item['图片链接'] = 'https:' + '\nhttps:'.join(div.xpath(".//div[@class='content']//img[@action-type='fl_pics']/@src")) if img_num else ''

            zm = div.xpath(".//div[@class='content']//p//a/i")
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
                em = div.xpath(".//div[@class='content']/p[@node-type='feed_list_content_full']/a/i/text()")[0] \
                    if is_full else div.xpath(".//div[@class='content']/p[@node-type='feed_list_content']/a/i/text()")[0]
            except IndexError:
                em = ''

            if em == '2':
                location = div.xpath(".//div[@class='content']/p[@node-type='feed_list_content_full']/a/i/../text()")[0].replace('2', '')\
                    if is_full else div.xpath(".//div[@class='content']/p[@node-type='feed_list_content']/a/i/../text()")[0].replace('2', '')
            else:
                location = ''
            web_item['定位'] = location
            web_data_list.append(web_item)
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
            return {}
        try:
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())

            app_json = requests.get(url=app_url, headers=app_header, params=app_param_userinfo, proxies=proxy, timeout=6).json()
            if 'msg' in app_json:
                if app_json['msg'] == '这里还没有内容':
                    print('❤这里还没有内容，使用带cookie的header')
                    app_json = requests.get(url=app_url, headers=app_header_cookie, params=app_param_userinfo, proxies=proxy, timeout=6).json()
                    if 'msg' in app_json:
                        print('❤' + app_json['msg'])
                        return {'性别': '', '关注': '', '粉丝': '', '是否认证': '', '认证类型': '', 'verified_type_ext': '', '认证说明': ''}
            assert app_json['data']['userInfo']
        except Exception as e:
            print(e)
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
                    app_json = requests.get(url=app_url, headers=app_header_cookie, params=app_param_cardsinfo, proxies=proxy, timeout=6).json()
                    if 'msg' in app_json:
                        print('❤' + app_json['msg'])
                        return {'所在地': ''}
            assert app_json['data']['cards']
        except Exception as e:
            print(e)
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
            # place_info = self.get_cards_info(user_id=user_id, retry_count=3)

            all_data.update(web_info)
            all_data.update(user_info)
            # all_data.update(place_info)
            print(web_info)
            print(user_info)
            # print(place_info)
            all_data_list.append(all_data)
        return all_data_list


if __name__ == '__main__':
    change_proxy(1)
    # 日期要多加1天
    date_list = ['2020-05-21', '2020-05-22', '2020-05-23', '2020-05-24', '2020-05-25', '2020-05-26', '2020-05-27', '2020-05-28', '2020-05-29', '2020-05-30', '2020-05-31', '2020-06-01']

    # custom:2020-01-09-0:2020-01-10-0 key_list = ['600028', '601668', '601398', '601318', '601939', '601288',
    # '600104', '601988', '601628', '601390', '旅游']
    key_list = ['#毛不易的美味歌单#']

    # csv_name = '人民币消毒'

    for key in key_list:
        for d in date_list:
            # 保存第一页数据，并修改总页数（只能通过第一次请求获取总页数）
            wb = WbSpider(keyword=key, start_time=d + '-0', end_time=d + '-24', page=1)
            data = wb.start()
            save_to_csv(file_name=key+'.csv', list_dict=data)
            print('############################')
            print(f"{key} {d}第{1}页数据存储成功")
            print('############################')

            # 保存剩下页数数据
            for i in range(2, total_page + 1):
                wb = WbSpider(keyword=key, start_time=d + '-0', end_time=d + '-24', page=i)
                data = wb.start()
                save_to_csv(file_name=key + '.csv', list_dict=data)
                print('############################')
                print(f"{key} {d}第{i}页数据存储成功")
                print('############################')

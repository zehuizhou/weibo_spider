# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
# 代理ip地址
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=4ed5fac7b24bba823e18f5299a16232e&orderNo=GL20200112165156B8GF39F4&count=1&isTxt=0&proxyType=1'

# web
web_url = 'https://s.weibo.com/weibo'

# cookie过期了就修改下
web_cookie = 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; Hm_lvt_50f34491c9065a59f87d0d334df29fa4=1577155440,1577155459; wvr=6; UOR=,,www.baidu.com; Ugrow-G0=140ad66ad7317901fc818d7fd7743564; SSOLoginState=1579054565; _s_tentry=login.sina.com.cn; Apache=5998859689627.967.1579054575244; ULV=1579054575251:7:5:3:5998859689627.967.1579054575244:1579052540860; secsys_id=46a0f46f252e2f8616a30a9456c3eaf1; YF-V5-G0=7a7738669dbd9095bf06898e71d6256d; YF-Page-G0=f0aa2e6d566ccd1c288fae19df01df56|1579063573|1579063573; login_sid_t=3954023b6f6bffede4e9f7cd157bf008; cross_origin_proto=SSL; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZf1L9rhvuemZ0RQUfwIqwdUHMpu1WUdVNxqUXMJeuG-qY.; SUB=_2A25zG6CwDeRhGeVI7lER9CvFyD6IHXVQUJV4rDV8PUNbmtAfLVnakW9NTAX_rBVWvkGqtsXDKeXU5SEk3eiCYiS8; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0P188nVnWReE-I; ALF=1610679392; webim_unReadCount=%7B%22time%22%3A1579144060205%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'

web_header = {
    'Host': 's.weibo.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': web_cookie
}

# app
app_url = 'https://m.weibo.cn/api/container/getIndex'

token = 'f7a921'

app_header = {
    'X-XSRF-TOKEN': token,
    'User-Agent': ua.random,
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest'
}

dates = ['2019-07-14', '2019-07-15', '2019-07-16', '2019-07-17', '2019-07-18', '2019-07-19', '2019-07-20',
         '2019-07-21', '2019-07-22', '2019-07-23', '2019-07-24', '2019-07-25', '2019-07-26', '2019-07-27',
         '2019-07-28', '2019-07-29', '2019-07-30', '2019-07-31', '2019-08-01', '2019-08-02', '2019-08-03',
         '2019-08-04', '2019-08-05', '2019-08-06', '2019-08-07', '2019-08-08', '2019-08-09', '2019-08-10',
         '2019-08-11', '2019-08-12', '2019-08-13', '2019-08-14', '2019-08-15', '2019-08-16', '2019-08-17',
         '2019-08-18', '2019-08-19', '2019-08-20', '2019-08-21', '2019-08-22', '2019-08-23', '2019-08-24',
         '2019-08-25', '2019-08-26', '2019-08-27']

keywords = ['香港问题', '香港事件', '香港议员']

app_param = {
    'type': 'uid',
    'value': 1729861114,
}

# res = requests.get(url=app_url, headers=app_header, params=app_param).json()
# print(res)

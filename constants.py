# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

# 代理ip地址
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=fb037669709eba969179b22f2064a0a1&orderNo=GL20200225155830IrGknHSG&count=1&isTxt=0&proxyType=1'

# web
web_url = 'https://s.weibo.com/weibo'

# cookie过期了就修改下
web_cookie = 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; UOR=,,login.sina.com.cn; wvr=6; ALF=1614494356; SSOLoginState=1582958357; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfOstEk2WxkywxtwS8tD2m7AfY1hukb5fteqfZpw_aONQ.; SUB=_2A25zXndGDeRhGeVI7lER9CvFyD6IHXVQKu-OrDV8PUNbmtAfLULhkW9NTAX_rHPf0Dbbea2eBbuck8Ywmwmn-5Ua; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=05iKh-Q44-DnRi; _s_tentry=login.sina.com.cn; Apache=2537411284708.8394.1582958361189; ULV=1582958361298:14:7:7:2537411284708.8394.1582958361189:1582854661963; webim_unReadCount=%7B%22time%22%3A1582958363171%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined'

web_header = {
    'Host': 's.weibo.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': web_cookie
}

# app
app_url = 'https://m.weibo.cn/api/container/getIndex'

token = 'fd14bd'

app_header_cookie = {
    'x-xsrf-token': token,
    'User-Agent': ua.random,
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'cookie': '_T_WM=24942942014; _ga=GA1.2.852180565.1582702609; ALF=1585550357; XSRF-TOKEN=3334c4; WEIBOCN_FROM=1110005030; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; MLOGIN=1; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfd0LzLA07BluHdV7ped0bWDazqUJrG2ckDD2WkPqnk-I.; SUB=_2A25zXnrVDeRhGeVI7lER9CvFyD6IHXVQoQadrDV6PUJbktANLWnEkW1NTAX_rE0o8VlZYdkSb03fwvn5hj-RuYR7; SUHB=0G0euq5tLxBMQZ; SSOLoginState=1582959238; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1005056487028379%26fid%3D1005056487028379%26uicode%3D10000011'
}

app_header = {
    'X-XSRF-TOKEN': token,
    'User-Agent': ua.random,
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest'
}

dates = ['2019-10-01']

keywords = ['香港问题', '香港事件', '香港议员']

app_param = {
    'type': 'uid',
    'value': 1981449674,
}

"""https://weibo.com/u/6487028379?refer_flag=1001030103_"""

# res = requests.get(url=app_url, headers=app_header_cookie, params=app_param).json()
#
# print(res)

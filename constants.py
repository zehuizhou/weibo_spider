# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

# 代理ip地址
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=3f3a3212bb8129e0d70d325c41bed8c7&orderNo=GL20200223101445SA8mbNNF&count=1&isTxt=0&proxyType=1'

# web
web_url = 'https://s.weibo.com/weibo'

# cookie过期了就修改下
web_cookie = 'SINAGLOBAL=1970227005826.6147.1563864103000; UOR=,,login.sina.com.cn; Ugrow-G0=cf25a00b541269674d0feadd72dce35f; YF-V5-G0=f5a079faba115a1547149ae0d48383dc; login_sid_t=5ad5818d069ded098ea5f13d5ee3f7b0; cross_origin_proto=SSL; _s_tentry=login.sina.com.cn; Apache=5717888890769.127.1582509596538; ULV=1582509596546:7:7:1:5717888890769.127.1582509596538:1582250939410; wb_view_log_3653045932=1680*10502; WBStorage=42212210b087ca50|undefined; wb_view_log=1680*10502; WBtopGlobal_register_version=307744aa77dd5677; SCF=ApTuVIRec5rnYko_9HmLKx8JM1Qd-n8MCEh-QuP9AgxCAJHJw8l9S64OmLPtfhfvphS7f51vaMgIv6bfm37eH94.; SUB=_2A25zUB8CDeRhGeVI7lER9CvFyD6IHXVQJHfKrDV8PUNbmtAfLVnSkW9NTAX_rDJTfDyyCZ0jQydOBXGTQ_mo3VDK; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0TPlxq9jgiqqpE; ALF=1614127827; SSOLoginState=1582591830; wvr=6; YF-Page-G0=4a643298bc01367bda901663683cd587|1582591850|1582591850; webim_unReadCount=%7B%22time%22%3A1582591860918%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'

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
    'cookie': '_T_WM=56715619644; WEIBOCN_FROM=1110003030; ALF=1585183829; XSRF-TOKEN=5f995c; SCF=ApTuVIRec5rnYko_9HmLKx8JM1Qd-n8MCEh-QuP9AgxCQ7dcVC6U-hnXEq1eE7o2FmEdJdm_7XdDVQcmDoaDDgI.; SUB=_2A25zUB-RDeRhGeVI7lER9CvFyD6IHXVQuqHZrDV6PUJbktANLXbekW1NTAX_rDzOC5a1-xsYm8UZSynicHAzWqqo; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=03o1lVi02r40_T; SSOLoginState=1582591937; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076036487028379%26fid%3D1005056487028379%26uicode%3D10000011'
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

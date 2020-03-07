# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

# 代理ip地址
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=fb037669709eba969179b22f2064a0a1&orderNo=GL20200225155830IrGknHSG&count=1&isTxt=0&proxyType=1'

# web
web_url = 'https://s.weibo.com/weibo'

# cookie过期了就修改下
web_cookie = 'SINAGLOBAL=1090758372960.1766.1562847473607; ALF=1614569588; SSOLoginState=1583033589; SCF=AiDcH5yG7P90hiw60kfQQhisYZmUC4yLSh_ZLjpiEJjeP4uBdQkrrF58WXsy6Q5xz0CwR7sADInr-L3Nx2vgeJA.; SUB=_2A25zX1ymDeRhGeVI7lER9CvFyD6IHXVQLclurDV8PUNbmtAfLRPMkW9NTAX_rDz1LtTlTM1I73IAizjqgby5aVks; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=02MfWbwgzONWCT; wvr=6; _s_tentry=login.sina.com.cn; UOR=www.7po.com,widget.weibo.com,login.sina.com.cn; Apache=5037387369390.458.1583033594809; ULV=1583033594820:16:1:1:5037387369390.458.1583033594809:1582978849836; webim_unReadCount=%7B%22time%22%3A1583035089161%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'

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
    'cookie': '_ga=GA1.2.852180565.1582702609; WEIBOCN_FROM=1110005030; _T_WM=73519821653; MLOGIN=1; ALF=1586162479; XSRF-TOKEN=799afa; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfG4hUcE3jGaWhGDzqrhLLWDSFzsi3eSSUqJYT8xFFGNE.; SUB=_2A25zZy5vDeRhGeVI7lER9CvFyD6IHXVQq7InrDV6PUJbktAKLWXYkW1NTAX_rBY_NKuZEMx9mqKZOzN5V0wOZoQL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=06Z1FKoV8Tj2PB; SSOLoginState=1583570495; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D2302836029748720%26fid%3D1005056029748720%26uicode%3D10000011'
}

app_header = {
    'X-XSRF-TOKEN': token,
    'User-Agent': ua.random,
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest'
}



app_param = {
    'type': 'uid',
    'value': 1981449674,
}
"https://m.weibo.cn/api/container/getIndex?refer_flag[]=1001030103_&refer_flag[]=1001030103_&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&sudaref=s.weibo.com&type=uid&value=5586763840&containerid=2302835586763840"
"https://m.weibo.cn/api/container/getIndex?refer_flag[]=1001030103_&refer_flag[]=1001030103_&is_hot[]=1&is_hot[]=1&jumpfrom=weibocom&sudaref=s.weibo.com&type=uid&value=5586763840&containerid=1005055586763840"

"""https://weibo.com/u/6487028379?refer_flag=1001030103_"""

res = requests.get(url=app_url, headers=app_header_cookie, params=app_param).json()

print(res)

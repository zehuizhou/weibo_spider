# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

# 代理ip地址
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=8d7cc3c74eeb76ad422c67df45944d31&orderNo=GL20200131152126nmVxqyej&count=1&isTxt=0&proxyType=1'

# web
web_url = 'https://s.weibo.com/weibo'

# cookie过期了就修改下
web_cookie = 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; wvr=6; login_sid_t=0921cff3290f71ddaddeb9791cc1ec5e; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; UOR=,,www.baidu.com; Apache=241358778566.89136.1583888615148; ULV=1583888615153:20:6:1:241358778566.89136.1583888615148:1583472822048; SSOLoginState=1583888646; webim_unReadCount=%7B%22time%22%3A1583918693198%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KMhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; ALF=1615511248; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZft3bTp0j7uZrFLHOfGK3gtPFApHsYSly1W8tEimLbPDo.; SUB=_2A25zbfsdDeRhGeVI7lER9CvFyD6IHXVQG2vVrDV8PUNbmtAfLUblkW9NTAX_rAWOKO3Cn4bnLoXfNdlOpGRo-RrD; SUHB=0h15T_i9y2ZlWV'

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

# res = requests.get(url=app_url, headers=app_header_cookie, params=app_param).json()
#
# print(res)

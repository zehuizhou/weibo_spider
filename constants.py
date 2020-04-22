# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

# 代理ip地址
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=8d7cc3c74eeb76ad422c67df45944d31&orderNo=GL20200131152126nmVxqyej&count=1&isTxt=0&proxyType=1'

# web
web_url = 'https://s.weibo.com/weibo'

# cookie过期了就修改下
web_cookie = 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; _s_tentry=passport.weibo.com; Apache=3765722860985.432.1587192593885; ULV=1587192593927:33:6:4:3765722860985.432.1587192593885:1587112232752; login_sid_t=d4290a64b9cb637e731e85792f4739f0; cross_origin_proto=SSL; SSOLoginState=1587193166; wvr=6; UOR=,,www.baidu.com; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZf_RfeEY7sP1hJBVjeTqmZvmVN14nI15iIO-7sQQDWSq4.; SUB=_2A25zm9KnDeRhGeVI7lER9CvFyD6IHXVQ0UNvrDV8PUNbmtAKLVrCkW9NTAX_rFAodjz9dmxOM1Tjl5midvcEnhnA; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0D-11LPvOGYakf; ALF=1619056247; webim_unReadCount=%7B%22time%22%3A1587520252314%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined'

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
    'cookie': '_ga=GA1.2.852180565.1582702609; _T_WM=70668980778; WEIBOCN_FROM=1110005030; ALF=1590112247; XSRF-TOKEN=db9590; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfldE_J8bt2MAsZo4WLLn633bSWbvrHOji2ZSzkRT6y64.; SUB=_2A25zm8inDeRhGeVI7lER9CvFyD6IHXVRZ-jvrDV6PUJbktAKLXfDkW1NTAX_rDajNOeNACRzzSzCZ4V6qebdesZE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0vJ4bSJonIhYtp; SSOLoginState=1587525879; MLOGIN=1; M_WEIBOCN_PARAMS=from%3Dfeed%26fid%3D1076035745465758%26uicode%3D10000011'
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

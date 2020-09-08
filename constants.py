# -*- coding: utf-8 -*-
import time
import requests
from fake_useragent import UserAgent
import os
import sys
import time
import requests
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

ua = UserAgent(verify_ssl=False)

# 代理ip地址 http://www.xiongmaodaili.com?invitationCode=8E31F8BE-73FA-4078-B64A-CF32280F439E 按量提取 每次1个 json格式
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=cf65354409478e7bd594f3bb98bb1805&orderNo=GL20200131152126nmVxqyej&count=1&isTxt=0&proxyType=1'

def change_proxy(retry_count):
    if retry_count < 0:
        return

    result = requests.get(proxy_url).json()
    if result['msg'] == 'ok':
        ip = result['obj'][0]['ip']
        port = result['obj'][0]['port']
        proxies = {"http": "http://" + ip + ":" + port, "https": "http://" + ip + ":" + port}

        with open('pro.txt', 'w') as f:
            f.write(str(proxies))

        print(f"代理ip为更改为：{proxies}")
        return proxies
    else:
        time.sleep(1)
        print('切换代理失败，重新尝试。。。')
        change_proxy(retry_count - 1)


# 保存数据
def save_to_csv(file_name, list_dict):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name + '.csv')
    flag = False if os.path.isfile(path) else True
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)


# web
web_url = 'https://s.weibo.com/weibo'

# cookie过期了就修改下
web_cookie = 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; wvr=6; UOR=,,www.baidu.com; Ugrow-G0=1ac418838b431e81ff2d99457147068c; login_sid_t=0a77e320293201bab2cce25b87a506d2; cross_origin_proto=SSL; YF-V5-G0=3751b8b40efecee990eab49e8d3b3354; _s_tentry=passport.weibo.com; Apache=2645040196906.0522.1592357519043; ULV=1592357519048:58:14:3:2645040196906.0522.1592357519043:1592268775076; wb_view_log=1920*10801; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfgBCx7jU_ZKm8Hfh2cEqZh7UxTJ5qJ0lSdqiexA_OwQI.; SUB=_2A25z7QL0DeRhGeVI7lER9CvFyD6IHXVQm3M8rDV8PUNbmtANLUXckW9NTAX_rKC-iKJOs4nN3Ou490Dwxw9ko7mf; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0vJ4bSJonIyucY; ALF=1623893540; SSOLoginState=1592357540; wb_view_log_3653045932=1920*10801; YF-Page-G0=f1e19cba80f4eeaeea445d7b50e14ebb|1592360893|1592360891; webim_unReadCount=%7B%22time%22%3A1592360905592%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'

web_header = {
    'Host': 's.weibo.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': web_cookie
}

# app
app_url = 'https://m.weibo.cn/api/container/getIndex'

app_cookie = '_ga=GA1.2.852180565.1582702609; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfYKNTUU4oscg5DwfNroNvvWp_ldLcrKjHzeaDFxG0WyM.; SUHB=0M21_tsFWEJs5E; _T_WM=61831882521; WEIBOCN_FROM=1110005030; MLOGIN=0; XSRF-TOKEN=30ea12; M_WEIBOCN_PARAMS=fid%3D1076035980037952%26uicode%3D10000011'

app_header_cookie = {
    # 'x-xsrf-token': 'fd14bd',
    'User-Agent': ua.random,
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'cookie': app_cookie
}

app_header = {
    # 'X-XSRF-TOKEN': 'fd14bd',
    'User-Agent': ua.random,
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest'
}

# app_param = {
#     'type': 'uid',
#     'value': 1981449674,
# }
#
# res = requests.get(url=app_url, headers=app_header_cookie, params=app_param).json()
#
# print(res)

if __name__ == '__main__':
    pass

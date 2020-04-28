# -*- coding: utf-8 -*-
import time
import requests
from fake_useragent import UserAgent
import os
import re
import sys
import time
import requests
from parsel import Selector
import pandas as pd

ua = UserAgent(verify_ssl=False)

# 代理ip地址
proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=8d7cc3c74eeb76ad422c67df45944d31&orderNo=GL20200131152126nmVxqyej&count=1&isTxt=0&proxyType=1'


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
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    flag = False if os.path.isfile(path) else True
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)


# web
web_url = 'https://s.weibo.com/weibo'

# cookie过期了就修改下
web_cookie = 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; wvr=6; UOR=,,www.baidu.com; wb_view_log_3653045932=1920*10801; Ugrow-G0=9ec894e3c5cc0435786b4ee8ec8a55cc; login_sid_t=430d775258d00b0bc7716ac7e386977c; cross_origin_proto=SSL; YF-V5-G0=125128c5d7f9f51f96971f11468b5a3f; WBStorage=42212210b087ca50|undefined; _s_tentry=passport.weibo.com; Apache=8400782393616.642.1587956783860; ULV=1587956783866:37:10:2:8400782393616.642.1587956783860:1587869529519; wb_view_log=1920*10801; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfNyLtXihlE7EH9IAt4zFSlq_SBisxfD8xRQkC3gYRS-g.; SUB=_2A25zojwSDeRhGeVI7lER9CvFyD6IHXVQ1irarDV8PUNbmtAfLVatkW9NTAX_rBJb3PtKsaH0IMo9W0TsiWJ5Ib4y; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0y0p1tk609DplM; ALF=1619492788; SSOLoginState=1587956802; YF-Page-G0=bf52586d49155798180a63302f873b5e|1587956804|1587956804; webim_unReadCount=%7B%22time%22%3A1587956807157%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'

web_header = {
    'Host': 's.weibo.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': web_cookie
}

# app
app_url = 'https://m.weibo.cn/api/container/getIndex'

app_cookie = 'ALF=1590628107; _T_WM=98632022946; WEIBOCN_FROM=1110003030; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; MLOGIN=1; SCF=ApTuVIRec5rnYko_9HmLKx8JM1Qd-n8MCEh-QuP9AgxCDxhUHwcdJEs34jAzvqqOHz7QelxMclJY58Yi0KDNALU.; SUB=_2A25zo_KpDeRhGeVI7lER9CvFyD6IHXVRb57hrDV6PUJbktANLRfgkW1NTAX_rCJ1jtpbkHpCEh_LY3fD_FwZIOEl; SUHB=0vJ4bSJonIhYtp; SSOLoginState=1588036345; M_WEIBOCN_PARAMS=fid%3D1076031265357020%26uicode%3D10000011; XSRF-TOKEN=37c1b4'

app_header_cookie = {
    'x-xsrf-token': 'fd14bd',
    'User-Agent': ua.random,
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Upgrade-Insecure-Requests': '1',
    'X-Requested-With': 'XMLHttpRequest',
    'cookie': app_cookie
}

app_header = {
    'X-XSRF-TOKEN': 'fd14bd',
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

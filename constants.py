# -*- coding: utf-8 -*-
import time
import requests
from fake_useragent import UserAgent
import os
import sys
import time
import requests
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
web_cookie = 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; wvr=6; UOR=,,www.baidu.com; Ugrow-G0=9ec894e3c5cc0435786b4ee8ec8a55cc; login_sid_t=430d775258d00b0bc7716ac7e386977c; cross_origin_proto=SSL; YF-V5-G0=125128c5d7f9f51f96971f11468b5a3f; _s_tentry=passport.weibo.com; Apache=8400782393616.642.1587956783860; ULV=1587956783866:37:10:2:8400782393616.642.1587956783860:1587869529519; SSOLoginState=1587956802; wb_view_log=1920*10801; WBStorage=42212210b087ca50|undefined; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZff3q1Zn8wWnjKyNOygDvieykp0O2_KplRH28j_q9to1s.; SUB=_2A25zo4eYDeRhGeVI7lER9CvFyD6IHXVQ2P5QrDV8PUNbmtANLVb6kW9NTAX_rJQ-xvFmL68kTzrGt1qNEOP0fNfs; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0A05ytqQN9DXjq; ALF=1619602247; wb_view_log_3653045932=1920*10801; YF-Page-G0=8a1a69dc6ba21f1cd10b039dff0f4381|1588066251|1588066251; webim_unReadCount=%7B%22time%22%3A1588066252630%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D'

web_header = {
    'Host': 's.weibo.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': web_cookie
}

# app
app_url = 'https://m.weibo.cn/api/container/getIndex'

app_cookie = '_ga=GA1.2.852180565.1582702609; ALF=1590658248; _T_WM=83354874305; XSRF-TOKEN=44bbaf; WEIBOCN_FROM=1110005030; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfZn6KksjBEOJHW7xmPqxJm-5LtCFODZwI7arSMO-Jmnk.; SUB=_2A25zo4heDeRhGeVI7lER9CvFyD6IHXVRbygWrDV6PUJbktAfLXf4kW1NTAX_rHooZMBAay4kBNpaLlitJ6SsvoWO; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=09PNBu7yGjVwjx; SSOLoginState=1588066318; MLOGIN=1; M_WEIBOCN_PARAMS=fid%3D1005051644395354%26uicode%3D10000011'

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

# res = requests.get(url=app_url, headers=app_header_cookie, params=app_param).json()
#
# print(res)

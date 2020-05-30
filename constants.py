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
web_cookie = 'SINAGLOBAL=9039371595693.941.1576205125652; _ga=GA1.2.1684815725.1577155440; UOR=,,www.baidu.com; login_sid_t=51ac8d93ad10fce8f709d86b79b04ef2; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=1846717474350.4966.1589180204867; ULV=1589180204874:39:2:1:1846717474350.4966.1589180204867:1588815714915; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfyIDuna_pXDCOAR8tgv2SGzegfHq5wgcx9Tnxu8D3rwc.; SUB=_2A25zvIdsDeRhGeVI7lER9CvFyD6IHXVQy_-krDV8PUNbmtANLUamkW9NTAX_rKDexTkYTne33fyHL2vHm3VJ5Cly; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5KzhUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0gHSVPK1aJrSPD; ALF=1620716219; SSOLoginState=1589180220; wvr=6; webim_unReadCount=%7B%22time%22%3A1589180224589%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A0%2C%22msgbox%22%3A0%7D; WBStorage=42212210b087ca50|undefined'

web_header = {
    'Host': 's.weibo.com',
    'User-Agent': ua.random,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': web_cookie
}

# app
app_url = 'https://m.weibo.cn/api/container/getIndex'

app_cookie = '_ga=GA1.2.852180565.1582702609; _T_WM=48146895564; XSRF-TOKEN=297c81; WEIBOCN_FROM=1110006030; ALF=1593404079; MLOGIN=1; SCF=AqURd7rrLbKR6K42oMeW_I-_GcEWkVQLrLN_HSe9iIZfojvE_qx_71115mTRZ853W6nd_3haKfnGw2aZahVwjgg.; SUB=_2A25z1a3hDeRhGeVI7lER9CvFyD6IHXVROTOprDV6PUJbktANLWXxkW1NTAX_rH9QFDwqXvBE22JkfPFHsCQoPvVv; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWES-MGSxVJk.S7AzfIp_iT5JpX5K-hUgL.FoecSKe7Sh-4e0z2dJLoIEXLxKBLBonL1h5LxKqL1-BLB-qLxKqLBo5L1KBLxKnLBoBLBKnLxKqLBo5LBoBt; SUHB=0xnyyaqQJufdul; SSOLoginState=1590812081; M_WEIBOCN_PARAMS=oid%3D4473768283954002%26luicode%3D20000061%26lfid%3D4473768283954002%26uicode%3D20000061%26fid%3D4473768283954002'

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

# app_param = {
#     'type': 'uid',
#     'value': 1981449674,
# }
#
# res = requests.get(url=app_url, headers=app_header_cookie, params=app_param).json()
#
# print(res)

if __name__ == '__main__':
    # import time
    #
    # def decorator(func):
    #     def punch(*args, **kwargs):
    #         print(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    #         func(*args, **kwargs)
    #     return punch
    #
    # @decorator
    # def say(name, department):
    #     print('昵称：{0} 部门：{1}上班打卡成功'.format(name, department))
    #
    # @decorator
    # def say_args(reason, **kwargs):
    #     print(reason)
    #     print(kwargs)
    #
    # say_args('张三', a='销售')

    import time
    from functools import wraps

    def decorator(func):
        @wraps(func)
        def wait(*args, **kwargs):
            time.sleep(2)
            ret = func(*args, **kwargs)
            return ret
        return wait


    @decorator
    def cal_sum():
        return 1

    a = cal_sum()
    print(a)

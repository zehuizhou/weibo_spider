import csv
import requests


param = {"entityName": "IsMuseumInfo",
         "pageNation": {"currentPageNumber": 1, "pageSize": 6000},
         "condition": {"level": "", "name": "", "id": "", "province": "", "type": ""}}

header = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'http://gl.sach.gov.cn/?from=singlemessage&isappinstalled=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

url = 'http://202.41.241.221:8769/datamanage/data/find/table'

def spider():
    need_list = []
    ret = requests.post(url=url, json=param, headers=header, proxies=proxy, timeout=6).json()
    print(ret)
    data = ret['data']['data']
    print(len(data))
    for i in data:
        level = i['level']
        name = i['name']
        province = i['province']
        type = i['type']
        museumNum = i['museumNum']
        attendance = i['attendance']
        need = [level, name, province, type, museumNum, attendance]
        need_list.append(need)
    return need_list


def save_data(file_name, data_list):
    f_name = file_name + ".csv"
    with open(f_name, "a", newline="", encoding="utf-8") as f:
        c = csv.writer(f)
        for i in data_list:
            c.writerow(i)


if __name__ == '__main__':
    data = spider()
    save_data('博物馆', data)
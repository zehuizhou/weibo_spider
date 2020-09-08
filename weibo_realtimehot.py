#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-09-08 09:26
#  @Author  : July
import pymysql
import requests
from parsel import Selector


def real_time_hot_spider():
    url = 'https://s.weibo.com/top/summary/summary?cate=realtimehot'
    header = {
        'Host': 's.weibo.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    res = requests.get(url=url, headers=header).content.decode()
    se = Selector(res)
    trs = se.xpath("//div[@class='data']/table/tbody/tr")
    items = []
    for tr in trs:
        if tr == trs[0]:
            serial_number = '0'
        else:
            serial_number = tr.xpath("./td[@class='td-01 ranktop']/text()").get('')
        key_word = tr.xpath("./td[@class='td-02']/a/text()").get('')
        times = tr.xpath("./td[@class='td-02']/span/text()").get('0')
        face = tr.xpath("./td[@class='td-02']/img/@title").get('')
        label = tr.xpath("./td[@class='td-03']/i/text()").get('')
        link = 'https://s.weibo.com/' + tr.xpath("./td[@class='td-02']/a/@href").get('')
        need = (int(serial_number), key_word, int(times), face, label, link)
        items.append(need)
    return items


def save_data(data):
    """
    CREATE TABLE `hot` (
        `id` BIGINT ( 20 ) NOT NULL AUTO_INCREMENT,
        `serial_number` INT ( 255 ) DEFAULT NULL,
        `key_word` VARCHAR ( 255 ) DEFAULT NULL,
        `times` BIGINT ( 20 ) DEFAULT NULL,
        `label` VARCHAR ( 255 ) DEFAULT NULL,
        `link` text,
        `create_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        `face` VARCHAR ( 255 ) DEFAULT NULL,
    PRIMARY KEY ( `id` )
    ) ENGINE = INNODB AUTO_INCREMENT = 52 DEFAULT CHARSET = utf8;
    """
    # 打开数据库连接，使用 cursor() 方法创建一个游标对象 cursor
    db = pymysql.connect(host="118.89.90.148", port=3307, user="root", password="123456", db="weibo")
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT INTO hot(serial_number, key_word, times, face, label, link) \
           VALUES (%s, %s, %s, %s, %s, %s)"
    try:
        # 执行sql语句
        cursor.executemany(sql, data)
        # 执行sql语句
        db.commit()
    except Exception as e:
        # 发生错误时回滚
        print(e)
        db.rollback()
    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    hot_data = real_time_hot_spider()
    save_data(data=hot_data)

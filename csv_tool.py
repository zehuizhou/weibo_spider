import pandas as pd
import re
import os

def file_name(file_dir):
    for files in os.walk(file_dir):
        print(files) #当前路径下所有非目录子文件


def update_csv_row(csv_name):
    data = pd.read_csv(csv_name, encoding='utf_8_sig', )

    data[u'微博id'] = data[u'微博id'].astype(str)
    data[u'微博链接'] = data[u'微博链接'].astype(str)

    data[u'微博id'] = data[u'微博链接'].apply(lambda x: re.findall('.*/(.*)\?refer_flag', x)[0])

    data.to_csv(csv_name, index=False, encoding='utf_8_sig')

if __name__ == '__main__':
    from os.path import abspath, dirname

    current_path = abspath(dirname(__file__))
    print(current_path)
    file_name(current_path)
    files = ['新冠病毒2-10至2-12.csv', '新冠病毒2-16.csv', '新冠病毒1-18至1-29.csv', '新冠病毒2-4至2-6.csv',
             '新冠病毒1-29.csv', '新冠病毒1-30至1-31.csv', '新冠病毒2-1至2-3.csv', '新冠病毒2-13至2-16.csv', '新冠病毒2-7至2-9.csv']

    for file in files:
        update_csv_row(current_path + '/' + file)

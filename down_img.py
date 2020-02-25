import re
import requests
import csv



def download(id, img_url):
    try:
        pic = requests.get(img_url, timeout=10)
        # 保存图片路径
        dir = 'imgs/' + str(id) + '.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        print(f"{id} 图片 {img_url} 下载成功~~")
    except requests.exceptions.ConnectionError:
        print('图片无法下载')


def start():
    with open('宽窄巷子.csv', 'r', encoding='utf_8_sig') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            id = row[0]
            image_urls = row[12].split('\n')
            for url in image_urls:
                if url != '':
                    download(id, url)


if __name__ == '__main__':
    start()

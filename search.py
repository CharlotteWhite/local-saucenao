#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import os.path
import time
import requests
from bs4 import BeautifulSoup


def GetFileList():
    file_lst = os.listdir('.')
    file_uplist = [x for x in file_lst if os.path.splitext(x)[1] == '.jpg' or os.path.splitext(x)[1] == '.png']
    while len(file_uplist) >= 150:  # Due to saucenao's ip limit
        file_uplist.pop()
    for file in file_uplist:
        Uploadimg(file)
        time.sleep(2)


def Uploadimg(file=None):
    if not file:
        return 0
    else:
        img_type = os.path.splitext(file)[1][1:].replace('jpg', 'jpeg')
        raw = open(file, 'rb')
        files = {'file': raw.read()}
        raw.close()
        url = 'http://saucenao.com/search.php'
        headers = {'Host': 'saucenao.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate',
                   'DNT': 1,
                   'Referer': 'http://saucenao.com/search.php',
                   'Connection': 'keep-alive'}
        # cookies = {'user': '', 'auth': ''}
        # proxies = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}
        params = {'file': '{file}'.format(file=file), 'Content-Type': 'image/{type}'.format(type=img_type), 'url': None, 'frame': 1, 'hide': 0, 'database': 999}
        link = requests.post(url=url, files=files, params=params, headers=headers)  # if need, add proxies and/or cookies
        content = BeautifulSoup(link.text, "html.parser")
        results = content.select('td[class=resulttablecontent]')
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        url_lst = open('result.txt', 'a+', encoding='utf-8')
        url_lst.write('\n##### ' + date + ' #####\n')
        for result in results:
            try:
                percent = result.select('div[class=resultsimilarityinfo]')[0].text
                ori_link = result.select('a[class=linkify]')[0].attrs['href']
                if float(percent[:-1]) >= 90.0:  # a magic number
                    print(file.split('\\')[-1], percent, ori_link)
                    url_lst.write(file.split('\\')[-1] + ' ' + percent + ' ' + ori_link + '\n')
                else:
                    pass
            except IndexError:  # when original image seems not found
                pass
        url_lst.close()


GetFileList()

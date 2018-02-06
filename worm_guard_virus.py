#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

cookies = {'PHPSESSID': '62f7584b550b5af9ea6060c86a0fce7f'}


def get_video_url(url):
    video_pages = []
    r = requests.get(url=url, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    # print(soup.prettify())
    video_pages_raw = soup.find_all('h2', 'entry-title')
    pattern = re.compile(r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
    for each_raw in video_pages_raw:
        # video_pages.append = pattern.match(each_raw)
        video_pages.append(each_raw.a.get('href'))
    print(video_pages)


if __name__ == '__main__':
    get_video_url('https://keenanonline.com/training-database/')

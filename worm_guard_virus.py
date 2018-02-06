#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

cookies = {'PHPSESSID': '62f7584b550b5af9ea6060c86a0fce7f',
           'wordpress_logged_in_4b3d08e309852ea3c6d29dfbcc1541a1': 'meteorshard%7C1519132290%7CPhlEOsviPS7WBbhe04n2J76zGS4g9qI41evJAR6oDO1%7C3816897a84e0a3e333f5be58954bc755be42303653473c59facf9f07105d44f2'}
video_pages_global = []


def get_video_page_url(url):
    video_pages = []
    r = requests.get(url=url, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    video_pages_raw = soup.find_all('h2', 'entry-title')
    pattern = re.compile(
        r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
    for each_raw in video_pages_raw:
        video_pages.append(each_raw.a.get('href'))
    return(video_pages)


def download_video_from(url):
    # Get iframe src
    r = requests.get(url=url, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    iframe_src = soup.find('iframe').get('src')

    # Get the file url of the video
    r = requests.session()
    headers = {
        'Referer': "https://keenanonline.com/"
    }
    video_player = r.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(r.content, "html.parser")
    pattern = re.compile(
        r'(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]')
    for each_file_url in (soup.find_all)

if __name__ == '__main__':
    # for i in range(1, 4):
    #     video_pages_global.append(get_video_page_url(
    #         'https://keenanonline.com/training-database/page/' + str(i)))
    # print(video_pages_global)

    download_video_from(
        'https://keenanonline.com/breaking-grips-finishing-knee-cut-roll-puerto-rico-seminar/')

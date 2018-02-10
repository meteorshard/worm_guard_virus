#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

proxies = {'http': 'http://127.0.0.1:1087',
           'https': 'http://127.0.0.1:1087'}

headers = {
    # "Host": "player.vimeo.com",
    # "Connection": "keep-alive",
    # "Cache-Control": "max-age=0",
    # "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,pt;q=0.6",
    "Referer": "https://keenanonline.com/"
}

cookies = {'intercom-session-c2xdup6c': 'MzU1MGtCSlAxeGxEQUVUdXQ0ekErR21EZ20vcVJnNGxxUW50ajZIUWM0Y09QWWlYMWd3blhKVURDNmZuVy9NaC0tbG9QaURZQ2NiSW05QThnN1N0ZVgrUT09--20264dc15a0df9fe9e68b00b2bf4d338da416a9e',
           'wordpress_logged_in_4b3d08e309852ea3c6d29dfbcc1541a1': 'meteorshard%7C1519298764%7C4BMNUO5pKi6q2K85AZr5t5Jm0JMxe9zxWkE7hVQCzhN%7C8b4976baaf5501e44ada9b0fa242204c69be6cda7c47a9bdabbd6cb377049ce8'}
video_pages_global = []


def get_video_page_url(url):
    video_pages = []
    r = requests.get(url=url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    video_pages_raw = soup.find_all('h2', 'entry-title')
    for each_raw in video_pages_raw:
        video_pages.append(each_raw.a.get('href'))
    return(video_pages)


def download_video_from(url):
    # Get iframe src
    s = requests.session()
    detail_page = s.get(url=url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(detail_page.content, 'html.parser')
    iframe_src = soup.find('iframe').get('src')
    print(iframe_src)

    # # Get the file url of the video
    # s = requests.session()
    #
    video_player = s.get(iframe_src, headers=headers, cookies=cookies, proxies=proxies)
    # print(video_player.content)

    pattern = re.compile(r'(?<="progressive":)\[.*?\]')
    result = list(pattern.findall(video_player.content))[0]
    # print(result)
    # print(result.split('},')[0])
    video_url = ""
    for each_video in result.split('},'):
        if (each_video.find('720p')!=-1):
            url_pattern = re.compile(r'https://.*?"')
            video_url = re.findall(url_pattern, each_video)[0][:-1]
    print(video_url)



if __name__ == '__main__':
    # for i in range(1, 4):
    #     video_pages_global.append(get_video_page_url(
    #         'https://keenanonline.com/training-database/page/' + str(i)))
    # print(video_pages_global)

    download_video_from(
        'https://keenanonline.com/lucas-leite-guard-rollover-sweep/')

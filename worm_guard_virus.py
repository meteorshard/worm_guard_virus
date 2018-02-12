#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import os
# from contextlib import closing
from bs4 import BeautifulSoup
# from classes.progressbar import ProgressBar

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


'-----按照分类解析列表页面查找播放页面地址-----'
def get_video_page_url(categories):
    # video_pages = []
    # r = requests.get(url=url, cookies=cookies, headers=headers)
    # soup = BeautifulSoup(r.content, "html.parser")
    # video_pages_raw = soup.find_all('h2', 'entry-title')
    # for each_raw in video_pages_raw:
    #     video_pages.append(each_raw.a.get('href'))
    # return(video_pages)

    video_pages = []

    for each_category in categories:
        for page_number in range(1,9999):
            index_url = 'https://keenanonline.com/category/{}/page/{}/'.format(each_category, page_number)
            print('Analyzing ' + index_url)
            r = requests.get(url=index_url, cookies=cookies, headers=headers)
            soup = BeautifulSoup(r.content, 'html.parser')

            # Check if the page exists
            valid_check = soup.find_all(id='post-404page')
            if valid_check:
                break

            video_pages_raw = soup.find_all('h2', 'entry-title fusion-post-title')
            for each_raw in video_pages_raw:
                video_pages.append(each_raw.a.get('href'))
                download_video_from(each_raw.a.get('href'))

    # print(video_pages)

'-----解析播放页面获得视频文件实际地址-----'
def download_video_from(url):
    # Check if the file already exists
    file_name_pattern = re.compile(r'(?<=https://keenanonline.com/).*?(?=/)')
    file_name = './downloaded/{}.mp4'.format(file_name_pattern.findall(url)[0])

    if os.path.exists(file_name):
        print('文件"{}"已存在不需要下载'.format(file_name))
        return -1

    # Get iframe src
    s = requests.session()
    detail_page = s.get(url=url, cookies=cookies, headers=headers)
    soup = BeautifulSoup(detail_page.content, 'html.parser')
    iframe_src = soup.find('iframe').get('src')
    print('正在从视频播放页面{}解析文件地址'.format(url))
    print('视频播放框架地址为{}'.format(iframe_src))

    # # Get the file url of the video
    video_player = s.get(iframe_src, headers=headers, cookies=cookies, proxies=proxies)

    pattern = re.compile(r'(?<="progressive":)\[.*?\]')
    result = list(pattern.findall(video_player.content))[0]

    # Seach 720p video file
    is_found = False
    for each_video in result.split('},'):
        if (each_video.find('720p')!=-1):
            url_pattern = re.compile(r'https://.*?"')
            video_url = re.findall(url_pattern, each_video)[0][:-1]
            is_found = True
            print('找到720p文件，地址是:\n{}\n-----'.format(video_url))
        elif (each_video.find('1080p')!=-1):
                url_pattern = re.compile(r'https://.*?"')
                video_url = re.findall(url_pattern, each_video)[0][:-1]
                is_found = True
                print('找到1080p文件，地址是:\n{}\n-----'.format(video_url))
        elif (each_video.find('480p')!=-1):
            url_pattern = re.compile(r'https://.*?"')
            video_url = re.findall(url_pattern, each_video)[0][:-1]
            is_found = True
            print('找到480p文件，地址是:\n{}\n-----'.format(video_url))
        elif (each_video.find('360p')!=-1):
            url_pattern = re.compile(r'https://.*?"')
            video_url = re.findall(url_pattern, each_video)[0][:-1]
            is_found = True
            print('找到360p文件，地址是:\n{}\n-----'.format(video_url))

    if is_found == False:
        print('找不到视频文件')
        return -1

    video_file = s.get(url=video_url, cookies=cookies, headers=headers)

    print('正在保存文件到{}...'.format(file_name))
    with open(file_name,'wb') as file:
        file.write(video_file.content)
    print('文件保存完成')

    # with closing(s.get(url=video_url, cookies=cookies, headers=headers, stream=True)) as video_file:
    #     chunk_size = 1024 # 单次请求最大值
    #     content_size = int(video_file.headers['content-length']) # 内容体总大小
    #     progress = ProgressBar(file_name, total=content_size,
    #                             unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
    #     with open(file_name, "wb") as file:
    #        for data in s.iter_content(chunk_size=chunk_size):
    #            file.write(data)
    #            progress.refresh(count=len(data))

if __name__ == '__main__':
    get_video_page_url(['guard','passing','submissions'])

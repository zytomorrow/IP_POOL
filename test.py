# !/usr/bin/python3
# -*- coding: utf-8 -*-


# @Time : 2019/3/28 23:54
# @Author : ZyTomorrow
# @Mail : z794672847@gmail.com
# @Github_Url : 
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                                     "Chrome/73.0.3683.86 Safari/537.36",
                       "Referer": "http://ip.zdaye.com/dayProxy.html"}

# 测试获取最大页的bs结构
# page = requests.get('http://ip.zdaye.com/dayProxy.html', headers=headers)
# max_page = BeautifulSoup(page.content).find_all('a', title='最后页')[0].contents
# print(max_page[0])

# 测试进入查找每页的title是否正确
page = requests.get('http://ip.zdaye.com/dayProxy.html', headers=headers).content
# print(page)
# title_list = BeautifulSoup(page).find_all('div', class_='title')
# for title in title_list:
#     print(title.a['href'])
# print(title_list)

# 测试ip文本split的问题
page = BeautifulSoup(requests.get('http://ip.zdaye.com/dayProxy/ip/293404.html', headers=headers).content)
# content = BeautifulSoup(page).find_all('div', class_='cont')  # 文本全在<div class='cont'>下
# ip_list = str(content.find_all('div', class_='cont')[0]).split("<br/>")[1:-1]  # 数据是<br/>换行分隔的
ip_list = str(page.find_all('div', class_='cont')[0]).split("<br/>")[1:-1]  # 数据是<br/>换行分隔的
print(ip_list)
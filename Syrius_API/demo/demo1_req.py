# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/15 10:48
# Desc:

import requests

headers = {'Cache-Control': 'private, no-cache, no-store, proxy-revalidate, no-transform', 'Connection': 'keep-alive',
           'Content-Encoding': 'gzip', 'Content-Type': 'text/html', 'Date': 'Fri, 15 Jul 2022 02:50:51 GMT',
           'Last-Modified': 'Mon, 23 Jan 2017 13:24:13 GMT', 'Pragma': 'no-cache', 'Server': 'bfe/1.0.8.18',
           'Set-Cookie': 'BDORZ=27315; max-age=86400; domain=.baidu.com; path=/', 'Transfer-Encoding': 'chunked'}

res = requests.get(url='https://www.baidu.com', headers=headers)

print(f"正文:{res.text}")
print(f"编码方式:{res.encoding}")
print(f"编码方式2:{res.apparent_encoding}")
print(f"url地址:{res.url}")
print(f"请求头:{res.headers}")
print(f"cookies:{res.cookies}")
print(f"content:{res.content}")
print(f"code:{res.status_code}")

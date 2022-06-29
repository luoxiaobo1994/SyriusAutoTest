# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/18 20:13
# Desc: requests二次封装

import requests


def requests_api(url, method='get', headers=None, data=None, json=None, cookies=None):
    if method.lower() == 'get':
        res = requests.get(url, headers=headers, data=data, json=json, cookies=cookies)
        code = res.status_code
    elif method.lower() == 'post':
        res = requests.post(url, headers=headers, data=data, json=json, cookies=cookies)
        code = res.status_code
    else:
        print(f"请求方法有误,请输入get或post.当前的输入:{method}")
        return
    body = res.text
    result = {}
    result["code"] = code
    result["body"] = body
    return result


def get(url, **kwargs):
    return requests_api(url, method='get', **kwargs)


def post(url, **kwargs):
    return requests_api(url, method='post', **kwargs)

# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/7/20 16:28
# Desc:封装接口请求

import requests


class SendRequest:
    sess = requests.session()  # session，保证一次执行的多个用例，处在同一个会话里，使用相同的cookies

    def all_request(self, method, url, **kwargs):
        res = SendRequest.sess.request(method, url, **kwargs)

        return res

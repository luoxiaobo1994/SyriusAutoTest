# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/5/18 20:13
# Desc: requests二次封装

import requests


class RequestUtil:
    sess = requests.session()

    def all_request(self, method, url, **kwargs):
        res = RequestUtil.sess.request(method, url, **kwargs)  # 请求方法要在url前面，还真是坑。
        return res


if __name__ == '__main__':
    res = RequestUtil().all_request(url="https://callonduty-cn-sqa-test.syriusdroids.com/api/sites", method='GET')
    print(res.json())

# -*- coding: utf-8 -*-
# Author: LuoXiaoBo
# 2023/4/24 19:39
# Describe: 本地调试脚本


import requests


def test_get_user():
    response = requests.get('https://jsonplaceholder.typicode.com/users/1')
    assert response.status_code == 200
    assert response.json()['username'] == 'Bret'

test_get_user()
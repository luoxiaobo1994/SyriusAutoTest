# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 11:41

import random

import requests

from base.common import read_yaml

point = list(read_yaml('locations.yaml', key='Locations').keys())


def create_task(point_num=3, site_name='Def2ixiR', repeat=99):
    base_url = "https://callonduty-cn-sqa-test.syriusdroids.com"
    create_url = f'/api/site/{site_name}/portal/createTask'  # 这里填入场地ID

    task = {
        "points": points_data(point_num),
        "repeat_times": repeat,  # 任务重复次数
        "task_name": f"{repeat}次重复任务"
    }

    res = requests.request('post', url=base_url + create_url, json=task)
    print(f"创建任务结果：{res.text}")
    # print(f"创建任务结果：{task}")


def point_task(tips='', timeout=0, point_alias='other name'):
    # 生成一个任务点信息，最小颗粒。
    return {
        "point_name": random.choice(point),
        "tips": tips if tips else "自动化任务，不要点击。不要遮挡机器人。任务第1个点",
        "timeout": timeout,
        "point_alias": point_alias  # 别名是必填项
    }


def points_data(num):
    # 生成一次任务的多个任务点任务集
    ls = []
    for i in range(num):
        ls.append(point_task())
    return ls


if __name__ == '__main__':
    create_task()
    # print(point)
    # print(point_task(tips='xxx'))
    # ls = []

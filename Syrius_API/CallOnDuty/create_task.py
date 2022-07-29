# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 11:41

import random
import time

import requests

from base.common import read_yaml
from call_cfg import cfg

base_url = cfg()['url']  # 这是测试环境的，注意切换。
file = 'locations.yaml'
point = list(read_yaml(file=file, key='Locations').keys())[1:]  # 去除待命点


def create_task():
    # create_url = f"/api/site/{cfg()['site']}/portal/createTask"  # 这里填入场地ID
    create_url = f"/api/site/Def2ixiR/portal/createTask"  # 这里填入场地ID
    repeat_times = random.randint(cfg()["repeat_min"], cfg()["repeat_max"])
    task = {
        "points": points_data(random.randint(cfg()["task_min"], cfg()["task_max"])),
        "repeat_times": repeat_times,  # 任务重复次数
        "task_name": f"{repeat_times}次重复任务"
    }

    url = base_url + create_url
    print(f"url：{url}")
    res = requests.request('post', url=url, json=task)
    print(f"创建任务结果：{res.text}\n")
    print(f"创建的任务详情：{task}")


def point_task(tips='', timeout=0):
    # 生成一个任务点信息，最小颗粒。
    return {
        "point_name": random.choice(point),
        "tips": str(random.choice(cfg()['tips'])),
        "timeout": timeout,
        "point_alias": random.choice(cfg()["other_name"])  # 别名是必填项
    }


def points_data(num):
    # 生成一次任务的多个任务点任务集
    ls = []
    for i in range(num):
        ls.append(point_task())
    return ls


def time_task(timmeout=90):
    while True:
        create_task()
        time.sleep(timmeout)


if __name__ == '__main__':
    # create_task()
    time_task()
    # print(point)
    # print(cfg()["site"])

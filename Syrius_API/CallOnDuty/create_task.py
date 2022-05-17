# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/9/22 11:41

import requests, json

base_url = "https://call-on-duty-test.syriusdroids.com"
create_url = '/api/site/{}/portal/createTask'.format('PwQnQb69')  # 这里填入场地ID


def create_task():
    task = {
        "points":
            [
                {
                    "point_name": "PICKING_0001",
                    "tips": "自动化任务，不要点击。不要遮挡机器人。任务第1个点",
                    "timeout": 0,
                    "point_alias": ""  # 别名是必填项
                },
                {
                    "point_name": "PICKING_0002",  # 点位名称
                    "tips": "自动化任务，不要点击。不要遮挡机器人。",  # 语音提示文本
                    "timeout": 0,  # 超时时间,暂时没什么用.
                    "point_alias": ""  # 别名
                },
                {
                    "point_name": "PICKING_0003",  # 点位名称
                    "tips": "自动化任务，不要点击。不要遮挡机器人。",  # 语音提示文本
                    "timeout": 0,  # 超时时间,暂时没什么用.
                    "point_alias": ""  # 别名
                },
                {
                    "point_name": "PICKING_0004",  # 点位名称
                    "tips": "自动化任务，不要点击。不要遮挡机器人。",  # 语音提示文本
                    "timeout": 0,  # 超时时间,暂时没什么用.
                    "point_alias": ""  # 别名
                },
                {
                    "point_name": "PICKING_0005",
                    "tips": "自动化任务，不要点击。不要遮挡机器人。",
                    "timeout": 0,
                    "point_alias": ""
                }
            ],
        "repeat_times": 99,  # 任务重复次数
        "task_name": "99次重复任务"
    }

    res = requests.request('post', url=base_url + create_url, json=task)
    print(f"创建任务结果：{res.text}")


if __name__ == '__main__':
    create_task()

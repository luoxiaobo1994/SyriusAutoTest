#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Kumar Ganduri // kumar@syriusrobotics.com
# vim:fenc=utf-8

"""

"""

import dbus
import time
import sched
import argparse
import json


def travel(p1, p2):
    print(p1, p2)
    # return None
    move = """{
        "action":"post",
        "type":"json",
        "route":"/buzzard/navigation/move",
        "endpoint":"create",
        "payload":{
            "id": "string",
            "routes":[{
                "from": "%s",
                "to": "%s"
            }],
            "offset":500
        }
    }"""
    p1_to_p2 = move % (p1, p2)
    p2_to_p1 = move % (p2, p1)

    bus = dbus.SystemBus()
    nav = bus.get_object("syrius.robot.navigation", "/syrius/robot/navigation")
    try:
        print("%s to %s" % (p1, p2))
        nav.request(p1_to_p2, dbus_interface="syrius.robot.navigation")
    except dbus.DBusException as e:
        time.sleep(5)
        print(e)


def status():
    # return True
    status_check = """{
        "action":"post",
        "type":"json",
        "route":"/buzzard/navigation/move",
        "endpoint":"status",
        "payload": ""
    }"""
    bus = dbus.SystemBus()
    nav = bus.get_object("syrius.robot.navigation", "/syrius/robot/navigation")
    try:
        # get position status, return json
        reply = nav.request(status_check, dbus_interface="syrius.robot.navigation")
        # print(reply)
        x = json.loads(reply)
        reply = x["status"]  # 返回两个状态：'OK','failed'
        print("dbus status reply -" + reply)
        if reply == "OK":  # position is OK
            return True
    except dbus.DBusException as e:  # maybe session err
        time.sleep(5)
        print(e)


def do_something():
    print("Doing stuff...")
    s.enter(1, 1, status, ())


if __name__ == '__main__':
    # travel("origin","CONTAINER_BIND_0001")
    parser = argparse.ArgumentParser()
    parser.add_argument('--nargs', nargs='+')
    runner = 0
    for _, value in parser.parse_args()._get_kwargs():
        if value is not None:
            print('Goals -', value)
            goal_list = value
    try:
        while True:
            print('test')
            s = sched.scheduler(time.time, time.sleep)  # 生成调度器
            s.enter(3, 1, status, ())  # 延迟，优先级，调度函数，调度函数所需的参数。
            if status():
                print('Robot State is Free')
                if len(goal_list) == 0:
                    travel("origin", goal_list[0])
                else:
                    travel("origin", goal_list[runner])
                    if runner < len(goal_list) - 1:
                        runner += 1
                    else:
                        print('Finished all tasks')
                        break
            else:
                print('Robot state is not Free')
            s.run()  # 运行调度器
    except KeyboardInterrupt:
        print('Keyboard Interruption')

# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/6 21:27

# ! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""

"""

import time

import dbus


def travel(p1, p2):
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


if __name__ == '__main__':
    travel("origin", "STANDBY_0001")

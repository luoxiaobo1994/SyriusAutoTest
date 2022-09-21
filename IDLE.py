# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

from utils.connect_linux import Linux_command

cmd = "/home/syrius/test_env/bin/python /home/syrius/test_env/bin/yakut call 5 1:dinosaurs.NodeManage.1.0 '{permit_broadcast: 0, permit_request: 1}'"
res = Linux_command(ip="10.2.16.200", command=cmd, port=9530)
print(res)

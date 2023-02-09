# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

ls = ['speed_picker', '紧急拣货中', '订单编号',
      '20230203173052885PQqUbgTnwyAYiaCct9K0O6SJed2fxs4jHZ',
      'A03010103', '接口订单:마이크로소프트 서버 호스트 I7 12800QD', 'picking_code.8cfdd8bd',
      '2600473D165PWb1S9m58', '×5', 'ic_btn_scan.74060d4d', '扫货品/输入']

with open('tempData/writelog.txt', 'a', encoding='utf8') as f:
    for i in ls:
        print(i)
        f.write(i)

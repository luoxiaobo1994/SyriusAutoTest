# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

students = {
    "1": {'name': '张三', '语文': 88, '数学': 75, '英语': 65},
    "2": {'name': '李四', '语文': 95, '数学': 55, '英语': 85},
    "3": {'name': '韩梅梅', '语文': 66, '数学': 66, '英语': 70},
    "4": {'name': '李雷', '语文': 61, '数学': 95, '英语': 75},
    "5": {'name': '尼古拉斯·赵四', '语文': 72, '数学': 85, '英语': 55}
}

avg_math = sum([score['语文'] for score in students.values()]) / len(students.values())
avg_cn = sum([score['数学'] for score in students.values()]) / len(students.values())
avg_en = sum([score['英语'] for score in students.values()]) / len(students.values())
print(avg_math)
print(avg_cn)
print(avg_en)

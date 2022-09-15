# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

"""
题目：将学生成绩低于科目平均分的信息提取出来。
"""

students = {
    "1": {'name': '张三', '语文': 88, '数学': 75, '英语': 65},  # 学号做主键，内容包含信息。
    "2": {'name': '李四', '语文': 95, '数学': 55, '英语': 85},
    "3": {'name': '韩梅梅', '语文': 66, '数学': 66, '英语': 70},
    "4": {'name': '李雷', '语文': 61, '数学': 95, '英语': 75},
    "5": {'name': '尼古拉斯·赵四', '语文': 72, '数学': 85, '英语': 55}
}
# 取出所有学生里的信息，拿到数学成绩。并求平均值。
avg_math = sum(map(lambda x: x['数学'], students.values())) / len(students)
avg_cn = sum(map(lambda x: x['语文'], students.values())) / len(students)
avg_en = sum(map(lambda x: x['英语'], students.values())) / len(students)

score = {'语文': avg_cn, '数学': avg_math, '英语': avg_en}  # 各科平均成绩汇总

for id, info in students.items():  # 学生 ： 信息
    for project, avg in score.items():  # 科目 ： 平均分
        if info[project] < avg:  # 学生的科目成绩低于该科目信息，则打印信息。
            print(f"{info['name']}的{project}成绩：{info[project]}，低于{project}平均分：{avg}")

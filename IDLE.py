# -*- coding:utf-8 -*-
# Author:Luoxiaobo
# Time: 2021/7/6 23:09

class Student:

    def __init__(self, student_list):
        self.student = student_list


student = Student(['小明', '小红', '张三'])

students = student.student
print(students)

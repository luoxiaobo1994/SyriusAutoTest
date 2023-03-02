# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/2 14:31
# Desc: 自动抓取Jira数据。

from Python_Jira import JiraTool
from utils.read_yaml import read_yaml

jira = JiraTool()

config = read_yaml('jira_config.yml')
print(config['month'][2023.02])

BUG_info = {
    'total': 0,
    '致命': 0,
    '严重': 0,
    '一般': 0,
    '建议': 0,
    '致命-解决数量': 0,
    '严重-解决数量': 0,
    '已解决': 0,
    '未解决': 0,
    '无分析评论': 0,
    'GoGoReady缺陷': 0,
    'MoveBase缺陷': 0,
    '碰撞缺陷': 0,
    'MCU缺陷': 0,
    'JingleBell缺陷': 0,
    'OTA缺陷': 0,
    'PQCP缺陷': 0,
    'FPCHECKER缺陷': 0,
    'L4T缺陷': 0,
    '未解决的工程师': {},  # 问题未解决，挂在工程师头上的问题。
    'reporter': {},  # 缺陷上报人
    'bug_versions': {},  # 问题版本合集
}


def issue_for_date(date_interval: tuple):
    # date_interval = ('2023-02-01', '2023-02-28') 这种格式
    jql = f"project = SQA AND issuetype = Bug AND created >= {date_interval[0]} AND created <= {date_interval[1]}"
    return jira.search_jira_jql(jql=jql)  # 返回的是可迭代对象，对象内容是缺陷的key，如：SQA-5457

def issue_for_level(level):
    pass



def process_all_issue():
    for i in issue_for_date(('2023-02-01', '2023-02-28'))[:10]:
        print(i)


# info = jira.get_issuefields('SQA-5422')
# comment = jira.get_comments('SQA-5422')
# print(info)
# print(info['summary'])
# print(info['assignee'])
# print(info['status'])
# print(info['issuetype'])
# print(info['reporter'])
# print(info['labels'])
# print(info['versions'])
# print(info['fixVersions'])
# print(comment)
# print(jira.get_issuefields('SQA-5422'))
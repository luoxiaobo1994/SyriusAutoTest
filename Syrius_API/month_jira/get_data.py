# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/27 15:19
# Desc: 获取月度Jira数据。


import base64
from jira import JIRA
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor


# url = 'https://jira.syriusrobotics.cn/issues/?jql=project%20%3D%20SQA%20AND%20issuetype%20%3D%20Bug%20AND%20created%20%3E%3D%202023-02-01%20AND%20created%20%3C%3D%202023-02-28'
#
# def get_bug_list(bug):
#     if bug.get('inwardIssue'):
#         bug_key = bug['inwardIssue']['key']
#         bug_info = jr.issue(bug_key)
#
#         info = {
#             'assignee': bug_info.fields.assignee.displayName,
#             'creator': bug_info.fields.reporter.displayName
#         }
#
#         issue_item = {
#             bug_key:info
#         }
#         return issue_item
#     return {'抓取异常'}
#
# jr = JIRA(url,basic_auth=('luoxiaobo@syriusrobotics.com','Lxb@12345'))
# issues = jr.issue('jiracode')
#
# print(issues.raw)

class JiraObj():

    def __init__(self, bug_style='', project_type=''):
        # Jira登录首页
        self.server = 'https://jira.syriusrobotics.cn/'
        # 登录信息
        self.basic_auth = ('luoxiaobo@syriusrobotics.com','Lxb@2023')
        self.jiraClient = JIRA(server=self.server,basic_auth=self.basic_auth)

JiraObj()
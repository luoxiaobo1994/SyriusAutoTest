# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/8/10 15:49
# Desc:

from jira import JIRA

# 创建 Jira 客户端连接
jira = JIRA(server='https://syrius.atlassian.net/',auth=('luoxiaobo@syriusrobotics.com','Lxb@20230713'))
boards = jira.boards()
print(boards)
# 获取项目信息
projects = jira.projects()
print(projects)
for project in projects:
    print('项目Key:', project.key)
    print('项目名称:', project.name)

# 获取指定项目的问题
# issues = jira.search_issues('project=SQASZ')
# for issue in issues:
#     print('问题Key:', issue.key)
#     print('问题摘要:', issue.fields.summary)

# 其他操作，如创建、更新、删除问题等，请参考官方文档：https://jira.readthedocs.io/

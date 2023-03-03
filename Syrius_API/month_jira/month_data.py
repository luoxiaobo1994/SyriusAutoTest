# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/2 14:31
# Desc: 自动抓取Jira数据。

from Python_Jira import JiraTool
from utils.read_yaml import read_yaml

jira = JiraTool()

config = read_yaml('jira_config.yml')
# print(config['month'][2023.02])

BUG_info = {
    'total': 0,
    '致命': 0,
    '严重': 0,
    '一般': 0,
    '提示': 0,
    '致命-解决数量': 0,
    '严重-解决数量': 0,
    '致命-无分析评论': 0,  # 针对未解决的问题
    '严重-无分析评论': 0,  # 针对未解决的问题
    'GoGoReady缺陷': 0,
    'MoveBase缺陷': 0,
    '碰撞缺陷': 0,
    '算法缺陷': 0,
    'MCU缺陷': 0,
    'JingleBell缺陷': 0,
    'OTA缺陷': 0,
    'PQCP缺陷': 0,
    'kuafu缺陷': 0,
    'FPCHECKER缺陷': 0,
    'clearjanitor缺陷': 0,
    'PonyRunner缺陷': 0,
    '无效缺陷': 0,
    '时钟缺陷': 0,
    '其他类型缺陷': 0,
    '待关闭缺陷': 0,
    'FCT缺陷': 0,
    'L4T缺陷': 0,
    '未解决的工程师': {},  # 问题未解决，挂在工程师头上的问题。
    'reporter': {},  # 缺陷上报人
    'bug_versions': {},  # 问题版本合集
    'all_labels': {},  # 所有的标签。 可以搞一个词云。
    'all_summery': [],  # 所有的标题，也可以搞一个词云
}


def issue_for_date(date_interval):
    project = "project = SQA AND issuetype = Bug"
    date = f"created >= {date_interval[0]} AND created <= {date_interval[1]}"
    jql = f"{project} AND {date}"
    total = jira.search_jira_jql(jql=jql)
    BUG_info['total'] = len(total)
    return total  # 返回的是可迭代对象，对象内容是缺陷的key，如：SQA-5457


all_bug_key = issue_for_date(config['month'][2023.02])


def issue_for_level(date_interval):
    # 月度区间内，各等级的缺陷。
    project = "project = SQA AND issuetype = Bug"
    date = f"created >= {date_interval[0]} AND created <= {date_interval[1]}"
    state_sovled = "status in (Aborted, Rejected, Disapear, Done)"
    critical_bug = f'{project} AND 问题级别 = 致命 AND {date}'
    BUG_info['致命'] = len(jira.search_jira_jql(jql=critical_bug))
    major_bug = f'{project} AND 问题级别 = 严重 AND {date}'
    BUG_info['严重'] = len(jira.search_jira_jql(jql=major_bug))
    general_bug = f"{project} AND 问题级别 = 一般 AND {date}"
    BUG_info['一般'] = len(jira.search_jira_jql(jql=general_bug))
    minor_bug = f"{project} AND 问题级别 = 提示 AND {date}"
    BUG_info['提示'] = len(jira.search_jira_jql(jql=minor_bug))
    done_critical = f"{project} AND {state_sovled} AND 问题级别 = 致命 AND {date}"
    BUG_info['致命-解决数量'] = len(jira.search_jira_jql(jql=done_critical))
    done_major = f"{project} AND {state_sovled} AND 问题级别 = 严重 AND {date}"
    BUG_info['严重-解决数量'] = len(jira.search_jira_jql(jql=done_critical))


def process_issue_label(date_interval):
    project = "project = SQA AND issuetype = Bug"
    date = f"created >= {date_interval[0]} AND created <= {date_interval[1]}"
    state_sovled = "status = open"
    critical_bug_list = jira.search_jira_jql(f'{project} AND {state_sovled} AND 问题级别 = 致命 AND {date}')
    for i in critical_bug_list:
        bug_info = jira.get_issuefields(i)


def jira_comment(date_interval):
    project = "project = SQA AND issuetype = Bug"
    date = f"created >= {date_interval[0]} AND created <= {date_interval[1]}"
    state_sovled = "status = open"
    critical_bug_list = jira.search_jira_jql(f'{project} AND {state_sovled} AND 问题级别 = 致命 AND {date}')
    for bug in critical_bug_list:
        comment = jira.get_comments(bug)
        if comment:
            pass
        else:
            BUG_info['致命-无分析评论'] += 1
    major_bug_list = jira.search_jira_jql(f'{project} AND {state_sovled} AND 问题级别 = 严重 AND {date}')
    for bug in major_bug_list:
        comment = jira.get_comments(bug)
        if comment:  # 有评论
            # print()
            pass
        else:
            BUG_info['严重-无分析评论'] += 1


def bug_labels():
    for bug in all_bug_key:
        labels = jira.get_issuelabels(bug)  # 得到标签列表。 如：['2302', 'MoveBase5465', '时钟同步']
        for label in labels:
            if label not in BUG_info['all_labels']:
                BUG_info['all_labels'][str(label)] = 1  # 强制将标签转字符串，即使如上得到的已经是字符串。
            else:
                BUG_info['all_labels'][str(label)] += 1
    for label in BUG_info['all_labels']:  # 处理获取到的所有标签
        current_label = label  # 当前的实际标签
        num = BUG_info['all_labels'][current_label]  # 当前标签，有多少个数。
        label = label.lower()  # 转小写。方便筛选
        if 'ggr' in label:
            BUG_info['GoGoReady缺陷'] += num  # 加上当前标签的数值
        elif 'movebase' in label:
            BUG_info['MoveBase缺陷'] += num
        elif 'kuafu' in label:
            BUG_info['kuafu缺陷'] += num
        elif 'pqcp' in label:
            BUG_info['PQCP缺陷'] += num
        elif 'l4tvendor' in label or 'l4t_vendor' in label:
            BUG_info['L4T缺陷'] += num
        elif 'fpchecker' in label:
            BUG_info['FPCHECKER缺陷'] += num
        elif 'clearjanitor' in label:
            BUG_info['clearjanitor缺陷'] += num
        elif 'mcu' in label:
            BUG_info['MCU缺陷'] += num
        elif 'ponyrunner' in label:
            BUG_info['PonyRunner缺陷'] += num
        elif 'fct' in label:
            BUG_info['FCT缺陷'] += num
        elif 'algorithm' in label:
            BUG_info['算法缺陷'] += num
        elif 'collision' in label:
            BUG_info['算法缺陷'] += num
        elif 'notabug' in label:
            BUG_info['无效缺陷'] += num
        elif 'robeclose' in label:
            BUG_info['待关闭缺陷'] += num
        elif 'time' in label:
            BUG_info['时钟缺陷'] += num
        elif 'ota' in label:
            BUG_info['OTA缺陷'] += num
        else:
            BUG_info['其他类型缺陷'] += num


def bug_title():
    for bug in all_bug_key:
        summery = jira.get_summary(bug)
        BUG_info['all_summery'].append(summery)


def bug_assignee():
    for bug in all_bug_key:
        assignee = jira.get_assignee(bug)
        if assignee not in BUG_info['未解决的工程师']:
            BUG_info['未解决的工程师'][assignee] = 1
        else:
            BUG_info['未解决的工程师'][assignee] += 1


def bug_reporter():
    for bug in all_bug_key:
        # print(f"bug-key：{bug}")
        reporter = jira.get_issuefields(bug)
        name = str(reporter['reporter'])
        # print(f'-------------- {name}  --  {BUG_info["reporter"]}  ------------')
        if name not in BUG_info['reporter']:
            BUG_info['reporter'][name] = 1
        else:
            BUG_info['reporter'][name] += 1


def main():
    date = config['month'][2023.02]
    issue_for_date(date)
    issue_for_level(date)
    jira_comment(date)
    bug_labels()
    bug_title()
    bug_assignee()
    bug_reporter()
    print(BUG_info)


main()

# info = jira.get_issuefields('SQA-5422')
# print(info)
# lebel = jira.get_issuelabels('SQA-5422')
# print(lebel)
# comment = jira.get_comments('SQA-5422')
# comment2 = jira.get_comments('SQA-5425')
# print(comment)
# print(comment2)
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

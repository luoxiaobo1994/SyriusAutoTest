# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/2 14:31
# Desc: 自动抓取Jira数据。

from datetime import date, timedelta

import yaml

from Python_Jira import JiraTool

jira = JiraTool()

def last_month_start_end_day():
    this_first = date.today().replace(day=1)  # 这个月1号
    prev_last = this_first - timedelta(days=1)  # 上个月最后一天。
    prev_first = prev_last.replace(day=1)  # 上个月1号。
    return prev_first, prev_last


start_date, end_date = last_month_start_end_day()
print(f"本次Jira数据获取的时间区间是：{start_date}~{end_date}。请注意时间区间的准确性。")

BUG_info = {
    'total': 0,
    '致命': 0,
    '严重': 0,
    '一般': 0,
    '提示': 0,
    '创建日期': {},  # 所有Jira的创建日期
    '致命-解决数量': 0,
    '严重-解决数量': 0,
    '一般-解决数量': 0,
    '提示-解决数量': 0,
    '致命-无分析评论': 0,  # 针对未解决的问题
    '严重-无分析评论': 0,  # 针对未解决的问题
    'GoGoReady缺陷': 0,
    'MoveBase缺陷': 0,
    '碰撞缺陷': 0,
    '算法缺陷': 0,
    '移动缺陷': 0,
    '建图缺陷': 0,
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


def issue_for_date():
    project = "project = SQA AND issuetype = Bug"
    date = f"created >= {start_date} AND created <= {end_date}"
    jql = f"{project} AND {date}"
    total = jira.search_jira_jql(jql=jql)
    BUG_info['total'] = len(total)
    return total  # 返回的是可迭代对象，对象内容是缺陷的key，如：SQA-5457


all_bug_key = issue_for_date()


def issue_for_level():
    # 月度区间内，各等级的缺陷。
    project = "project = SQA AND issuetype = Bug"
    date = f"created >= {start_date} AND created <= {end_date}"
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
    BUG_info['严重-解决数量'] = len(jira.search_jira_jql(jql=done_major))
    done_general = f"{project} AND {state_sovled} AND 问题级别 = 一般 AND {date}"
    BUG_info['一般-解决数量'] = len(jira.search_jira_jql(jql=done_general))
    done_minor = f"{project} AND {state_sovled} AND 问题级别 = 提示 AND {date}"
    BUG_info['提示-解决数量'] = len(jira.search_jira_jql(jql=done_minor))


def process_issue_label(date_interval):
    project = "project = SQA AND issuetype = Bug"
    date = f"created >= {date_interval[0]} AND created <= {date_interval[1]}"
    state_sovled = "status = open"
    critical_bug_list = jira.search_jira_jql(f'{project} AND {state_sovled} AND 问题级别 = 致命 AND {date}')
    for i in critical_bug_list:
        bug_info = jira.get_issuefields(i)


def jira_comment():
    project = "project = SQA AND issuetype = Bug"
    date = f"created >= {start_date} AND created <= {end_date}"
    state_sovled = "status = open"
    critical_bug_list = jira.search_jira_jql(f'{project} AND {state_sovled} AND 问题级别 = 致命 AND {date}')
    for bug in critical_bug_list:
        # 致命问题
        comment = jira.get_comments(bug)
        if comment:
            pass
        else:
            BUG_info['致命-无分析评论'] += 1
    major_bug_list = jira.search_jira_jql(f'{project} AND {state_sovled} AND 问题级别 = 严重 AND {date}')
    for bug in major_bug_list:
        # 严重问题
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
            BUG_info['碰撞缺陷'] += num
            BUG_info['算法缺陷'] += num
        elif 'mapping' in label:
            BUG_info['建图缺陷'] += num
            BUG_info['算法缺陷'] += num
        elif 'move_issue' in label:
            BUG_info['移动缺陷'] += num
            BUG_info['算法缺陷'] += num
        elif 'notabug' in label:
            BUG_info['无效缺陷'] += num
        elif 'tobeclose' in label:
            BUG_info['待关闭缺陷'] += num
        elif 'time' in label:
            BUG_info['时钟缺陷'] += num
        elif 'ota' in label:
            BUG_info['OTA缺陷'] += num
        elif 'jinglebell' in label:
            BUG_info['JingleBell缺陷'] += num
            BUG_info['MoveBase缺陷'] += num
        else:
            BUG_info['其他类型缺陷'] += num


def bug_title():
    for bug in all_bug_key:
        summery = jira.get_summary(bug)
        BUG_info['all_summery'].append(summery)


def bug_assignee():
    for bug in all_bug_key:
        assignee = jira.get_assignee(bug)
        if assignee not in BUG_info['未解决的工程师']:  # 这个工程师还未收录。
            jql = f'project = SQA AND issuetype = Bug AND status in (open, "IN PROGRESS", "NEED VERIFY", POSTPONE) ' \
                  f'AND created >= {start_date} AND created <= {end_date} AND assignee in ({assignee})'
            # print(jql)
            issue_num = jira.search_jira_jql(jql=jql)
            if issue_num == 0:
                pass
            else:
                BUG_info['未解决的工程师'][assignee] = len(issue_num)
        else:
            pass


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


def created_date():
    for bug in all_bug_key:
        issue_info = jira.get_issuefields(bug)
        created_date = str(issue_info['created'].split('T')[0])  # '2023-02-17' 这样的，拿去画图，会很密
        created_date = created_date[5:]  # 把年和一个-去掉。
        if created_date not in BUG_info['创建日期']:
            BUG_info['创建日期'][created_date] = 1
        else:
            BUG_info['创建日期'][created_date] += 1


def write_yaml(file, data=None, mode='a'):
    if file and isinstance(data, dict):
        with open(file, encoding='utf-8', mode=mode) as f:
            yaml.dump(data, stream=f, allow_unicode=True)

    else:
        print(f"数据写入yaml文件：。请检查输入文件路径或存入的数据类型是否是键值对。")


def main():
    # 这一步是获取所有数据。
    issue_for_date()
    issue_for_level()
    jira_comment()
    bug_labels()
    bug_title()
    bug_assignee()
    bug_reporter()
    created_date()
    # print(BUG_info)
    write_yaml(file='jira_data.yml', data=BUG_info, mode='w')


main()

# info = jira.get_issuefields('SQA-5422')
# print(info['created'].split('T')[0])
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

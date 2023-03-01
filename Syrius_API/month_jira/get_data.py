# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/2/27 15:19
# Desc: 获取月度Jira数据。

import seaborn as sns

from matplotlib import pyplot as plt

from base.common import read_yaml

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题

data = read_yaml('month_data.yml')
# 缺陷分类
month_issues = [data[i] for i in data][-2]  # 只拿最后一个月的。月度总数据
P0 = month_issues['致命']  # 致命问题的数据，数据如：{'total': 1, 'solve': 1, 'unsole': 1, 'unanalyzed': 1}
P1 = month_issues['严重']
P2 = month_issues['一般']
P3 = month_issues['提示']

every_issue_total = [month_issues[i]['total'] for i in month_issues]
print(every_issue_total)
issue_rank = ['致命', '严重', '一般', '提示']
issue_state = ['完成', '开放', '未分析', '拒绝']


# 画柱状图
def issue_bar():
    sns.set_style({'font.sans-serif': ['simhei', 'Arial']})
    plt.bar(issue_rank, every_issue_total)
    plt.ylabel('缺陷数量(个)')
    plt.title("各等级缺陷数量分布图")
    plt.show()


# 画饼图：各等级问题占比情况。
def issue_pie():
    plt.pie(every_issue_total, labels=issue_rank, autopct='%1.2f%%', startangle=90)
    plt.ylabel('缺陷数量(个)')
    plt.title("各等级缺陷占比分布图")
    plt.show()

# 画饼图：缺陷在各模块的占比。
def issue_module():
    pass


# 画柱状图：致命，严重缺陷解决情况
def solve_bar():
    totalWidth = 0.8  # 一组柱状图的宽度
    labelNums = 2  # 一组的两种种类，所有缺陷/已解决缺陷
    barWidth = totalWidth / labelNums  # 小柱宽度
    seriesNums = 2  # 两组数据，只管致命和严重缺陷。
    plt.bar([x for x in range(seriesNums)], [P0['total'], P1['total']], label='缺陷总数', width=barWidth)  # 缺陷总数
    plt.bar([x + barWidth for x in range(seriesNums)], [P0['solve'], P1['solve']], label='已解决',
            width=barWidth)  # 已解决数量
    plt.xticks([x + barWidth / 2 * (labelNums - 1) for x in range(seriesNums)], ["致命", "严重"])
    plt.xlabel("缺陷等级")
    plt.ylabel("缺陷数量")
    plt.title("致命/严重缺陷解决情况")
    plt.legend()
    plt.show()

# 画折线图


if __name__ == '__main__':
    issue_pie()
    issue_bar()
    solve_bar()
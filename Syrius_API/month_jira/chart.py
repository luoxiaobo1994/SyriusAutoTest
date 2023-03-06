# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/6 10:06
# Desc: 绘图
import yaml
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud

plt.rcParams["font.sans-serif"] = ["SimHei"]  # 设置字体
plt.rcParams["axes.unicode_minus"] = False  # 该语句解决图像中的“-”负号的乱码问题


def auto_text(rects):
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height),
                     xy=(rect.get_x() + rect.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords='offset points',
                     ha='center', va='bottom'  # 水平方向和垂直方向
                     )


def issue_pie(total, level, ylabel='', chart_name='图标名称'):
    plt.pie(total, labels=level, autopct='%1.2f%%', startangle=90)
    # auto_text(rect1)
    plt.ylabel(ylabel)
    plt.title(chart_name)
    plt.show()


def issue_bar(every_level, level, xlabel='y轴名称', ylabel='y轴名称', title='图标名称'):
    rect1 = plt.bar(level, every_level)
    auto_text(rect1)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def two_bar(total_list, solve_list, xticks, xlabel_name='缺陷等级', ylabel_name="缺陷数量", title='缺陷解决情况',
            label_heigh='缺陷总数', label_lower='已解决'):
    totalWidth = 0.8  # 一组柱状图的宽度
    labelNums = len(total_list)  # 一组的两种种类，所有缺陷/已解决缺陷
    barWidth = totalWidth / labelNums  # 小柱宽度
    seriesNums = len(total_list)  #
    rect1 = plt.bar([x for x in range(seriesNums)], total_list, label=label_heigh, width=barWidth)  # 缺陷总数
    rect2 = plt.bar([x + barWidth for x in range(seriesNums)], solve_list, label=label_lower,
                    width=barWidth)  # 已解决数量
    plt.xticks([x + barWidth / 2 * (labelNums - 1) for x in range(seriesNums)], xticks)
    # plt.yticks([0,max(total_list)],[0,max(total_list)])
    auto_text(rect1)
    auto_text(rect2)
    plt.xlabel(xlabel_name)
    plt.ylabel(ylabel_name)
    plt.title(title)
    plt.legend()
    plt.show()


def date_plot(x, y, label='', xlabel_name='', ylabel_name='', title=''):
    # 月内创建jira频率。
    plt.plot(x, y, linewidth=1, marker='o', label=label)
    for a, b in zip(x, y):
        plt.text(a, b, b, ha='center', va='bottom', fontsize=20)
    plt.xlabel(xlabel_name)
    plt.ylabel(ylabel_name)
    plt.title(title)
    plt.show()


def read_yaml(file, key=None):
    with open(file, encoding='utf-8') as f:
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        if key:
            return value[key] if value[key] else f'No value: {key}'
        return value


def chart():
    # 从本地获取数据
    data = read_yaml('jira_data.yml')
    # print(type(data), data)
    # 将数据绘图
    issue_level = ['致命', '严重', '一般', '提示']
    issue_num = [data[key] for key in issue_level]  # 各级别缺陷
    solved_issue = [data[key + '-解决数量'] for key in issue_level]  # 各级别解决缺陷
    no_coment = {'致命': data['致命-无分析评论'], '严重': data['严重-无分析评论']}
    created_date = data['创建日期']  # 这直接是一个好的字典。
    issue_state = ['完成', '开放', '未分析', '拒绝']
    # 各等级问题解决情况
    # two_bar(total_list=issue_num, solve_list=solved_issue, xticks=issue_level,title='缺陷解决情况')
    # 各等级问题占比情况
    # issue_pie(total=issue_num,level=issue_level,ylabel='',chart_name='各等级缺陷分布比例')
    # 问题模块
    issue_type = [key for key in data if key.endswith('缺陷')]
    issue_type_bum = [data[key] for key in issue_type]
    # print(issue_type,issue_type_bum)
    # issue_pie(total=issue_type_bum, level=issue_type, ylabel='', chart_name='问题类型分布')
    # 构建日期分布
    # date_plot(x=created_date.keys(), y=created_date.values(), xlabel_name='日期', ylabel_name='创建缺陷数量',
    #           title='月度每日创建缺陷数量')
    # 致命。严重分析情况
    open_issue = ['致命', '严重']
    open_issue_num = [data['致命'] - data['致命-解决数量'], data['严重'] - data['严重-解决数量']]
    no_coment_issue = [data['致命-无分析评论'], data['严重-无分析评论']]
    # two_bar(open_issue_num, no_coment_issue, open_issue, label_heigh='未解决数量', label_lower='未解决-且无分析',
    #         title='致命/严重开放问题分析情况')
    # 未解决问题的责任工程师
    un_solved_engineer = data['未解决的工程师'].keys()
    un_solved_num = [data['未解决的工程师'][key] for key in un_solved_engineer]
    # issue_bar(un_solved_num, un_solved_engineer, xlabel='工程师', ylabel='未解决缺陷数量', title='未解决缺陷指派情况')
    # Jira创建情况
    reporter = data['reporter'].keys()
    report_num = [data['reporter'][key] for key in reporter]
    issue_bar(report_num, reporter, xlabel='工程师', ylabel='创建Jira数量', title='Jira创建情况')

def word_cloud():
    data = read_yaml('jira_data.yml')
    text = ','.join(data['all_summery'])
    text = text.replace('【','').replace('】','')
    words = ''.join(jieba.lcut(text))
    words_cloud = WordCloud(font_path = "C:\Windows\Fonts\SIMYOU.TTF",
                            width=1200,height=800,max_font_size=80
                            ).generate(words)
    words_cloud.to_file('词云.jpg')
    # print(words)


if __name__ == '__main__':
    # chart()
    word_cloud()

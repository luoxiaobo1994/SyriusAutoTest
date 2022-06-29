# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/1/9 18:35

"""
目标:一键生成一个自定义的订单.需要自定义的内容:
    1.订单ID,
        指定要生成多少个订单.
        指定一个开始数.
        指定一个相同的ID需要几行.
    2.符合场地需求的货架格式.
    3.自定义的商品名称.
    4.随机拣货数值.
    5.可能新增的字段.
"""

import random
import string
import time

import pandas


def file_time():
    now_time = time.localtime()  # [2020, 11, 30, 12, 3, 5, 0, 335, 0]
    # date_1 = '_'.join(str(i).zfill(2) for i in now_time[:3])
    time_1 = '_'.join(str(i).zfill(2) for i in now_time[:6])
    return time_1


class create_order():

    def colums(self, ):
        # csv 文件的表头.有新增,修改字段名称,就在这里修改.
        return ("Order ID(M)", "Batch ID(O)", "Business Type(M)", "Business Process(M)", "Priority(M)",
                "Container Type(M)"
                , "Item Name(M)", "Item Code(M)", "Item Image URL(O)", "Item Count(M)", "Bin Location(M)",
                "Sequential Execution(O)")

    def order_id(self, num=1, same_id=1, pick_type=1, container_num=1, code_len=20, count_range=99,
                 file_path='', file_name='order.csv'):
        start_time = time.time()
        df = pandas.DataFrame(columns=self.colums())
        # 储位位置,目前是绑定了公司的. 不同场地需要做的话,再改.
        binlocations = [[1, 2, 3, 4, 5, 6, 7], [1, 2], [1, 2], [1, 2, 3, 4]]  # 排.列,层,位
        index_num = 0
        start = self.random_time()
        for id in range(start, start + num):  # 不同的ID号个数.
            for count in range(same_id):  # 一个相同ID号,有多少个.
                # 得新生成数据,不然就是same_id个相同的商品数据了.  有新增字段,这里也要对应新增函数.
                x = (id, self.alpha_digit(),  # 波次ID，用数字字母组成
                     self.business_type(),
                     self.business_process(pick_type),  # 拣货类型,传入索引.1=Total,2=Order
                     self.priority(),
                     self.container_type(container_num),  # 载物箱类型,1=1A,2=3A,3=9A
                     self.item_name(),  # 商品名称
                     self.item_code(code_len),  # 商品码
                     self.item_link(),  # 商品图片链接
                     # self.net_link(),
                     self.item_count(count_range),  # 拣货数量,1~参数值.比如1~30 之间的随机数值.
                     self.binlocation(binlocations),  # 货架位置
                     self.sequential_execution())  # 是否顺序下单
                # df.append(pandas.DataFrame(x))
                df.loc[index_num] = x  # 新增一行
                index_num += 1
                # print(x)
        final_name = self.business_process(pick_type) + '_' + str(num) + '单_' + str(same_id) + '商品_' + file_name
        df.to_csv(f"{file_path}/{final_name}.csv", index=False, sep=',')  # 不保存索引
        print(f"订单生成完成,耗时{(time.time() - start_time):0.2f}秒.文件在:{file_path}{final_name}")
        # print(df)

    def batch_id(self, num=1):
        return num

    def alpha_digit(self, num=30):
        ls = string.ascii_letters + string.digits
        return ''.join(random.sample(ls, random.choice(range(1, num))))

    def business_type(self, pick_type="Picking"):
        return pick_type

    def business_process(self, pick_pro=1):
        # 业务类型,注意新旧webportal,最新版已经修改回了TotalPicking和OrderPicking.
        pick_list = ["Total Picking", "Order Picking", "Sorting after picking", "Sorting while picking"]
        return pick_list[pick_pro - 1]

    def priority(self, num=1):
        return num

    def container_type(self, container=1):
        # 载物箱类型.一个文件,只会选一个. 下面的列表里随机生成.
        container_ls = [
            '1A_container',
            '3A_container',
            '6A_container',
            '9A_container',
            '1A_container&1A_container',
            '3A_container&3A_container',
            '6A_container&6A_container',
            '9A_container&9A_container',
        ]
        return container_ls[container - 1]

    def item_name(self):
        # 商品名称,随机选一个.这样处理不太好,测试数据,就无所谓了.
        # 如果从文件里读,则还要附带一个文件,测试数据需求不大,代码写死即可.
        goods_ls = ['不定时随机急停 黑色 XXL $189', '检查右上角订单详情按钮',
                    '随机上报异常', '扫描错误的商品条码xx123', '注意检查页面文本', '多语言测试页面', '+-按钮是否正常',
                    '进入异常上报 再返回', '丢失定位后 是否还能恢复移动', '退出SP 重启能否正常加载进入', '联想ThinkPad_T490', '拯救者Y9000 I7-12800H 16+512GB',
                    '中日小さな화셔袋をお04-ubun汤の998中に入', '喉が渇いた时に 108kg',
                    '文化的なシャツXXLの男性をJuxing', 'メカニカルキーボード104キー',
                    'Juxing 문츠 XXL 남성', '마이크로소프트 서버 호스트 I7 12800Q',
                    '这个名称很长-超过100个字符-看看怎么显 示 的 ' * 3,
                    ]
        return random.choice(goods_ls)

    def item_code(self, num=20):
        # 商品条码生成.现在是字母数字随机组合,1/3字母,2/3数字.
        # code = '199103181516'  # 先保留,异常情况,就返回万能码.
        alpha = random.sample(string.ascii_letters, num // 3)
        number = random.sample('0123456789' * (num // 10), num - num // 3)
        code = alpha + number
        random.shuffle(code)  # 直接原地打散了,没有返回值.
        return ''.join(code)

    def item_link(self):
        # 你要使用的商品图片链接.从下面的这些数据随机取一个.拼接成完整路径.
        # 百度图片:https://www.baidu.com/img/PCfb_5bf082d29588c07f842ccde3f97243ea.png
        link_list = ['4549395350520.png', '4902777079851.jpg', '4909384486567.png', '4923743543567.jpg',
                     '4942355137139.png', '4571157254333.jpg', '4903301519393.png', '4909411069421.png',
                     '4923743892375.jpg', '6911986345668.png', '4901330502881.png', '4905677849329.jpg',
                     '4922812584629.jpg', '4935768382748.png', '6912287534566.jpg', '4901330573492.jpg',
                     '4909345726135.jpg', '4922848674385.jpg', '4942355137122.png']
        return 'file:///../sdcard/syrius_guanxi_productImg/' + random.choice(link_list)

    def item_count(self, max_num=1, israndom=False):
        if israndom:
            return max_num
        elif max_num != 1:
            return random.randint(1, max_num)
        else:
            return 1

    def binlocation(self, *args):
        # 希音的储位格式: SS1424-3714-31
        # 可以实现了,但是有点难用.需要在页面上加配置来实现. 有些位置需要补0,有些位置不需要补0.不太好整.
        binlocation = 'A'
        for index, i in enumerate(args[0]):
            binlocation += str(random.choice(i)).zfill(2)  # 随便选一个.
        return binlocation

    def sequential_execution(self, default='No'):
        return default

    def other_col(self, name, data):
        # 暂时还没想好怎么写.
        return

    def random_time(self):
        x = [str(i).zfill(2) for i in list(time.localtime())]  # 时间戳
        x.append('01')
        # random.shuffle(x)  # 原地打乱列表顺序.
        y = int(''.join(x))  # 拼接,转型.
        return y


if __name__ == '__main__':
    ci = create_order()
    ci.order_id(
        pick_type=2,  # 订单类型.1=Total,2=Order
        num=18,  # 多少个不同的订单ID.
        same_id=3,  # 一个ID号要几个商品
        container_num=3,  # 载物箱索引,1=1A,2=3A,3=6A,4=9A
        count_range=10,  # 拣货数量的随机范围1~这个值.
        code_len=15,  # 商品码长度
        file_path='D:\工作\项目\订单\csv订单\\',  # 订单生成文件的路径,填写自己存放的路径.
        file_name=f'{file_time()}'  # 文件名称
    )

# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2023/3/9 22:39
# Desc: 二进制求和

# 内置函数法
class Solution:

    def addBinary(self, a: str, b: str):
        res = int(a, 2) + int(b, 2)  # 直接使用内置函数int将二进制转了十进制计算，再转回二进制即可。
        return str(bin(res))[2:]  # 二进制是0b开头的


# 非内置函数法

class Solution2:

    def addBinary(self, a: str, b: str):
        r, p = '', 0
        d = len(b) - len(a)  # 位数差
        # 经过这一步补0操作，得到a,b的长度是一致的。
        a = '0' * d + a  # 补0，如果d是正数，则前补。
        b = '0' * -d + b  # 补0，如果d是正数，则不补。
        # 经过下面循环，逐渐处理，最后能得到结果，最多是进不进1的问题。
        for i, j in zip(a[::-1], b[::-1]):  # 反向取，取相同长度出来计算。
            s = int(i) + int(j) + p  # i, j 无非是0或1，加上p
            r = str(s % 2) + r  # 累计的位答案。s是0,1,2之一，求余。
            p = s // 2  # 地板除，只有当s是2时，p=1.
        return '1' + r if p else r  # 结果是否进1，跟p的剩余情况有关。

a = '101010'
b = '1101'

print(Solution().addBinary(a,b))
print(Solution2().addBinary(a,b))
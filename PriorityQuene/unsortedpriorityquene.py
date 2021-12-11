# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月27日19时
"""
from PriorityQuene.priorityquenebase import PriorityQueneBase


class UnsortedPriorityQuene(PriorityQueneBase):
    """使用未排序列表实现的优先级队列，其父类为PriorityQueneBase"""

    def _find_min(self):
        """返回队列中key最小的项"""

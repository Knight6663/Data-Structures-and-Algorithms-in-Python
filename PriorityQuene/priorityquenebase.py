# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月27日19时
"""


class PriorityQueneBase:
    """优先级队列基类"""

    class _Item:
        """优先级队列中的元素项"""
        __slots__ = '_key', '_value'

        def __init__(self, key, value):
            self._key = key
            self._value = value

        def __lt__(self, other):
            return self._key < other._key

    def is_empty(self):
        """判断队列中是否为空"""
        return len(self) == 0



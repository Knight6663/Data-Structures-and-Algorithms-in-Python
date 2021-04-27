# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月27日20时
"""


class LinkedQuene:
    """链式队列"""

    # -------------------------------------------------------------------
    class _Node:
        """结点"""
        __slots__ = '_element', '_next'

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # --------------------------------------------------------------------

    def __init__(self):
        """建立一个空队列"""
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        """返回队列的长度"""
        return self._size

    def is_empty(self):
        """返回队列是否为空的布尔值"""
        return self._size == 0

    def first(self):
        """返回队列中的front"""
        if self.is_empty():
            raise TypeError('队列是空的!')
        return self._head._element

    def dequene(self):
        """出队列"""
        if self.is_empty():
            raise TypeError('队列是空的!')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return answer

    def enquene(self, element):
        """入队列"""
        newest = self._Node(element, None)
        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest
        self._size += 1

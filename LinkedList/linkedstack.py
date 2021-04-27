# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月27日20时
"""


class LinkedStack:
    """单向链表实现栈"""

    # -------------------------------------------------------------------
    class _Node:
        """结点"""
        __slots__ = '_element', '_next'

        def __init__(self, element, next):
            self._element = element
            self._next = next

    # --------------------------------------------------------------------

    def __init__(self):
        """建立一个空栈"""
        self._head = None
        self._size = 0

    def __len__(self):
        """返回栈的长度"""
        return self._size

    def is_empty(self):
        """返回栈是否为空的布尔值"""
        return self._size == 0

    def push(self, element):
        """入栈"""
        self._head = self._Node(element, self._head)
        self._size += 1

    def top(self):
        """返回栈顶元素"""
        if self.is_empty():
            raise TypeError('栈是空的!')
        return self._head._element

    def pop(self):
        """出栈"""
        if self.is_empty():
            raise TypeError('栈是空的!')
        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        return answer


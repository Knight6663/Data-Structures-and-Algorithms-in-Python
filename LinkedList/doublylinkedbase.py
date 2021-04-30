# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月30日14时
"""


class _DoublyLinkedBase:
    """双端列表的基础类"""

    class _Node:
        """储存双链结点的非公开类"""
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev, next):
            self._element = element
            self._prev = prev
            self._next = next

    def __init__(self):
        """创建一个空列表"""
        self._header = self._Node(None, None, None)
        self._trailer = self._Node(None, None, None)
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0

    def __len__(self):
        """返回列表长度"""
        return self._size

    def is_empty(self):
        """检测列表是否为空"""
        return self._size == 0

    def _insert_between(self, element, predecessor, successor):
        """在两个已经存在的结点之间添加一个元素element，并返回这个新的结点"""
        newest = self._Node(element, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        """从列表中删除一个结点，并返回这个结点的元素"""
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None
        return element

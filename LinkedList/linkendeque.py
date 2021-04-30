# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月30日14时
"""

from LinkedList.doublylinkedbase import _DoublyLinkedBase


class LinkedDeque(_DoublyLinkedBase):
    """链式双端队列"""

    def first(self):
        """返回双端队列中的front的element"""
        if self.is_empty():
            raise ValueError('双端队列是空的!')
        return self._header._next._element

    def last(self):
        """返回双端队列中的back的element"""
        if self.is_empty():
            raise ValueError('双端队列是空的!')
        return self._trailer._prev._element

    def insert_first(self, element):
        """在双端队列的最前面添加一个元素"""
        self._insert_between(element, self._header, self._header._next)

    def insert_last(self, element):
        """在双端队列的最后面添加一个元素"""
        self._insert_between(element, self._trailer._prev, self._trailer)

    def delete_first(self):
        if self.is_empty():
            raise ValueError('双端队列是空的!')
        return self._delete_node(self._header._next)

    def delete_last(self):
        if self.is_empty():
            raise ValueError('双端队列是空的!')
        return self._delete_node(self._trailer._prev)

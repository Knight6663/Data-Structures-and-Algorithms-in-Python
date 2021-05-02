# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年05月02日17时
"""

from LinkedList.doublylinkedbase import _DoublyLinkedBase


class PositionalList(_DoublyLinkedBase):
    """一个可以方位位置的有序容器"""

    # --------------------Position class ---------------------------
    class Position:
        """表示单个元素的位置抽象类"""

        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            """返回这个位置的元素"""
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            """如果other没有表示相同的位置，则返回True"""
            return not (self == other)

    # ---------------------- 公共方法 ---------------------------
    def _validate(self, position):
        """返回position位置的结点，如果非法则提示错误"""
        if not isinstance(position, self.Position):
            raise TypeError('必须传入Position类型')
        if position._container is not self:
            raise ValueError('position并不属于这个容器')
        if position._node._next is None:
            raise ValueError('position不再有效')
        return position._node

    def _make_position(self, node):
        """给结点增加Position实例"""
        if node is self._header or node is self._trailer:
            return None
        else:
            return self.Position(self, node)

    # --------------------- 存储 ------------------------------
    def first(self):
        return self._make_position(self._header._next)

    def last(self):
        return self._make_position(self._trailer._prev)

    def before(self, position):
        """返回在position之前的位置"""
        node = self._validate(position)
        return self._make_position(node._prev)

    def after(self, position):
        """返回position之后的位置"""
        node = self._validate(position)
        return self._make_position(node._next)

    def __iter__(self):
        """迭代生成返回列表元素"""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def _insert_between(self, element, predecessor, successor):
        """在已近存在的结点和新的位置中添加一个元素"""
        node = super()._insert_between(element, predecessor, successor)
        return self._make_position(node)

    def add_first(self, element):
        """在列表的最前方插入一个元素并返回产生的新位置"""
        return self._insert_between(element, self._header, self._header._next)

    def add_last(self, element):
        """在列表的最后方插入一个元素并返回产生的新位置"""
        return self._insert_between(element, self._trailer._prev, self._trailer)

    def add_before(self, position, element):
        """在位置position之前插入一个元素并返回产生的新位置"""
        original = self._validate(position)
        return self._insert_between(element, original._prev, original)

    def add_after(self, position, element):
        """在位置position之后插入一个元素并返回产生的新位置"""
        original = self._validate(position)
        return self._insert_between(element, original, original._next)

    def delete(self, position):
        """删除并返回删除位置的元素"""
        original = self._validate(position)
        return self._delete_node(original)

    def replace(self, position, element):
        """将位置position中的元素替换成element,返回旧元素"""
        original = self._validate(position)
        old_value = original._element
        original._element = element
        return old_value


def insertion_sort(L):
    """对列表进行排序"""
    if len(L) > 1:
        marker = L.first()
        while marker != L.last():
            pivot = L.after(marker)
            value = pivot.element()
            if value > marker.element():
                marker = pivot
            else:
                walk = marker
                while walk != L.first() and L.before(walk).element() > value:
                    walk = L.before(walk)
                L.delete(pivot)
                L.add_before(walk, value)


if __name__ == '__main__':      # 测试
    L = PositionalList()
    p1 = L.add_first(1)
    for i in [2, 95, 14, 11, 15, 59, 7, 31, 48, 115]:
        L.add_after(p1, i)
    for i in L.__iter__():
        print(i, end=' ')       # 原序列应为: 1 115 48 31 7 59 15 11 14 95 2
    print('\n'+50*'-')          # 分界线
    insertion_sort(L)
    for i in L.__iter__():
        print(i, end=' ')       # 应输出: 1 2 7 11 14 15 31 48 59 95 115



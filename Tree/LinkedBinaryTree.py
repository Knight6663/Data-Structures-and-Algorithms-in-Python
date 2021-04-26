# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月20日19时
"""

import BinaryTree


class LinkedBinaryTree(BinaryTree.BinaryTree):
    """链式二叉树结构"""

    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.BinaryTree.Position):
        """一个代表单个元素位置的抽象类"""

        def __init__(self, container, node):
            """用户不应调用构造函数"""
            self._container = container
            self._node = node

        def element(self):
            """返回位置储存的元素"""
            return self._node._element

        def __eq__(self, other):
            """如果其他Position表示了相同位置，则返回True"""
            return type(other) is type(self) and other._node is self._node

    def _validate(self, position):
        """如果位置合法，返回关联结点"""
        if not isinstance(position, self.Position):
            raise TypeError('position必须是适当的Position类型')
        if position._container is not self:
            raise ValueError('position并不属于这个容器')
        if position._node._parent is position._node:
            raise ValueError('position不合法')
        return position._node

    def _make_position(self, node):
        """由已经给出的Node返回Position实例(如果没有Node则返回None)"""
        return self.Position(self, node) if node is not None else None

    # -------------------------二叉树构造函数-----------------------------
    def __init__(self):
        """创建一个初始空二叉树"""
        self._root = None
        self._size = 0

    # -------------------------公共存储----------------------------------
    def __len__(self):
        """返回树中元素的总数"""
        return self._size

    def root(self):
        """返回表示树的根节点的位置(如果是空树则返回None)"""
        return self._make_position(self._root)

    def parent(self, position):
        """返回position的父结点(若position没有根节点则返回None)"""
        node = self._validate(position)
        return self._make_position(node._parent)

    def left(self, position):
        """
        返回position的左孩子的位置
        如果position没有左孩子，则返回None
        """
        node = self._validate(position)
        return self._make_position(node._left)

    def right(self, position):
        """
        返回position的右孩子的位置
        如果position没有右孩子，则返回None
        """
        node = self._validate(position)
        return self._make_position(node._right)

    def num_children(self, position):
        """返回位置position所含有的孩子数"""
        node = self._validate(position)
        count = 0
        if node._left is not None:  # 左孩子存在
            count += 1
        if node._left is not None:  # 右孩子存在
            count += 1
        return count

    # -----------------------非公开更新方法-----------------
    def _add_root(self, e):
        """
        放置元素e在一个空树的根节点上，并返回新位置
        如果树不为空的时候会Raise ValueError
        :param e:元素
        :return: 新位置
        """
        if self._root is not None:
            raise ValueError('根节点已经存在了!')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, position, e):
        """
        position位置上创造一个新的左孩子，储存元素e
        当位置position不合法或position已经有了一个左孩子时，Raise ValueError
        :param position: 左孩子的位置position
        :param e: 元素
        :return: 新结点的位置
        """
        node = self._validate(position)
        if node._left is not None:
            raise ValueError('左孩子已经存在了!')
        self._size += 1
        node._left = self._Node(e, parent=node)
        return self._make_position(node._left)

    def _add_right(self, position, e):
        """
        position位置上创造一个新的右孩子，储存元素e
        当位置position不合法或position已经有了一个右孩子时，Raise ValueError
        :param position: 右孩子的位置position
        :param e: 元素
        :return: 新结点的位置
        """
        node = self._validate(position)
        if node._right is not None:
            raise ValueError('右孩子已经存在了!')
        self._size += 1
        node._right = self._Node(e, parent=node)
        return self._make_position(node._right)

    def _replace(self, position, e):
        """
        将位置p上的元素替换为e，返回旧元素
        :param position: 位置position
        :param e: 元素
        :return: 旧位置上的元素
        """
        node = self._validate(position)
        old = node._element
        node._element = e
        return old

    def _delete(self, position):
        """
        删除位置position的结点，如果有孩子的话，将其替换为它的孩子
        当位置position不合法或者位置position有两个孩子的时候会raise ValueError
        :param position:位置position
        :return:返回储存在位置position的元素
        """
        node = self._validate(position)
        if self.num_children(position) == 2:
            raise ValueError('这个position已经有了两个孩子了!')
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            if node is parent._right:
                parent._right = child
        self._size -= 1
        node._parent = node  # 对已经弃用的结点进行处理
        return node._element

    def _attach(self, position, t1, t2):
        """
        将树1和树2作为左树和右树合并在外部位置position
        :param position: 位置
        :param t1: 树1
        :param t2: 树2
        :return: 无
        """
        node = self._validate(position)
        if not self.is_leaf(position):
            raise ValueError('位置position必须是叶子')
        if not type(self) is type(t1) is type(t2):  # 三个树必须是同一种类型
            raise TypeError('树的类型必须匹配')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0


def preorder_indent(tree, position, depth):
    print(2 * depth * ' ' + str(position.element()))
    for c in tree.children(position):
        preorder_indent(tree, c, depth + 1)


def preorder_label(tree, position, depth, path):
    """
    在由T为根节点的树上输出深度为d的子树
    :param tree:root
    :param position:position
    :param depth:depth
    :param path:path
    :return:print
    """
    label = '.'.join(str(j + 1) for j in path)
    print(2 * depth * '' + label, position.element())
    path.append(0)
    for c in tree.children(position):
        preorder_label(tree, c, depth + 1, path)
        path[-1] += 1
    path.pop()


def parenthesize(tree, position):
    """"""
    print(position.element(), end='')
    if not tree.is_leaf(position):
        first_time = True
        for c in tree.children(position):
            sep = '(' if first_time else ','
            print(sep, end='')
            first_time = False
            parenthesize(tree, c)
        print(')', end='')


if __name__ == '__main__':
    t = LinkedBinaryTree()
    p_root = t._add_root('A')
    p1 = t._add_left(p_root, 'B')
    t._add_left(p1, 'D')
    p2 = t._add_right(p1, 'E')
    t._add_right(p2, 'F')
    t._add_right(p_root, 'C')
    #t._delete(p2)  # 删除B的字树E
    for p in t.__iter__():
        print(p)
    print(20 * '*')
    preorder_indent(t, t.root(), 0)
    print(20 * '*')
    parenthesize(t, p_root)

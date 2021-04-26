# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月20日17时
"""



class Tree:
    """一个表示树的抽象类"""

    # ------------嵌套Position类-----------------------
    class Position:
        """一个表示单独元素位置的抽象类"""

        def element(self):
            """返回元素在这个位置的储存"""
            raise NotImplementedError('由子类实现')

        def __eq__(self, other):
            """如果其他Position表示了相同位置，则返回True"""
            raise NotImplementedError('由子类实现')

        def __ne__(self, other):
            """如果其他Position没有表示了相同位置，则返回True"""
            return not (self == other)

    # ------------具体子类必须支持的抽象方法---------------
    def root(self):
        """返回表示树的根节点的位置(如果是空树则返回None)"""
        raise NotImplementedError('由子类实现')

    def parent(self, p):
        """返回p的双亲(若p没有根节点则返回None)"""
        raise NotImplementedError('由子类实现')

    def num_children(self, p):
        """返回位置p所含有的孩子数"""
        raise NotImplementedError('由子类实现')

    def children(self, p):
        """Generate an iteration of Position representing p's children"""
        raise NotImplementedError('由子类实现')

    def __len__(self):
        """返回树上的所有元素的数目"""
        raise NotImplementedError('由子类实现')

    # ------------在这个类中具体实现的方法-----------------
    def is_root(self, p):
        """如果p表示的是树的根节点，则返回True"""
        return self.root() == p

    def is_leaf(self, p):
        """如果p没有任何一个孩子，则返回True"""
        return self.num_children(p) == 0

    def is_empty(self):
        """如果这个树是空的，则返回True"""
        return len(self) == 0

    def depth(self, p):
        """返回位置p距离根节点的深度"""
        return 0 if self.is_root(p) else 1 + self.depth(self.parent(p))

    def _height(self, p):  # 时间上接近于子树的大小
        """返回树的高度"""
        return 0 if self.is_leaf(p) else 1 + max(self._height(c) for c in self.children(p))

    def height(self, p=None):
        """
        返回指定位置p作为根节点的高度
        如果p是None,返回整个树的高度
        """
        if p is None:
            p = self.root()
        return self._height(p)

    def preorder(self):
        """前序遍历"""
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self, p):
        """前序子树遍历"""
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def postorder(self):
        """后序遍历"""
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):
        """后序子树遍历"""
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other
        yield p

    def pre_position(self):
        return self.preorder()

    def post_position(self):
        return self.postorder()

    def __iter__(self):
        """生成树中元素的迭代"""
        for p in self.pre_position():
            yield p.element()

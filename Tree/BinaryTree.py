# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月20日18时
"""

import Tree


class BinaryTree(Tree.Tree):
    """一个表示二叉树的抽象类"""

    # -------------附加抽象方法-------------
    def left(self, p):
        """
        返回p的左孩子的位置
        如果p没有左孩子，则返回None
        """
        raise NotImplementedError('必须由子类实现')

    def right(self, p):
        """
        返回p的右孩子的位置
        如果p没有右孩子，则返回None
        """
        raise NotImplementedError('必须由子类实现')

    def sibling(self, p):
        """返回p的兄弟姐妹的位置(如果没有则返回None)"""
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """生成一个代表p的孩子位置的迭代对象"""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def inorder(self):
        """中序遍历"""
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        """中序子树遍历"""
        if self.left(p) is not None:
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p
        if self.right(p) is not None:
            for other in self._subtree_inorder(self.right(p)):
                yield other
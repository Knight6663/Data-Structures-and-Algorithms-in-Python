# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月25日18时
"""
import LinkedBinaryTree


class ExpressionTree(LinkedBinaryTree):
    """表达式树"""

    def __init__(self, token, left=None, right=None):
        super().__init__()
        if not isinstance(token, str):
            raise TypeError('Token必须是一个字符')
        self._add_root(token)
        if left is not None:
            if token not in '+-*x/':          # 将*和x都视为乘法
                raise ValueError('token必须合法')
            self._attach(self.root(), left, right)

    def _parenthesize_recur(self, p, result):
        """将p的子树的分段表示追加到结果列表"""
        if self.is_leaf(p):
            result.append(str(p.element()))
        else:
            result.append('(')
            self._parenthesize_recur(self.left(p), result)
            result.append(p.element())
            self._parenthesize_recur(self.right(p), result)
            result.append(')')

    def __str__(self):
        """以字符串形式返回表达式"""
        pieces = []
        self._parenthesize_recur(self.root(), pieces)
        return ''.join(pieces)

    def evaluate(self):
        """返回表达式的数字结果"""
        return

    def _evaluate_recur(self, p):
        """"""
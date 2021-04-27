# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月25日18时
"""
from LinkedBinaryTree import LinkedBinaryTree


class ExpressionTree(LinkedBinaryTree):
    """表达式树"""

    def __init__(self, token, left=None, right=None):
        super().__init__()            # 父类继承
        if not isinstance(token, str):
            raise TypeError('Token必须是一个字符')
        self._add_root(token)
        if left is not None:
            if token not in '+-*x/':  # 将*和x都视为乘法
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
        return self._evaluate_recur(self.root())

    def _evaluate_recur(self, p):
        """返回p处子树的数字结果"""
        if self.is_leaf(p):
            return float(p.element())
        else:
            op = p.element()
            left_val = self._evaluate_recur(self.left(p))
            right_val = self._evaluate_recur(self.right(p))
            if op == '+':
                return left_val + right_val
            if op == '-':
                return left_val - right_val
            if op == '/':
                return left_val / right_val
            else:
                return left_val * right_val


def build_experssion_tree(tokens):
    """建立表达式树，tokens为字符串"""
    S = []
    for t in tokens:
        if t in '+-/*x':
            S.append(t)
        elif t not in '()':
            S.append(ExpressionTree(t))
        elif t == ')':
            right = S.pop()
            op = S.pop()
            left = S.pop()
            S.append(ExpressionTree(op, left, right))
    return S.pop()


if __name__ == '__main__':
    EX = build_experssion_tree('(((3+1)*6)/((9-5)+2))')     # 建立表达式树
    print(EX.evaluate())

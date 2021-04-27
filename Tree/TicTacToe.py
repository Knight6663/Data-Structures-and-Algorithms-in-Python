# -*- coding:UTF-8 -*-
"""
作者:吕瑞承
日期:2021年04月26日22时
"""

import random

# 用0-8的9个数字来表示棋盘的位置:0,1,2,3,4,5,6,7,8,
# WIN表示的是取胜的情况，即一行，一列，对角线相同时。
WIN = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
       (0, 3, 6), (1, 4, 7), (2, 5, 8),
       (0, 4, 8), (2, 4, 6))

row = ((0, 1, 2), (3, 4, 5), (6, 7, 8))

# -1表示玩家 0表示空位 1表示电脑.
X_HUMAN = -1
EMPTY = 0
O_COMPUTER = 1

# 棋盘上的值为0,1，-1，正好可以和mark中的标志相对应
# mark中的标志是为了输出棋盘
mark = ['·', 'O', 'X']
RESULT = ['平局', '电脑胜利', '玩家胜利']
HUMAN = 1
COMPUTER = 0


# 输出当前的棋盘状态
def PRINT(board):
    for i in row:
        re = ' '
        for j in i:
            re += mark[board[j]] + ' '
        print(re)


# 判断当前棋盘是否还有空位,true表示还有空位，false表示没有空位了
# 判断当前棋盘board的每一个位置是否为空
def isEmpty(board):
    for item in range(0, 9):
        if board[item] == EMPTY:
            return True
    return False


# 判断是否已经产生赢家
# -1表示玩家获胜，1表示电脑获胜，0为平局或者还未结束
# 在主程序的while循环中返回为0则表示还未结束，while循环结束后返回的0表示平局
def winner(board):
    for i in WIN:
        # -1即为玩家，1为电脑
        if board[i[0]] == board[i[1]] == board[i[2]] == -1:
            return -1
        elif board[i[0]] == board[i[1]] == board[i[2]] == 1:
            return 1
    return 0


# alpha-bate剪枝策略的具体内容
'''这里的搜索深度是9，叶子节点的估价函数值为1电脑赢，-1玩家赢，0是平局'''


def A_B(board, player, next_player, alpha, beta):
    board1 = board
    win = winner(board1)
    # 有玩家获胜时
    if win != EMPTY:
        return win
    elif not isEmpty(board1):
        # 没有空位,平局
        return 0

    # 检查当前玩家"player"的所有可落子点
    for move in range(0, 9):
        if board1[move] == EMPTY:
            board1[move] = player
            # 落子之后交换玩家，继续检验
            val = A_B(board1, next_player, player, alpha, beta)
            board1[move] = EMPTY

            # 对于一个MAX节点，估计出其倒推值的下确界Alpha，
            # 若这个Alpha值不小于MAX的父节点(MIN节点)的估计倒推值的上确界Beta，即Alpha≥Beta，
            # 则就不必再扩展该MAX节点的其余子节点了，为Beta剪枝。
            if player == O_COMPUTER:  # 当前玩家是Max玩家，是1
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta  # 直接返回当前的最大可能取值beta, 进行剪枝

            # 对于一个MIN节点，估计出其倒推值的上确界Beta，
            # 这个Beta值不大于MIN的父节点(MAX节点)的估计倒推值的下确界Alpha，即Alpha≥Beta，
            # 则就不必再扩展该MIN节点的其余子节点了，为Alpha剪枝。
            else:  # 当前玩家是Min玩家，是-1
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha  # 直接返回当前的最小可能取值alpha, 进行剪枝
    if player == O_COMPUTER:
        re = alpha
    else:
        re = beta
    return re


# 确定下一步电脑的走步，用到alpha-bate剪枝策略
def move(board):
    board1 = board
    best = -2  # 初始化最优值为-2，因为棋盘的值为-1,0,1
    cmoves = []  # 用来存储可能的位置
    for i in range(0, 9):
        if board1[i] == EMPTY:
            board1[i] = O_COMPUTER  # 暂时将i位置处作为电脑的走步

            # val为在暂时走步的基础上得出的结果
            val = A_B(board1, X_HUMAN, O_COMPUTER, -2, 2)
            board1[i] = EMPTY  # 恢复原状态
            if val > best:
                best = val
                cmoves = [i]
            if val == best:
                cmoves.append(i)
    return random.choice(cmoves)


# 游戏开始
if __name__ == '__main__':

    # 初始化下一步，当输入有误时默认玩家先
    next_move = HUMAN

    first = input("请选择哪一方先下，输入x表示玩家先下，输入o表示电脑先下（小写）：")
    if first == "x":
        next_move = HUMAN
    elif first == "o":
        next_move = COMPUTER
    else:
        print("输入有误，默认玩家先下")

    # 初始化棋盘为空
    board = [EMPTY for i in range(9)]

    # 当棋盘还有空位且没有出现赢家时
    while isEmpty(board) and winner(board) == EMPTY:
        PRINT(board)
        if next_move == HUMAN and isEmpty(board):
            try:
                hmove = int(input("请输入你要落子的位置(0-8)："))
                if board[hmove] != EMPTY:
                    print('位置选择错误，请重新选择')
                    continue
                board[hmove] = X_HUMAN
                next_move = COMPUTER
            except:
                print("输入有误，请重试")
                continue
        if next_move == COMPUTER and isEmpty(board):
            cmove = move(board)
            board[cmove] = O_COMPUTER
            next_move = HUMAN

    # 当没有空位或已经出现赢家时退出循环
    # 输出结果
    PRINT(board)
    print(RESULT[winner(board)])

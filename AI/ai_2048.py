from AI.calculator import *
from board import *


class AI2048Result(object):
    def __init__(self, move=-1, score=0):
        self.move = move
        self.score = score


def search_best(this_board: Board, depth, alpha, beta, playerTurn: bool) -> AI2048Result:
    """
    :param this_board:  当前棋盘局势 Board类
    :param depth:       当前深度
    :param alpha:       玩家方剪枝
    :param beta:        电脑方剪枝
    :param playerTurn:  玩家/电脑方
    :return:            AI2048Result类
    """
    bestMove = -1
    result = AI2048Result()

    if playerTurn:
        bestScore = alpha
        for direction in range(4):
            newBoard = Board(this_board.map)
            changed = newBoard.move(direction)
            if changed:  # 如果该方向可以移动
                if depth == 0:
                    result.move = direction
                    result.score = calculate_evaluation(newBoard.map)
                else:
                    result = search_best(newBoard, depth - 1, bestScore, beta, False)

                if result.score > bestScore:
                    bestScore = result.score
                    bestMove = direction
                if bestScore > beta:
                    return AI2048Result(bestMove, beta)
    else:
        bestScore = beta
        newBoard = Board(this_board.map)
        score_2 = []
        score_4 = []
        worstSituation = []
        freeBlocks1 = newBoard.getFreeBlocks()
        freeBlocks = copy.deepcopy(freeBlocks1)
        for value in [2, 4]:
            for i in range(len(freeBlocks)):
                if not newBoard.add_xy(freeBlocks[i][0], freeBlocks[i][1], value):
                    print("Ai加数这边出现bug")
                if value == 2:
                    score_2.append(-calculate_smoothness(newBoard.map) + calculate_islands(newBoard.map))
                if value == 4:
                    score_4.append(-calculate_smoothness(newBoard.map) + calculate_islands(newBoard.map))
                newBoard.remove_xy(freeBlocks[i][0], freeBlocks[i][1])
        maxScore = max(max(score_2), max(score_4))
        for i in range(len(score_2)):
            if score_2[i] == maxScore:
                worstSituation.append([freeBlocks[i], 2])
        for i in range(len(score_4)):
            if score_4[i] == maxScore:
                worstSituation.append([freeBlocks[i], 4])
        for situation in worstSituation:
            newBoard2 = Board(this_board.map)
            if not newBoard2.add_xy(situation[0][0], situation[0][1], situation[1]):
                print("bug!!")
            result = search_best(newBoard2, depth, alpha, bestScore, True)

            if result.score < bestScore:
                bestScore = result.score

            if bestScore < alpha:
                return AI2048Result(-1, alpha)

    return AI2048Result(bestMove, bestScore)


def getBestMove(this_board, depth=4):
    """通过搜索算法返回当前最优移动方向"""
    result = search_best(this_board, depth, -1000000, 1000000, True)
    return result.move

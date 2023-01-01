from calculator import *
from board_2048 import *


class AI2048Result(object):
    def __init__(self, move=-1, score=0, positions=0, cutoffs=0):
        self.move = move
        self.positions = positions
        self.cutoffs = cutoffs
        self.score = score


def search_best(this_board: Board, depth, alpha, beta, positions, cutoffs, playerTurn: bool) -> AI2048Result:
    bestScore = 0
    bestMove = -1
    result = AI2048Result()

    if playerTurn:
        bestScore = alpha
        for direction in range(4):
            newBoard = Board(this_board.map)
            changed = newBoard.move(direction)
            if changed:  # 如果该方向可以移动
                positions += 1
                if depth == 0:
                    result.move = direction
                    result.score = calculate_evaluation(newBoard.map)
                else:
                    result = search_best(newBoard, depth - 1, bestScore, beta, positions, cutoffs, False)
                    if result.score > 9900:
                        result.score -= 1
                    positions = result.positions
                    cutoffs = result.cutoffs

                if result.score > bestScore:
                    bestScore = result.score
                    bestMove = direction
                if bestScore > beta:
                    cutoffs += 1
                    return AI2048Result(bestMove, beta, positions, cutoffs)
    else:
        bestScore = beta
        newBoard = Board(this_board.map)
        score_2 = []
        score_4 = []
        worstSituation = []
        freeBlocks = newBoard.getFreeBlocks()
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
                print("BUG!!")
            positions += 1
            result = search_best(newBoard2, depth, alpha, bestScore, positions, cutoffs, True)
            positions = result.positions
            cutoffs = result.cutoffs

            if result.score < bestScore:
                bestScore = result.score

            if bestScore < alpha:
                cutoffs += 1
                return AI2048Result(-1, alpha, positions, cutoffs)

    return AI2048Result(bestMove, bestScore, positions, cutoffs)


def getBestMove(this_board, depth=4):
    tmp = Board(this_board.map)
    result = search_best(tmp, depth, -100000, 100000, 0, 0, True)
    return result.move

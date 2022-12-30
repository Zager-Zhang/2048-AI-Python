from board import *


class AI2048Result(object):
    def __init__(self, move=-1, score=0, positions=0, cutoffs=0):
        self.move = move
        self.positions = positions
        self.cutoffs = cutoffs
        self.score = score


def search_best(this_board: Board, depth, alpha, beta, position, cutoffs, playerTurn: bool):
    bestScore = 0
    bestMove = -1
    result = AI2048Result()

    if playerTurn:
        bestScore = alpha
        newBoard = Board(this_board.map)

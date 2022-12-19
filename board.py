import copy
import random
import math
from config_2048 import *

GAME_CONTINUE = 1
GAME_ERROR = 0
GAME_OVER = -1
# 方块的位置权值


# tip的映射
tip = {0: 'left', 1: 'up', 2: 'right', 3: 'down'}


class Board(object):
    """棋盘类"""

    def __init__(self):
        """棋盘初始化"""
        self.map = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.best_direction = None

        # 开局先加入两个2
        self.add(True)
        self.add(True)
        self.print_map()

    def __judge_add(self):
        """判断当前是否可以添加数"""

        for i in range(4):
            for j in range(4):
                if self.map[i][j] == 0:
                    return True
        return False

    def __judge_game(self):
        """判断游戏是否可以继续"""

        for i in range(4):
            for j in range(4):
                if self.map[i][j] == 0:
                    return True
                elif j + 1 <= 3 and self.map[i][j] == self.map[i][j + 1]:
                    return True
                elif j - 1 >= 0 and self.map[i][j] == self.map[i][j - 1]:
                    return True
                elif i + 1 <= 3 and self.map[i][j] == self.map[i + 1][j]:
                    return True
                elif i - 1 >= 0 and self.map[i][j] == self.map[i - 1][j]:
                    return True
        return False

    def add(self, is_start=False):
        """
        随机添加一个新数字
        :return: True 可以继续游戏 False 操作错误无法继续游戏
        """
        if not self.__judge_game():
            print("Game Over!")
            return GAME_OVER
        if not self.__judge_add():
            print("操作失误，请重新操作")
            return GAME_ERROR
        pos = random.randint(0, 15)
        while self.map[math.floor(pos // 4)][pos % 4] != 0:
            pos = random.randint(0, 15)
        num = random.randint(0, 99)
        num = (lambda x: 4 if x >= 90 else 2)(num)  # 十分之一的概率为4
        if is_start:
            num = 2
        self.map[math.floor(pos // 4)][pos % 4] = num
        return GAME_CONTINUE

    @staticmethod
    def calculate_predictions(mapp):
        """计算未来一步的预测评分值"""

        tmp = 0
        for i in range(4):
            for j in range(4):
                if j + 1 <= 3 and mapp[i][j] == mapp[i][j + 1]:
                    tmp += mapp[i][j]
                elif j - 1 >= 0 and mapp[i][j] == mapp[i][j - 1]:
                    tmp += mapp[i][j]
                elif i + 1 <= 3 and mapp[i][j] == mapp[i + 1][j]:
                    tmp += mapp[i][j]
                elif i - 1 >= 0 and mapp[i][j] == mapp[i - 1][j]:
                    tmp += mapp[i][j]
        return tmp

    @staticmethod
    def calculate_map_w(mapp):
        """计算当前方块权值"""

        tmp = 0
        for i in range(4):
            for j in range(4):
                tmp += mapp[i][j] * map_w[i][j]
        return tmp

    def move_left(self, is_change=True):
        """
        左移 并 计算评分
        :param is_change: 是否对当前情况进行修改
        :return: 不修改 :当前情况的评分值 用来提供AI的判断标准
                 修改   :返回 0
        """
        single_score = 0
        single_cnt = 0
        tmp_map = copy.deepcopy(self.map)
        for i in range(4):
            row = tmp_map[i]
            # 将每一行的0都移到后面
            row = sorted(row, key=lambda x: 1 if x == 0 else 0)
            for j in range(3):
                if row[j] == row[j + 1]:
                    single_score += row[j] * 2
                    single_cnt += 1
                    row[j] += row[j + 1]
                    row[j + 1] = 0
            # 再次更新每一行的0
            row = sorted(row, key=lambda x: 1 if x == 0 else 0)
            tmp_map[i] = row

        prediction_score = self.calculate_predictions(tmp_map)
        if is_change:
            self.map = copy.deepcopy(tmp_map)
            self.score += single_score
            return 0
        else:
            return single_score + single_cnt * single_score + prediction_score * 0.8

    def move_right(self, is_change=True):
        self.map = [row[::-1] for row in self.map]
        temp = self.move_left(is_change)
        self.map = [row[::-1] for row in self.map]
        return temp

    def move_up(self, is_change=True):
        # 左旋90° 再 右旋90°
        self.map_left_rotate90()
        temp = self.move_left(is_change)
        self.map_right_rotate90()
        return temp

    def move_down(self, is_change=True):
        # 右旋90° 再 左旋90°
        self.map_right_rotate90()
        temp = self.move_left(is_change)
        self.map_left_rotate90()
        return temp

    def print_map(self):
        print("当前局势为:")
        for i in range(4):
            print(self.map[i])

    def map_left_rotate90(self):
        """ 左旋转90° """
        temp_map = [[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                temp_map[i][j] = self.map[j][3 - i]
        self.map = copy.deepcopy(temp_map)

    def map_right_rotate90(self):
        """ 右旋转90° """
        temp_map = [[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                temp_map[i][j] = self.map[3 - j][i]
        self.map = copy.deepcopy(temp_map)

    def tip_direction(self):
        """提示操作方向"""

        prediction = [0, 0, 0, 0]
        prediction[0] = self.move_left(False)
        prediction[1] = self.move_up(False)
        prediction[2] = self.move_right(False)
        prediction[3] = self.move_down(False)
        self.best_direction = prediction.index(max(prediction))
        # print(tip[self.best_direction])
        return self.best_direction

    def update(self, surface, is_tip):

        # 棋盘板的颜色
        surface.fill(BOARD_COLOR, rect=BOARD_RECD)

        # 棋盘格颜色
        for i in range(4):
            for j in range(4):
                surface.fill(BOARD_PLAID_COLOR,
                             rect=(BOARD_RECD.x + SIDE_WIDTH * (j + 1) + CUBE_WIDTH * j,
                                   BOARD_RECD.y + SIDE_WIDTH * (i + 1) + CUBE_WIDTH * i, CUBE_WIDTH, CUBE_WIDTH))
        for i in range(4):
            for j in range(4):
                if self.map[i][j]:
                    cube_rect = pygame.Rect(BOARD_RECD.x + SIDE_WIDTH * (j + 1) + CUBE_WIDTH * j,
                                            BOARD_RECD.y + SIDE_WIDTH * (i + 1) + CUBE_WIDTH * i, CUBE_WIDTH,
                                            CUBE_WIDTH)
                    surface.fill(CUBE_COLORS[int(math.log2(self.map[i][j]))], rect=cube_rect)

                    if self.map[i][j] <= 4:
                        font = pygame.font.SysFont("Microsoft Sans Serif", 50)
                        text = font.render(str(self.map[i][j]), True, CUBE_NUM_COLORS[0])
                    elif self.map[i][j] <= 64:
                        font = pygame.font.SysFont("Microsoft Sans Serif", 45)
                        text = font.render(str(self.map[i][j]), True, CUBE_NUM_COLORS[1])
                    elif self.map[i][j] <= 512:
                        font = pygame.font.SysFont("Microsoft Sans Serif", 40)
                        text = font.render(str(self.map[i][j]), True, CUBE_NUM_COLORS[1])
                    else:
                        font = pygame.font.SysFont("Microsoft Sans Serif", 35)
                        text = font.render(str(self.map[i][j]), True, CUBE_NUM_COLORS[1])
                    font_rect = text.get_rect(center=cube_rect.center)
                    surface.blit(text, font_rect)

        if is_tip:
            font = pygame.font.SysFont("consolas", 36)
            text = font.render('tip:' + tip[self.tip_direction()], True, (100, 100, 10))
            font_rect = text.get_rect(center=(225, 406))
            surface.blit(text, font_rect)

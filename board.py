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

    def __init__(self, mapp=None):
        """棋盘初始化"""
        self.map = [[0 for _ in range(4)] for _ in range(4)]
        self.score = 0
        self.best_direction = None

        # 开局先加入两个2
        self.add(True)
        self.add(True)

        if mapp is not None:
            self.map = [[mapp[i][j]
                         for i in range(4)] for j in range(4)]
        self.print_map()

    def __judge_add(self):
        """判断当前是否可以添加数"""

        for i in range(4):
            for j in range(4):
                if self.map[i][j] == 0:
                    return True
        return False

    def __judge_game(self):
        """判断游戏是否可以继续：是否有空方块或者有可以合并的"""

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
        :return: GAME_OVER GAME_ERROR GAME_CONTINUE
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

    def add_xy(self, x, y, value):
        if self.map[x][y] == 0:
            self.map[x][y] = value
            return True
        else:
            return False

    def remove_xy(self, x, y):
        self.map[x][y] = 0

    def getFreeBlocks(self):
        """返回所以空格子的位置(i,j)"""
        FreeBlocks = []
        for i in range(4):
            for j in range(4):
                if self.map[i][j] == 0:
                    FreeBlocks.append([i, j])
        return FreeBlocks

    def move_left(self, is_change=True):
        """
        :param is_change True->改变当前棋盘  False->只是为了判断能否执行该移动
        :function: 棋盘左移
        :return: False不能左移 True可以左移
        """

        single_score = 0
        is_ok = False
        tmp_map = copy.deepcopy(self.map)
        last_map = copy.deepcopy(self.map)  # 修改前的棋盘
        for i in range(4):
            row = tmp_map[i]
            # 将每一行的0都移到后面
            row = sorted(row, key=lambda x: 1 if x == 0 else 0)
            for j in range(3):
                if row[j] == row[j + 1]:
                    single_score += row[j] * 2
                    row[j] += row[j + 1]
                    row[j + 1] = 0
            # 再次更新每一行的0
            row = sorted(row, key=lambda x: 1 if x == 0 else 0)
            tmp_map[i] = row

        now_map = copy.deepcopy(tmp_map)  # 修改后的棋盘
        if now_map != last_map:
            is_ok = True

        if is_change:
            self.map = copy.deepcopy(now_map)
        self.score += single_score
        return is_ok

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

    def move(self, direction, is_change=True):
        if direction == MOVE_LEFT:
            return self.move_left(is_change)
        elif direction == MOVE_UP:
            return self.move_up(is_change)
        elif direction == MOVE_RIGHT:
            return self.move_right(is_change)
        elif direction == MOVE_DOWM:
            return self.move_down(is_change)

    # def tip_direction(self):
    #     """提示操作方向"""
    #     # 循环寻找最大而且可移动的方向
    #     prediction = [0, 0, 0, 0]
    #     for i in range(4):
    #         direction = prediction.index(max(prediction))
    #         if not self.move(direction, False):
    #             prediction[direction] = -1
    #         else:
    #             self.best_direction = direction
    #             break
    #     return self.best_direction

    def print_map(self):
        pass
        # print("当前局势为:")
        # print(tip[self.tip_direction()])
        # for i in range(4):
        #     print(self.map[i])

    # TODO:还想加入一个显示当前在 常规2048 还是 AI2048 的界面
    def update(self, surface, is_tip, bestscore, mode):
        '''
        :param surface:
        :param is_tip:
        :return:
        '''
        mode_text = ["Classic", "Auto"]
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

        surface.fill((205, 170, 125), rect=pygame.Rect(230, 60, 95, 45))
        font = pygame.font.SysFont("Microsoft Sans Serif", 25)
        text = font.render(str(self.score), True, (245, 245, 220))
        font_rect = text.get_rect(centerx=277, centery=82)
        surface.blit(text, font_rect)

        surface.fill((205, 170, 125), rect=pygame.Rect(335, 60, 95, 45))
        font = pygame.font.SysFont("Microsoft Sans Serif", 25)
        text = font.render(str(bestscore), True, (245, 245, 220))
        font_rect = text.get_rect(centerx=382, centery=82)
        surface.blit(text, font_rect)

        surface.fill((255, 250, 240), rect=pygame.Rect(34, 105, 190, 28))
        font = pygame.font.SysFont("consolas", 26)
        text = font.render("Mode:", True, (205, 55, 0))
        surface.blit(text, (35, 106))

        font = pygame.font.SysFont("consolas", 26)
        text = font.render(str(mode_text[mode]), True, (205, 112, 84))
        surface.blit(text, (112, 106))

        if is_tip:
            font = pygame.font.SysFont("consolas", 36)
            text = font.render('tip:' + tip[self.best_direction], True, (100, 100, 10))
            font_rect = text.get_rect(center=(225, 406))
            surface.blit(text, font_rect)

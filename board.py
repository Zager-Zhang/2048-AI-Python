import pygame
import random


# 棋盘类
class Board(object):

    def __init__(self):
        self.map = [[0 for i in range(4)] for j in range(4)]
        # 开局先加入两个数
        self.add()
        self.add()
        self.print_map()

    def add(self):
        """随机添加一个新数字"""
        pos = random.randint(0, 15)
        while self.map[pos // 4][pos % 4] != 0:
            pos = random.randint(1, 16)
        num = random.randint(0, 99)
        num = (lambda x: 4 if x >= 90 else 2)(num) # 十分之一的概率为4
        print(num)
        self.map[pos // 4][pos % 4] = num

    def move_left(self):
        for i in range(4):
            row = self.map[i]
            # 将每一行的0都移到后面
            row = sorted(row, key=lambda x: 1 if x == 0 else 0)
            for j in range(3):
                if row[j] == row[j + 1]:
                    row[j] += row[j + 1]
                    row[j + 1] = 0
            # 再次更新每一行的0
            row = sorted(row, key=lambda x: 1 if x == 0 else 0)
            self.map[i] = row

    def move_right(self):
        self.map = [row[::-1] for row in self.map]
        self.move_left()
        self.map = [row[::-1] for row in self.map]

    def move_up(self):
        # 左旋90°
        self.map_left_rotate90()
        # self.print_map()

        self.move_left()

        # 右旋90°
        self.map_right_rotate90()
        # self.print_map()

    def move_down(self):
        # 左旋90°
        self.map_right_rotate90()
        # self.print_map()

        self.move_left()

        # 右旋90°
        self.map_left_rotate90()
        # self.print_map()

    def print_map(self):
        print("hhh:")
        for i in range(4):
            print(self.map[i])

    def map_left_rotate90(self):
        """ 左旋转90° """
        temp_map = [[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                temp_map[i][j] = self.map[j][3 - i]
        self.map = temp_map

    def map_right_rotate90(self):
        temp_map = [[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                temp_map[i][j] = self.map[3 - j][i]
        self.map = temp_map

# B = Board()
# T = 3
# while T:
#     T -= 1
#     B.move_up()
#     B.print_map()
#     B.add()
#     B.print_map()

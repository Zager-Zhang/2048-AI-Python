import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 450, 630)
# 屏幕刷新率
FRAME_PER_SEC = 60
# 方块中字体的大小
CUBE_NUM_SIZE = 80

# 常规颜色
RED = (255, 0, 0)
LIGHT_RED = (180, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 0, 180)

# 方块的颜色
CUBE_COLORS = [(0, 0, 0), (245, 222, 179), (237, 224, 200), (242, 177, 121), (245, 149, 99), (246, 124, 95),
               (246, 94, 59), (237, 207, 114), (237, 204, 97), (244, 164, 96), (255, 160, 122), (255, 127, 80)]
# 方块中数字的颜色
CUBE_NUM_COLORS = [(95, 95, 95), (249, 246, 242)]

# 棋盘的颜色
BOARD_COLOR = (187, 173, 160)
# 棋盘格的颜色
BOARD_PLAID_COLOR = (205, 193, 180)
# 棋盘的位置
BOARD_RECD = pygame.Rect(20, 200, 400 + 10, 400 + 10)
SIDE_WIDTH = 10
CUBE_WIDTH = 90

# 按钮相关
BUTTON_COLOR = (143, 122, 102)
BUTTON_FONT_COLOR = (255, 255, 255)
BUTTON_FONT_SIZE = 24
BUTTON_START_X = 30
BUTTON_START_Y = 120
BUTTON_SIDE = 10
BUTTON_SIZE = (90, 45)

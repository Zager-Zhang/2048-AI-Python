from config_2048 import *
from button.button import *
from AI.ai_2048 import *
import time


class Game2048(object):

    def __init__(self):
        print("2048游戏初始化...")
        pygame.init()

        # 屏幕相关
        self.screen = pygame.display.set_mode(SCREEN_RECT.size, 0, 32)
        self.screen.fill((255, 250, 240), rect=SCREEN_RECT)
        pygame.display.set_caption("2048——by 张明杰 鄢歆璐 梅阳鸿")

        # 字体相关
        font_EN = pygame.font.SysFont("comicsansms", 85)
        text_title = font_EN.render("2048", True, (119, 110, 101))
        self.screen.blit(text_title, (10, 0))

        # 分数块相关
        self.screen.fill((205, 170, 125), rect=SCORE_RECT)
        font_EN = pygame.font.SysFont("consolas", 26)
        text_title = font_EN.render("Score", True, (245, 245, 220))
        self.screen.blit(text_title, (242, 32))

        self.screen.fill((205, 170, 125), rect=BEST_RECT)
        font_EN = pygame.font.SysFont("consolas", 26)
        text_title = font_EN.render("Best", True, (245, 245, 220))
        self.screen.blit(text_title, (353, 32))

        # 模式相关
        font_EN = pygame.font.SysFont("consolas", 26)
        text_title = font_EN.render("Mode:", True, (0, 0, 0))
        self.screen.blit(text_title, (35, 106))

        # 时钟相关
        self.time = pygame.time.Clock()

        # 按钮显示
        self.button_start = Button(((BUTTON_START_X, BUTTON_START_Y), BUTTON_SIZE), BUTTON_COLOR, "comicsansms",
                                   BUTTON_FONT_COLOR,
                                   BUTTON_FONT_SIZE, "New", BUTTON_START)
        self.button_start.update(self.screen)

        self.button_classic = Button(((BUTTON_START_X + BUTTON_SIDE + BUTTON_SIZE[0], BUTTON_START_Y), BUTTON_SIZE),
                                     BUTTON_COLOR, "comicsansms", BUTTON_FONT_COLOR,
                                     BUTTON_FONT_SIZE, "Classic", BUTTON_CLASSIC)
        self.button_classic.update(self.screen)

        self.button_auto = Button(((BUTTON_START_X + (BUTTON_SIDE + BUTTON_SIZE[0]) * 2, BUTTON_START_Y), BUTTON_SIZE),
                                  BUTTON_COLOR, "comicsansms", BUTTON_FONT_COLOR,
                                  BUTTON_FONT_SIZE, "Auto", BUTTON_AUTO)
        self.button_auto.update(self.screen)

        self.button_tip = Button(((BUTTON_START_X + (BUTTON_SIDE + BUTTON_SIZE[0]) * 3, BUTTON_START_Y), BUTTON_SIZE),
                                 BUTTON_COLOR, "comicsansms", BUTTON_FONT_COLOR,
                                 BUTTON_FONT_SIZE, "Tip", BUTTON_TIP)
        self.button_tip.update(self.screen)

        # 最好分数
        self.best_score = 0
        self.flag_start = False
        self.flag_classic = True
        self.flag_auto = False
        self.flag_tip = False
        self.flag_gameover = False

        # 创建新的棋局
        mapp = [[2, 32, 2, 0],
                [8, 4, 64, 0],
                [2, 32, 128, 1024],
                [4, 8, 256, 4096]]
        self.board = Board()

    def game_start(self):
        print("2048游戏开始...")
        while True:
            mode = 0 if self.flag_classic else 1
            self.best_score = max(self.best_score, self.board.score)

            self.time.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.board.update(self.screen, self.flag_tip, self.best_score, mode)
            pygame.display.update()
            self.__flag_handler()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()

            # 处理键盘事件
            elif event.type == pygame.KEYDOWN:
                if self.flag_classic:
                    self.__keyboard_handler(event.key)

            # 处理按钮事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_start.check_event()
                self.__button_func_handler(self.button_start.func_handler())
                self.button_classic.check_event()
                self.__button_func_handler(self.button_classic.func_handler())
                self.button_auto.check_event()
                self.__button_func_handler(self.button_auto.func_handler())
                self.button_tip.check_event()
                self.__button_func_handler(self.button_tip.func_handler())

    def __flag_handler(self):
        """标志位处理"""
        if self.flag_auto or self.flag_tip:
            self.update_best_direction()

        if self.flag_start:
            self.flag_start = False
            print("新的游戏开始了...")
            self.board = Board()

        if self.flag_auto:
            self.AI_start()

        if self.flag_gameover:
            self.flag_gameover = False
            self.show_game_over()

    def __keyboard_handler(self, key):
        """键盘处理：常规2048相关操作"""
        direction = -1
        if key == pygame.K_DOWN or key == pygame.K_s:
            direction = MOVE_DOWM
        elif key == pygame.K_UP or key == pygame.K_w:
            direction = MOVE_UP
        elif key == pygame.K_LEFT or key == pygame.K_a:
            direction = MOVE_LEFT
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            direction = MOVE_RIGHT

        # 没有使用要求的按键操作
        if direction == -1:
            print("按键错误，请使用正确的按键")
            return None

        # 执行移动操作，并用is_move记录是否成功移动
        is_move = self.board.move(direction)

        # 加数时先判断是否还能继续游戏
        if self.board.add() == GAME_OVER:
            self.flag_gameover = True

        # 可以继续游戏，但可能操作使其无法移动
        if not is_move:
            print(f"不能执行{CHAR_DIRECTION[direction]}动作，请重新操作")
            return None

    def __button_func_handler(self, button_func):
        """处理按钮功能"""

        if button_func == BUTTON_START:
            self.flag_start = True
            self.flag_classic = True
            self.flag_auto = False
        elif button_func == BUTTON_CLASSIC:
            self.flag_classic = True
            self.flag_auto = False
        elif button_func == BUTTON_AUTO:
            self.flag_auto = True
            self.flag_classic = False
        elif button_func == BUTTON_TIP:
            if self.flag_tip:
                self.flag_tip = False
            else:
                self.flag_tip = True

    def update_best_direction(self):
        newboard = Board(self.board.map)

        # 搜索深度随空格子数的减少而增大，可以兼顾速度和质量
        depth = DEPTH
        if 4 <= calculate_empty(newboard.map) <= 7:
            depth = DEPTH + 1
        elif calculate_empty(newboard.map) <= 3:
            depth = DEPTH + 2
        best_direction = getBestMove(newboard, depth)
        self.board.best_direction = best_direction

    # TODO:静态估计AI还存在可能操作不能执行的bug
    def AI_start(self):
        """AI功能"""

        is_ok = self.board.move(self.board.best_direction)

        if self.board.best_direction == -1:  # 无法移动说明游戏结束
            self.show_game_over()
        else:
            self.board.add()

    def show_game_over(self):
        font_end = pygame.font.SysFont("comicsansms", 60)
        text_end = font_end.render("Game Over!", True, (50, 50, 50))
        self.screen.blit(text_end, (60, 300))
        pygame.display.update()
        self.flag_auto = False
        self.flag_tip = False

        time.sleep(2)

    @staticmethod
    def __game_over():
        print("2048游戏结束...")
        pygame.quit()
        exit()

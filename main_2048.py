from board_2048 import *
from button import *
from config_2048 import *
from ai_2048 import *
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
        self.font_EN = pygame.font.SysFont("comicsansms", 75)
        self.text_title = self.font_EN.render("2048", True, (119, 110, 101))
        self.screen.blit(self.text_title, (10, 0))

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

        # 创建新的棋局
        self.board = Board()

    def game_start(self):
        print("2048游戏开始...")
        while True:
            self.time.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__button_handler()
            self.board.update(self.screen, self.flag_tip)
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            # 处理键盘事件
            elif event.type == pygame.KEYDOWN:
                if self.button_classic:
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

    def __button_handler(self):
        """按钮处理"""

        if self.flag_start:
            self.flag_start = False
            print("新的游戏开始了...")
            self.board = Board()
        elif self.flag_classic:
            pass
        elif self.flag_auto:
            self.AI_start()
        elif self.flag_tip:
            pass

    def __keyboard_handler(self, key):
        """键盘处理：常规2048游戏"""
        direction = -1
        if key == pygame.K_DOWN or key == pygame.K_s:
            direction = MOVE_DOWM
        elif key == pygame.K_UP or key == pygame.K_w:
            direction = MOVE_UP
        elif key == pygame.K_LEFT or key == pygame.K_a:
            direction = MOVE_LEFT
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            direction = MOVE_RIGHT

        if direction == -1:
            print("按键错误，请使用正确的按键")
            return None

        is_move = self.board.move(direction)
        if not is_move:
            print(f"不能执行{CHAR_DIRECTION[direction]}动作，请重新操作")
            return None

        if self.board.add() == GAME_OVER:
            font_end = pygame.font.SysFont("comicsansms", 60)
            text_end = font_end.render("Game Over!", True, (50, 50, 50))
            self.screen.blit(text_end, (60, 350))
            pygame.display.update()

            time.sleep(2)
            self.board = Board()
        self.board.print_map()
        self.board.tip_direction()

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

    # TODO:静态估计AI还存在可能操作不能执行的bug
    def AI_start(self):
        """AI功能"""
        newboard = Board(self.board.map)
        best_direction = getBestMove(newboard, DEPTH)
        print(CHAR_DIRECTION[best_direction])
        is_ok = self.board.move(best_direction)

        self.best_score = max(self.best_score, self.board.score)
        print(" score:%d\n best_score:%d" % (self.board.score, self.best_score))

        if self.board.add() == GAME_OVER:
            font_end = pygame.font.SysFont("comicsansms", 60)
            text_end = font_end.render("Game Over!", True, (50, 50, 50))
            self.screen.blit(text_end, (60, 300))
            pygame.display.update()

            time.sleep(2)
            self.board = Board()
        # self.board.print_map()

    @staticmethod
    def __game_over():
        print("2048游戏结束...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game2048 = Game2048()
    game2048.game_start()

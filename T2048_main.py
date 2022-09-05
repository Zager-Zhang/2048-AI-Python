from button import *
from board import *
import time


class T2048Game(object):

    def __init__(self):
        print("2048游戏初始化...")
        pygame.init()

        # 屏幕相关
        # self.Fullscreen = 0
        self.screen = pygame.display.set_mode(SCREEN_RECT.size, 0, 32)
        self.screen.fill((255, 250, 240), rect=SCREEN_RECT)
        pygame.display.set_caption("2048——by Zager Tracy")

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
            self.board.update(self.screen)
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == pygame.KEYDOWN:
                if self.button_classic:
                    self.__keyboard_handler(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_start.check_event()
                self.__button_func_handler(self.button_start.func_handler())
                self.button_classic.check_event()
                self.__button_func_handler(self.button_classic.func_handler())
                self.button_auto.check_event()
                self.__button_func_handler(self.button_auto.func_handler())
                self.button_tip.check_event()
                self.__button_func_handler(self.button_tip.func_handler())

    def AI_start(self):
        best_direction = self.board.tip_direction()
        if best_direction == 0:
            self.board.move_left()
        elif best_direction == 1:
            self.board.move_up()
        elif best_direction == 2:
            self.board.move_right()
        elif best_direction == 3:
            self.board.move_down()

        print(" score:%d\n best_score:%d" % (self.board.score, self.best_score))
        if not self.board.add():
            self.best_score = max(self.best_score, self.board.score)

            font_end = pygame.font.SysFont("comicsansms", 60)
            text_end = font_end.render("Game Over!", True, (50, 50, 50))
            self.screen.blit(text_end, (60, 300))
            pygame.display.update()

            time.sleep(3)
            self.board = Board()
        self.board.print_map()

    def __button_handler(self):
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
        """键盘处理"""

        if key == pygame.K_DOWN or key == pygame.K_s:
            self.board.move_down()
        elif key == pygame.K_UP or key == pygame.K_w:
            self.board.move_up()
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.board.move_left()
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.board.move_right()
        else:
            return None

        self.board.add()
        self.board.print_map()
        self.board.tip_direction()
        # elif key == pygame.K_f:
        #     self.Fullscreen = not self.Fullscreen
        #     if self.Fullscreen:
        #         self.screen = pygame.display.set_mode(SCREEN_RECT.size, pygame.FULLSCREEN, 32)
        #     else:
        #         self.screen = pygame.display.set_mode(SCREEN_RECT.size, 0, 32)

    def __button_func_handler(self, button_func):
        """处理按钮功能"""

        if button_func == BUTTON_START:
            self.flag_start = True
        elif button_func == BUTTON_CLASSIC:
            self.flag_classic = True
            self.flag_auto = False
        elif button_func == BUTTON_AUTO:
            self.flag_auto = True
            self.flag_classic = False
        elif button_func == BUTTON_TIP:
            self.flag_tip = True

    @staticmethod
    def __game_over():
        print("2048游戏结束...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game2048 = T2048Game()
    game2048.game_start()

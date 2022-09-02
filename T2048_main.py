from T2048 import *
from button import *
from board import *


class T2048Game(object):

    def __init__(self):
        print("2048游戏初始化...")
        pygame.init()

        # 屏幕相关
        self.Fullscreen = 0
        self.screen = pygame.display.set_mode(SCREEN_RECT.size, 0, 32)
        pygame.display.set_caption("2048——by ZAGER")

        # 字体相关
        self.font_ZH = pygame.font.SysFont("SimHei", 50)
        self.font_EN = pygame.font.SysFont("arial", 50)
        self.text_title = self.font_EN.render("2048", True, (255, 0, 0))
        self.screen.blit(self.text_title, (0, 0))

        # 时钟相关
        self.time = pygame.time.Clock()

        # 按钮测试
        self.button1 = Button(((100, 100), (100, 100)), RED, "arial", BLUE, 40, "New", BUTTON_START)
        self.button1.update(self.screen)

        self.button2 = Button(((100, 200), (100, 100)), GREEN, "arial", BLUE, 40, "Quit", BUTTON_QUIT)
        self.button2.update(self.screen)

        # 创建新的棋局
        self.board = Board()

    def game_start(self):
        print("2048游戏开始...")
        while True:
            self.time.tick(60)
            self.__event_handler()

            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over()
            elif event.type == pygame.KEYDOWN:
                self.__keyboard_handler(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button1.check_event()
                self.__button_func_handler(self.button1.func_handler())
                self.button2.check_event()
                self.__button_func_handler(self.button2.func_handler())

    def __keyboard_handler(self, key):
        """按键处理"""

        if key == pygame.K_DOWN or key == pygame.K_s:
            self.board.move_down()
            self.board.add()
            self.board.print_map()
        elif key == pygame.K_UP or key == pygame.K_w:
            self.board.move_up()
            self.board.add()
            self.board.print_map()
        elif key == pygame.K_LEFT or key == pygame.K_a:
            self.board.move_left()
            self.board.add()
            self.board.print_map()
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.board.move_right()
            self.board.add()
            self.board.print_map()
        # elif key == pygame.K_f:
        #     self.Fullscreen = not self.Fullscreen
        #     if self.Fullscreen:
        #         self.screen = pygame.display.set_mode(SCREEN_RECT.size, pygame.FULLSCREEN, 32)
        #     else:
        #         self.screen = pygame.display.set_mode(SCREEN_RECT.size, 0, 32)

    def __button_func_handler(self, button_func):
        """处理按钮功能"""

        if button_func == BUTTON_START:
            print("游戏开始")
            self.board = Board()
        elif button_func == BUTTON_QUIT:
            self.__game_over()

    @staticmethod
    def __game_over():
        print("2048游戏结束...")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game2048 = T2048Game()
    game2048.game_start()

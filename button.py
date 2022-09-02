import pygame

BUTTON_START = 1
BUTTON_QUIT = 2


class Button(object):

    def __init__(self, rect, rect_color, font, text_color, text_size, text, func, **kwargs):
        """
        按键初始化
        :param rect:       按键大小和位置
        :param rect_color: 按键颜色
        :param font:       字体
        :param text_color: 字体颜色
        :param text_size:  字体大小
        :param text:       按键上显示文本
        :param func:       功能
        :param kwargs: 
        """
        self.rect = pygame.Rect(rect)
        self.rect_color = rect_color
        self.font = pygame.font.SysFont(font, text_size)
        self.text_color = text_color
        self.text_size = text_size
        self.text = self.font.render(text, True, self.text_color)
        self.func = func

        # 按钮的状态
        self.status = 0

    def check_event(self):
        """检测是否按下按键"""

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.status = 1

    def func_handler(self):
        """返回按钮的功能"""

        if self.status:
            self.status = 0
            return self.func

    def update(self, surface):
        """绘制按钮的文本和方框"""

        text_rect = self.text.get_rect(center=self.rect.center)
        surface.fill(self.rect_color, rect=self.rect)
        surface.blit(self.text, text_rect)
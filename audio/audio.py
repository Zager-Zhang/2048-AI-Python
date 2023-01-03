import pygame
import time


def show_click_audio():
    pygame.mixer.Sound("./audio/button_click.wav").play()


def show_over_audio():
    pygame.mixer.Sound("./audio/game_over.wav").play()


def show_error_audio():
    pygame.mixer.Sound("./audio/error_move.wav").play()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    while True:
        show_click_audio()
        time.sleep(1)

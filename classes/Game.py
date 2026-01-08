import pygame


class Game:

    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Ski Alpin 2D")
        self.clock = pygame.time.Clock()
        self.snow_color = (200, 200, 255)
        self.game_over_color = (255, 0, 0)
        self.level = 1

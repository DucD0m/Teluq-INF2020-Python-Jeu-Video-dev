import random

class Obstacle:

    def __init__(self, window_width, start_y, spacing, image):
        self.image = image
        self.min = 4*spacing + 70
        self.max = window_width - self.image.get_width() - 4*spacing
        self.x = random.randint(self.min, self.max)
        self.y = start_y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.cleared = False

    def update_rect(self):
        self.rect.topleft = (self.x + 10, self.y + 10)
        self.rect.width = self.image.get_width() - 20
        self.rect.height = self.image.get_height() - 20

    def draw(self, window, start_y, speed):
        self.y -= speed
        if self.y < 0:
            self.cleared = False
            self.y = start_y
            self.x = random.randint(self.min, self.max)
        window.blit(self.image, (self.x, self.y))

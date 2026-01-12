import random

class Obstacle:

    def __init__(self, window_height, window_left_limit, window_right_limit, image, jump_allowed):
        self.image = image
        self.y = window_height + random.randint(0,window_height)
        self.x = random.randint(window_left_limit + 50, window_right_limit - 50)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.width = self.image.get_width() - 20
        self.rect.height = self.image.get_height() - 20
        self.cleared = False
        self.jump_allowed = jump_allowed

    def update_rect(self):
        self.rect.topleft = (self.x + 10, self.y + 10)

    def set_cleared(self):
        self.cleared = True

    def update_position(self,window_height, window_left_limit, window_right_limit, speed):
        self.y -= speed
        if self.y < 0:
            self.cleared = False
            self.y = window_height + random.randint(0,window_height)
            self.x = random.randint(window_left_limit + 50, window_right_limit - 50)

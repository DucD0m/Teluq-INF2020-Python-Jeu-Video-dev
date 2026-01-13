import random


class Obstacle:

    def __init__(self, height, left_limit, right_limit, image, jump_allowed):
        self.image = image
        self.y = height + random.randint(0, height)
        self.x = random.randint(left_limit + 50, right_limit - 50)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.width = self.image.get_width() - 20
        self.rect.height = self.image.get_height() - 20
        self.cleared = False
        self.jump_allowed = jump_allowed

    def update_rect(self):
        self.rect.topleft = (self.x + 10, self.y + 10)

    def set_cleared(self):
        self.cleared = True

    def update_position(self, height, left_limit, right_limit, speed):
        self.y -= speed
        if self.y < -self.image.get_height():
            self.cleared = False
            self.y = height + random.randint(0, height)
            self.x = random.randint(left_limit + 50, right_limit - 50)

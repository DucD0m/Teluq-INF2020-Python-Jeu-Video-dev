class Player:
    def __init__(self, window_width, image_left, image_right):
        self.image_left = image_left
        self.image_right = image_right
        self.image = self.image_left

        self.starting_x = window_width // 2 - self.image.get_width() // 2
        self.starting_y = self.image.get_height() + 20
        self.x = self.starting_x
        self.y = self.starting_y

        self.rect = self.image.get_rect(topleft=(self.x + 10, self.y + 10))
        self.rect.width -= 20
        self.rect.height -= 20

        self.speed = 5
        self.dx = 0
        self.mx = 0

        self.starting_lives = 3
        self.lives = self.starting_lives
        self.points = 0

        self.invincible = False
        self.invincible_time = 0.0
        self.invincible_duration = 3.0

        self.stop_points = False
        self.stop_points_time = 0.0
        self.stop_points_duration = 3.0

        self.jumping = False
        self.jump_time = 0.0
        self.jump_duration = 1.5
        self.jump_x = self.x
        self.angle = 0.0
        self.scale = 1.0

    def input(self, keys, height, left_limit, right_limit):
        self.horizontal_move(keys)
        self.vertical_move(keys)
        self.jump_move(keys)
        self.position_limits(height, left_limit, right_limit)

    def horizontal_move(self, keys):
        if not self.jumping:
            if keys["left"]:
                self.dx = -self.speed
                self.mx = -self.speed
                self.image = self.image_left
            elif keys["right"]:
                self.dx = self.speed
                self.mx = self.speed
                self.image = self.image_right
            else:
                self.dx = self.mx
        else:
            self.dx = 0

        self.x += self.dx

    def vertical_move(self, keys):
        if keys["up"]:
            self.y -= self.speed
        if keys["down"]:
            self.y += self.speed

    def jump_move(self, keys):
        if keys["space"] and not self.jumping:
            self.jumping = True
            self.jump_time = 0.0
            self.jump_x = self.x

    def position_limits(self, height, left_limit, right_limit):
        self.x = max(left_limit, min(self.x, right_limit))
        self.y = max(0, min(self.y, height - self.image.get_height()))

    def update(self, dt):
        self.update_rect()
        self.update_invincibility(dt)
        self.update_stop_points(dt)
        self.update_jump(dt)

    def update_rect(self):
        self.rect.topleft = (self.x + 10, self.y + 10)

    def update_invincibility(self, dt):
        if self.invincible:
            self.invincible_time += dt
            if self.invincible_time >= self.invincible_duration:
                self.invincible = False

    def update_stop_points(self, dt):
        if self.stop_points:
            self.stop_points_time += dt
            if self.stop_points_time >= self.stop_points_duration:
                self.stop_points = False

    def update_jump(self, dt):
        if self.jumping:
            self.jump_time += dt
            t = self.jump_time / self.jump_duration
            if t >= 1.0:
                t = 1.0
                self.jumping = False
                self.angle = 0.0
                self.scale = 1.0

            if t < 0.5:
                self.scale = 1.0 + t * 2
                self.angle = t * 360
            else:
                self.scale = 2.0 - (t - 0.5) * 2
                self.angle = 180 + (t - 0.5) * 360

    def obstacle_cleared(self):
        self.points += 25

    def obstacle_jumped(self):
        self.points += 100
        self.stop_points = True
        self.stop_points_time = 0.0

    def obstacle_hit(self):
        self.lives -= 1
        self.invincible = True
        self.invincible_time = 0.0

    def reset(self):
        self.lives = self.starting_lives
        self.points = 0
        self.x = self.starting_x
        self.y = self.starting_y
        self.invincible = True
        self.invincible_time = 0.0

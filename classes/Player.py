import pygame

class Player:
    def __init__(self, window_width):
        self.size = 100
        self.starting_x = window_width // 2 - self.size // 2
        self.starting_y = self.size + 20
        self.x = self.starting_x
        self.y = self.starting_y
        self.speed = 5

        # Charger les images
        self.image_left = pygame.transform.scale(
            pygame.image.load("images/Skier-PNG-Photos-sm.png"), (self.size, self.size)
        )
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_left  # image actuelle

        # Hitbox ajustée
        self.rect = self.image.get_rect(topleft=(self.x + 5, self.y + 5))
        self.rect.width -= 10
        self.rect.height -= 10

        # Mouvements
        self.dx = 0
        self.mx = 0

        # Stats
        self.starting_lives = 3
        self.lives = self.starting_lives
        self.points = 0
        self.invincible = False
        self.invincible_time = 0.0
        self.invincible_duration = 3.0
        self.stop_points = False
        self.stop_points_time = 0.0
        self.stop_points_duration = 3.0

        # Saut / animation
        self.jumping = False
        self.jump_time = 0.0
        self.jump_duration = 1.5
        self.jump_x = self.x
        self.angle = 0.0
        self.scale = 1.0

    def input(self, keys, window):
        """Gère le mouvement horizontal et le saut"""
        if not self.jumping:
            if keys[pygame.K_LEFT]:
                self.dx = -self.speed
                self.mx = -self.speed
                self.image = self.image_left
            elif keys[pygame.K_RIGHT]:
                self.dx = self.speed
                self.mx = self.speed
                self.image = self.image_right
            else:
                self.dx = self.mx
        else:
            self.dx = 0

        # Déplacement vertical simple
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.jump_time = 0.0
            self.jump_x = self.x

        # Limites horizontales
        self.x += self.dx
        self.x = max(window.left_limit, min(self.x, window.right_limit))

        # Limites verticales
        self.y = max(0, min(self.y, window.height - self.size))

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_time = 0.0
            self.jump_x = self.x

    def update(self, dt):
        self.update_rect()

        # Gestion invincibilité
        if self.invincible:
            self.invincible_time += dt
            if self.invincible_time >= self.invincible_duration:
                self.invincible = False

        # Gestion stop points
        if self.stop_points:
            self.stop_points_time += dt
            if self.stop_points_time >= self.stop_points_duration:
                self.stop_points = False

        # Animation du saut
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

    def get_transformed_image(self):
        """Retourne l'image transformée (rotation + scale)"""
        return pygame.transform.rotozoom(self.image, -self.angle, self.scale)

    def update_rect(self):
        """Met à jour la hitbox"""
        self.rect.topleft = (self.x + 10, self.y + 10)
        self.rect.width = self.size - 20
        self.rect.height = self.size - 20

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

    def draw(self, window):
        transformed = self.get_transformed_image()
        rect = transformed.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        draw_player = True

        if self.invincible:
            draw_player = int(self.invincible_time * 10) % 2 == 0

        if draw_player:
            if self.jumping:
                window.blit(transformed, rect)
            else:
                window.blit(self.image, (self.x, self.y))

    def reset(self):
        self.lives = self.starting_lives
        self.points = 0
        self.x = self.starting_x
        self.y = self.starting_y
        self.invincible = True
        self.invincible_time = 0.0

import pygame

class Window:

    def __init__(self, width, height):
        if not pygame.get_init():
            pygame.init()
        self.width = width
        self.height = height
        self.spacing = 50
        self.dx = self.spacing
        self.alignment = -10
        self.num_rows = self.height // self.spacing
        self.left_limit = 4 * self.spacing - 50
        self.right_limit = self.width - 4 * self.spacing - 50
        self.white = (255, 255, 255)
        self.blue = (50, 50, 255)
        self.snow_color = (200, 200, 255)
        self.red = (255, 0, 0)
        self.font_default = pygame.font.SysFont(None, 36)
        self.font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 18)
        self.big_tree = pygame.transform.scale(pygame.image.load("images/Winter-Tree-PNG-File.png"), (200, 200))
        self.big_skier = pygame.transform.scale(pygame.image.load("images/Skier-PNG-Photos.png"), (200, 200))
        self.tree = pygame.transform.scale(pygame.image.load("images/Winter-Tree-PNG-File-sm.png"), (70, 70))
        self.rock = pygame.transform.scale(pygame.image.load("images/Stones-Transparent-Isolated-Background-sm.png"), (90, 60))
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ski Alpin 2D")

    def show_text(self, text, x, y, color):
            text_render = self.font.render(text, True, color)
            text_rect = text_render.get_rect(center=(x, y))
            self.display.blit(text_render, text_rect)

    def show_start_screen(self):
            self.display.fill(self.blue)

            self.show_text(
                "SKI ALPIN 2D",
                self.width // 2,
                self.height // 3,
                self.white
            )

            self.show_text(
                "Appuyer sur RETOUR pour débuter",
                self.width // 2,
                self.height*2 // 3,
                self.white
            )

            self.display.blit(self.big_tree,[200,200])
            self.display.blit(self.big_skier,[self.width - 400,200])

    def show_game_over_screen(self, game, player):
            self.display.fill(self.red)

            self.show_text(
                "LA PARTIE EST TERMINÉE",
                self.width // 2,
                self.height // 4,
                self.white
            )

            self.show_text(
                f"Niveau : {game.level}",
                self.width // 2,
                self.height // 2 - 25,
                self.white
            )

            self.show_text(
                f"Points : {player.points}",
                self.width // 2,
                self.height // 2 + 25,
                self.white
            )

            self.show_text(
                "Appuyer sur RETOUR pour recommencer",
                self.width // 2,
                self.height*2.5 // 3,
                self.white
            )

            self.display.blit(self.big_tree,[200,200])
            self.display.blit(self.big_skier,[self.width - 400,200])

    def update_side_limit_fillers(self, speed):
            for i in range(-1, self.num_rows):
                x = i * self.spacing + self.dx
                self.display.blit(self.tree,[self.alignment,x])
                self.display.blit(self.tree,[self.spacing+self.alignment,x])
                self.display.blit(self.tree,[(2*self.spacing+self.alignment),x])
                self.display.blit(self.tree,[(3*self.spacing+self.alignment),x])
                self.display.blit(self.tree,[self.width-(4*self.spacing-self.alignment),x])
                self.display.blit(self.tree,[self.width-(3*self.spacing-self.alignment),x])
                self.display.blit(self.tree,[self.width-(2*self.spacing-self.alignment),x])
                self.display.blit(self.tree,[self.width-self.spacing+self.alignment,x])
            self.dx -= speed
            if self.dx <= 0:
                self.dx += self.spacing

    def update_status(self, game, player):
        game.level = player.points // 1000 + 1
        game.speed = game.level + 1
        level_text =self.font.render(f"Niveau : {game.level}", True, (0, 0, 0))
        lives_text =self.font.render(f"Vies : {player.lives}", True, (0, 0, 0))
        points_text =self.font.render(f"Points : {player.points}", True, (0, 0, 0))
        self.display.blit(level_text, (300, 20))
        self.display.blit(lives_text, (600, 20))
        self.display.blit(points_text, (900, 20))


class Game:

    def __init__(self):
        if not pygame.get_init():
            pygame.init()
        self.started = False
        self.clock = pygame.time.Clock()
        self.level = 1
        self.speed = 2
        self.keys = ""

    def check_game_started(self):
        if self.keys[pygame.K_RETURN]:
            self.started = True

    def check_restart_game(self, player, dt):
        if self.keys[pygame.K_RETURN]:
            self.level = 1
            player.reset()
            player.update(dt)

    def update_key_pressed(self):
        self.keys = pygame.key.get_pressed()

    def check_collision(self, window, player, obstacle):
        if player.rect.colliderect(obstacle.rect) and not player.invincible and (not player.jumping or not obstacle.jump_allowed):
            player.lives -= 1
            player.invincible = True
            player.invincible_time = 0.0

        elif player.rect.colliderect(obstacle.rect) and not player.invincible and obstacle.jump_allowed and player.jumping and not player.stop_points:
            player.points += 100
            player.stop_points = True
            player.stop_points_time = 0.0

        if (player.x <= window.left_limit or player.x >= window.right_limit) and not player.invincible:
            player.lives -= 1
            player.invincible = True
            player.invincible_time = 0.0

    def check_obstacle_cleared(self, player, obs):
        if player.y > obs.y:
            if obs.cleared == False:
                player.points += 25
                obs.cleared = True

    def check_quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def flip(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()

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
        self.left_limit = 3 * self.spacing
        self.right_limit = self.width - 5 * self.spacing
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.blue = (50, 50, 255)
        self.snow_color = (200, 200, 255)
        self.red = (255, 0, 0)
        self.font_default = pygame.font.SysFont(None, 36)
        self.font_retro = pygame.font.Font("fonts/PressStart2P-Regular/PressStart2P-Regular.ttf", 18)
        self.font_snow = pygame.font.Font("fonts/ice-and-snow-font/IceAndsnowNormal-2ve8.ttf", 216)
        self.big_skier = pygame.transform.scale(pygame.image.load("images/Skier-PNG-Photos.png"), (200, 200))
        self.big_tree = pygame.transform.scale(pygame.image.load("images/Winter-Tree-PNG-File.png"), (200, 200))
        self.skier_left = pygame.transform.scale(pygame.image.load("images/Skier-PNG-Photos-sm.png"), (100, 100))
        self.skier_right = pygame.transform.flip(self.skier_left, True, False)
        self.tree = pygame.transform.scale(pygame.image.load("images/Winter-Tree-PNG-File-sm.png"), (70, 70))
        self.rock = pygame.transform.scale(pygame.image.load("images/Stones-Transparent-Isolated-Background-sm.png"), (90, 60))
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ski Alpin 2D")

    def show_text(self, text, x, y, color, font):
            text_render = font.render(text, True, color)
            text_rect = text_render.get_rect(center=(x, y))
            self.display.blit(text_render, text_rect)

    def show_start_screen(self):
            self.display.fill(self.blue)

            self.show_text(
                "SKI ALPIN 2D",
                self.width // 2,
                self.height // 3,
                self.white,
                self.font_snow
            )

            self.show_text(
                "Appuyer sur RETOUR pour débuter",
                self.width // 2,
                self.height*2 // 3,
                self.white,
                self.font_retro
            )

            self.display.blit(self.big_tree,[100,self.height // 2])
            self.display.blit(self.big_skier,[self.width - 300,self.height // 2])

    def show_game_over_screen(self, game_level, player_points):
            self.display.fill(self.red)

            self.show_text(
                "LA PARTIE EST TERMINÉE",
                self.width // 2,
                self.height // 4,
                self.white,
                self.font_retro
            )

            self.show_text(
                f"Niveau : {game_level}",
                self.width // 2,
                self.height // 2 - 25,
                self.white,
                self.font_retro
            )

            self.show_text(
                f"Points : {player_points}",
                self.width // 2,
                self.height // 2 + 25,
                self.white,
                self.font_retro
            )

            self.show_text(
                "Appuyer sur RETOUR pour recommencer",
                self.width // 2,
                self.height*2.5 // 3,
                self.white,
                self.font_retro
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

    def update_status(self, game_level, player_lives, player_points):
        self.show_text(
            f"Niveau : {game_level}",
            self.width // 4,
            20,
            self.black,
            self.font_retro
        )
        self.show_text(
            f"Vies : {player_lives}",
            self.width // 2,
            20,
            self.black,
            self.font_retro
        )
        self.show_text(
            f"Points : {player_points}",
            self.width*3 // 4,
            20,
            self.black,
            self.font_retro
        )

    def draw(self, image, x, y):
        if y < self.height or y > -image.get_height():
            self.display.blit(image, (x, y))

    def draw_player(self, player):
        """Attention, cette fonction reçoit directement un objet qui est donc mutables."""
        transformed = self.transform_player_image(player.image, player.angle, player.scale)
        rect = transformed.get_rect(center=(player.x + player.image.get_width()//2, player.y + player.image.get_height()//2))
        draw_player = True

        if player.invincible:
            draw_player = int(player.invincible_time * 10) % 2 == 0

        if draw_player:
            if player.jumping:
                self.display.blit(transformed, rect)
            else:
                self.draw(player.image, player.x, player.y)

    def transform_player_image(self, player_image, player_angle, player_scale):
        return pygame.transform.rotozoom(player_image, -player_angle, player_scale)

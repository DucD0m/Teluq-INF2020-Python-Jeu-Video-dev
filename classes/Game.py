import pygame


class Game:

    def __init__(self, width, height):
        pygame.init()
        self.started = False
        self.width = width
        self.height = height
        self.spacing = 50
        self.alignment = -10
        self.dx = self.spacing
        self.num_rows = self.height // self.spacing
        self.window = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Ski Alpin 2D")
        self.clock = pygame.time.Clock()
        self.white = (255, 255, 255)
        self.blue = (50, 50, 255)
        self.snow_color = (200, 200, 255)
        self.red = (255, 0, 0)
        self.level = 1
        self.speed = 2
        self.big_tree = pygame.transform.scale(pygame.image.load("images/Winter-Tree-PNG-File.png"), (200, 200))
        self.big_skier = pygame.transform.scale(pygame.image.load("images/Skier-PNG-Photos.png"), (200, 200))
        self.tree = pygame.transform.scale(pygame.image.load("images/Winter-Tree-PNG-File-sm.png"), (70, 70))
        self.rock = pygame.transform.scale(pygame.image.load("images/Stones-Transparent-Isolated-Background-sm.png"), (90, 60))
        self.left_limit = 4 * self.spacing - 50
        self.right_limit = self.width - 4 * self.spacing - 50
        self.keys = ""

    def show_text(self, text, x, y, color):
        text_render = self.font.render(text, True, color)
        text_rect = text_render.get_rect(center=(x, y))
        self.window.blit(text_render, text_rect)

    def show_start_screen(self):
        self.window.fill(self.blue)

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

        self.window.blit(self.big_tree,[200,200])
        self.window.blit(self.big_skier,[self.width - 400,200])

        if self.keys[pygame.K_RETURN]:
            self.started = True

    def show_game_over_screen(self, player, dt):
        self.window.fill(self.red)

        self.show_text(
            "LA PARTIE EST TERMINÉE",
            self.width // 2,
            self.height // 4,
            self.white
        )

        self.show_text(
            f"Niveau : {self.level}",
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

        self.window.blit(self.big_tree,[200,200])
        self.window.blit(self.big_skier,[self.width - 400,200])

        if self.keys[pygame.K_RETURN]:
            self.level = 1
            player.reset()
            player.update(dt)

    def update_key_pressed(self):
        self.keys = pygame.key.get_pressed()

    def update_status(self, player):
        self.level = player.points // 1000 + 1
        self.speed = self.level + 1
        self.level_text =self.font.render(f"Niveau : {self.level}", True, (0, 0, 0))
        lives_text =self.font.render(f"Vies : {player.lives}", True, (0, 0, 0))
        points_text =self.font.render(f"Points : {player.points}", True, (0, 0, 0))
        self.window.blit(self.level_text, (400, 20))
        self.window.blit(lives_text, (600, 20))
        self.window.blit(points_text, (800, 20))

    def update_side_limit_fillers(self):
        for i in range(-1, self.num_rows):
            x = i * self.spacing + self.dx
            self.window.blit(self.tree,[self.alignment,x])
            self.window.blit(self.tree,[self.spacing+self.alignment,x])
            self.window.blit(self.tree,[(2*self.spacing+self.alignment),x])
            self.window.blit(self.tree,[(3*self.spacing+self.alignment),x])
            self.window.blit(self.tree,[self.width-(4*self.spacing-self.alignment),x])
            self.window.blit(self.tree,[self.width-(3*self.spacing-self.alignment),x])
            self.window.blit(self.tree,[self.width-(2*self.spacing-self.alignment),x])
            self.window.blit(self.tree,[self.width-self.spacing+self.alignment,x])
        self.dx -= self.speed
        if self.dx <= 0:
            self.dx += self.spacing

    def check_quit_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def flip(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()

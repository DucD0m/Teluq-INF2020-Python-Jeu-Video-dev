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
        self.black = (0, 0, 0)
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
        self.show_text(
            f"Niveau : {game.level}",
            self.width // 4,
            20,
            self.black
        )
        self.show_text(
            f"Vies : {player.lives}",
            self.width // 2,
            20,
            self.black
        )
        self.show_text(
            f"Points : {player.points}",
            self.width*3 // 4,
            20,
            self.black
        )


class Game:

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        if not pygame.get_init():
            pygame.init()
        pygame.mixer.init()
        self.started = False
        self.clock = pygame.time.Clock()
        self.level = 1
        self.speed = 2
        self.keys = ""
        self.sound_points = pygame.mixer.Sound("audio/points.wav")
            # Sound from https://www.bfxr.net/
        self.sound_doh = pygame.mixer.Sound("audio/Homer-Doh! - QuickSounds.com.mp3")
        self.sound_woohoo = pygame.mixer.Sound("audio/WOOHOO! (homer) - QuickSounds.com.mp3")
            # Sounds from https://quicksounds.com/library/sounds/homer
        self.sound_killed = pygame.mixer.Sound("audio/killed.wav")
        pygame.mixer.music.load("audio/Pandemia(chosic.com).mp3")
            # Pandemia by MaxKoMusic | https://maxkomusic.com/
            # Music promoted by https://www.chosic.com/free-music/all/
            # Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
            # https://creativecommons.org/licenses/by-sa/3.0/

    def game_started(self):
        if self.keys[pygame.K_RETURN]:
            self.started = True
            pygame.mixer.music.play(-1)  # boucle infinie

    def restart_game(self):
        if self.keys[pygame.K_RETURN]:
            self.level = 1
            pygame.mixer.music.unpause()
            return True
        else:
            return False

    def update_key_pressed(self):
        self.keys = pygame.key.get_pressed()

    def check_collision(self, window, player, obstacle):
        if player.rect.colliderect(obstacle.rect) and not player.invincible and (not player.jumping or not obstacle.jump_allowed):
            return "hit"
        elif player.rect.colliderect(obstacle.rect) and not player.invincible and obstacle.jump_allowed and player.jumping and not player.stop_points:
            return "jumped"
        elif (player.x <= window.left_limit or player.x >= window.right_limit) and not player.invincible:
            return "hit"
        else:
            return False

    def check_obstacle_cleared(self, player, obs):
        if player.y <= obs.y or obs.cleared:
            return False
        else:
            return True

    def obstacle_hit(self, player_lives):
        if player_lives == 0:
            self.sound_killed.play()
            pygame.mixer.music.pause()
        else:
            self.sound_doh.play()

    def obstacle_cleared(self):
        self.sound_points.play()

    def obstacle_jumped(self):
        self.sound_woohoo.play()

    def update_status(self, player):
        self.level = player.points // 1000 + 1
        self.speed = self.level + 1

    def check_quit_event(self):
        quit_event = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True

        return quit_event

    def flip(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()

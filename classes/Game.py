import pygame


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

    def update_status(self, player_points):
        self.level = player_points // 1000 + 1
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

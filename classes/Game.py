"""
Module définissant la classe Game.

Ce module contient la classe Game, responsable de la logique globale du jeu.
Elle gère :
- l'initialisation de pygame et du système audio,
- l'état de la partie (début, redémarrage, fin),
- le niveau et la vitesse du jeu,
- les entrées clavier,
- les collisions et leurs effets,
- les sons et la musique de fond.

La classe Game agit comme un contrôleur central reliant le joueur,
la fenêtre et les obstacles, elle est une sous-classe de la classe
AssetManager.

Classes:
    AssetManager: Fournit des utilitaires simples pour signaler les problèmes
        de chargement de fichiers (images, sons, polices, etc.)
"""
import pygame
from classes.AssetManager import AssetManager


class Game(AssetManager):
    """Gère la logique principale et l'état global du jeu."""

    def __init__(self):
        """Initialise le jeu, pygame et les ressources audio.

        # pragma: no cover signifie que les lignes associées ne sont
        pas calculées dans le calcul de couverture des tests unittest.
        """
        pygame.mixer.pre_init(44100, -16, 2, 512)

        if not pygame.get_init():
            pygame.init()  # pragma: no cover

        pygame.mixer.init()

        self.started = False
        self.clock = pygame.time.Clock()
        self.level = 1
        self.speed = 1
        self.keys = ""

        # github.com/RobertGodin/CodePython/tree/master/chapitre8/Son1.wav
        sound_killed_path = "audio/killed.wav"

        # Sound from https://www.bfxr.net/
        sound_points_path = "audio/points.wav"

        # Sounds from https://quicksounds.com/library/sounds/homer
        sound_doh_path = "audio/Homer-Doh! - QuickSounds.com.mp3"
        sound_woohoo_path = "audio/WOOHOO! (homer) - QuickSounds.com.mp3"

        # Pandemia by MaxKoMusic | https://maxkomusic.com/
        # Music promoted by https://www.chosic.com/free-music/all/
        # Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
        # https://creativecommons.org/licenses/by-sa/3.0/
        music_path = "audio/Pandemia(chosic.com).mp3"

        try:
            self.sound_killed = pygame.mixer.Sound(sound_killed_path)
        except FileNotFoundError:
            self.sound_killed = None
            super().print_file_missing_error(sound_killed_path)

        try:
            self.sound_points = pygame.mixer.Sound(sound_points_path)
        except FileNotFoundError:
            self.sound_points = None
            super().print_file_missing_error(sound_points_path)

        try:
            self.sound_doh = pygame.mixer.Sound(sound_doh_path)
        except FileNotFoundError:
            self.sound_doh = None
            super().print_file_missing_error(sound_doh_path)

        try:
            self.sound_woohoo = pygame.mixer.Sound(sound_woohoo_path)
        except FileNotFoundError:
            self.sound_woohoo = None
            super().print_file_missing_error(sound_woohoo_path)

        try:
            pygame.mixer.music.load(music_path)
            self.music = True
        except pygame.error:
            self.music = False
            super().print_file_missing_error(music_path)

    def game_started(self):
        """Démarre la partie lorsque la touche Entrée est pressée."""
        if self.keys["return"]:
            self.started = True
            if self.music:
                pygame.mixer.music.play(-1)  # boucle infinie

    def restart_game(self):
        """Redémarre la partie si la touche Entrée est pressée.

        Returns:
            bool: True si la partie doit redémarrer, False sinon.
        """
        if self.keys["return"]:
            self.level = 1
            if self.music:
                pygame.mixer.music.unpause()
            return True

        return False

    def update_key_pressed(self):
        """Met à jour l'état des touches clavier pressées."""
        pressed = pygame.key.get_pressed()
        self.keys = {
            "left": pressed[pygame.K_LEFT],
            "right": pressed[pygame.K_RIGHT],
            "up": pressed[pygame.K_UP],
            "down": pressed[pygame.K_DOWN],
            "space": pressed[pygame.K_SPACE],
            "return": pressed[pygame.K_RETURN]
        }

    def check_collision(self, window, player, obstacle):
        """Détecte une collision entre le joueur et un obstacle visible.

        Cette méthode gère plusieurs cas :
        - collision classique (perte de vie),
        - obstacle sauté avec succès (gain de points),
        - sortie des limites latérales.

        Attention :
            Cette méthode reçoit directement des objets mutables
            (window, player, obstacle).

        Args:
            window (Window): Fenêtre du jeu.
            player (Player): Joueur.
            obstacle (Obstacle): Obstacle testé.

        Returns:
            str | bool: "hit", "jumped" ou False s'il n'y a pas de collision.
        """
        visible = -obstacle.image.get_height() < obstacle.y < window.height

        if visible:
            collision = player.rect.colliderect(obstacle.rect)
        else:
            collision = False

        if (
            collision
            and not player.invincible
            and (not player.jumping or not obstacle.jump_allowed)
        ):
            return "hit"

        if (
            collision
            and not player.invincible
            and obstacle.jump_allowed
            and player.jumping
            and not player.stop_points
        ):
            return "jumped"

        if (
            not player.invincible
            and (
                player.x <= window.left_limit
                or player.x >= window.right_limit
            )
        ):
            return "hit"

        return False

    def check_obstacle_cleared(self, player_y, obs_y, obs_cleared):
        """Vérifie si un obstacle a été dépassé par le joueur.

        Args:
            player_y (int): Position verticale du joueur.
            obs_y (int): Position verticale de l'obstacle.
            obs_cleared (bool): Indique si l'obstacle a déjà été comptabilisé.

        Returns:
            bool: True si l'obstacle est franchi pour la première fois.
        """
        if player_y <= obs_y or obs_cleared:
            return False
        else:
            return True

    def obstacle_hit(self, player_lives):
        """Joue le son approprié lorsqu'un obstacle est touché.

        Args:
            player_lives (int): Nombre de vies restantes du joueur.
        """
        if player_lives == 0:
            if self.sound_killed:
                self.sound_killed.play()
            if self.music:
                pygame.mixer.music.pause()
        else:
            if self.sound_doh:
                self.sound_doh.play()

    def obstacle_cleared(self):
        """Joue le son associé au passage d'un obstacle."""
        if self.sound_points:
            self.sound_points.play()

    def obstacle_jumped(self):
        """Joue le son associé à un obstacle sauté."""
        if self.sound_woohoo:
            self.sound_woohoo.play()

    def update_status(self, player_points):
        """Met à jour le niveau et la vitesse du jeu.

        Args:
            player_points (int): Nombre de points du joueur.
        """
        self.level = player_points // 1000 + 1
        self.speed = self.level/2 + 1

    def check_quit_event(self):
        """Vérifie si l'utilisateur a demandé à quitter le jeu.

        Returns:
            bool: True si l'événement de fermeture est détecté.
        """
        quit_event = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_event = True

        return quit_event

    def quit(self):
        """Ferme proprement pygame."""
        pygame.quit()

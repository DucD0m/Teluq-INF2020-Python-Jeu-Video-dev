"""
Module window.

Ce module définit la classe Window, responsable de la gestion
de la fenêtre du jeu, de l'affichage graphique, des écrans
principaux (démarrage, fin de partie) et du rendu des éléments
visuels (joueur, obstacles, décor et interface utilisateur).
"""
import pygame
from classes.VisualAssetManager import VisualAssetManager


class Window:
    """Gère la fenêtre principale et l'affichage du jeu.

    Cette classe centralise :
    - l'initialisation de la fenêtre graphique,
    - le chargement des images et des polices,
    - l'affichage des écrans de jeu (début, partie terminée),
    - le rendu du joueur, des obstacles et du décor,
    - l'affichage des informations de statut (niveau, vies, points).
    """

    def __init__(self, width, height):
        """Initialise la fenêtre du jeu et charge les ressources graphiques.

        Args:
            width (int): Largeur de la fenêtre en pixels.
            height (int): Hauteur de la fenêtre en pixels.
        """
        if not pygame.get_init():
            pygame.init()
        assets = VisualAssetManager()
        self.width = width
        self.height = height
        self.spacing = 50
        self.dx = self.spacing
        self.alignment = -10
        self.num_rows = self.height // self.spacing
        self.left_limit = 3 * self.spacing
        self.right_limit = self.width - 5 * self.spacing
        self.white = (255, 255, 255)
        self.snow_color = (200, 200, 255)

        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ski Alpin 2D")

        self.font_retro = assets.load_retro_font()
        self.font_snow = assets.load_snow_font()
        self.big_skier = assets.load_big_skier()
        self.big_tree = assets.load_big_tree()
        self.skier_left = assets.load_skier()
        self.skier_right = pygame.transform.flip(self.skier_left, True, False)
        self.tree = assets.load_tree()
        self.rock = assets.load_rock()

    def show_text(self, text, x, y, color, font):
        """Affiche du texte centré à l'écran.

        Args:
            text (str): Texte à afficher.
            x (int): Position horizontale du centre du texte.
            y (int): Position verticale du centre du texte.
            color (tuple[int, int, int]): Couleur RGB du texte.
            font (pygame.font.Font): Police utilisée.
        """
        text_render = font.render(text, True, color)
        text_rect = text_render.get_rect(center=(x, y))
        self.display.blit(text_render, text_rect)

    def show_start_screen(self):
        """Affiche l'écran de démarrage du jeu."""
        blue = (50, 50, 255)
        self.display.fill(blue)

        self.show_text(
            "SKI ALPIN 2D",
            self.width // 2,
            self.height // 3,
            self.white,
            self.font_snow
        )

        self.show_text(
            "Appuyer sur ENTRÉE pour débuter",
            self.width // 2,
            self.height*2 // 3,
            self.white,
            self.font_retro
        )

        self.display.blit(self.big_tree, [100, self.height // 2])
        self.display.blit(
            self.big_skier, [self.width - 300, self.height // 2])

    def show_game_over_screen(self, game_level, player_points):
        """Affiche l'écran de fin de partie.

        Args:
            game_level (int): Niveau atteint par le joueur.
            player_points (int): Score final du joueur.
        """
        red = (255, 0, 0)
        self.display.fill(red)

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
            "Appuyer sur ENTRÉE pour recommencer",
            self.width // 2,
            self.height*2.5 // 3,
            self.white,
            self.font_retro
        )

        self.display.blit(self.big_tree, [200, 200])
        self.display.blit(self.big_skier, [self.width - 400, 200])

    def update_side_limit_fillers(self, speed):
        """Met à jour le décor sur les bords de la piste.

        Args:
            speed (int): Vitesse de défilement vertical.
        """
        for i in range(-1, self.num_rows):
            x = i * self.spacing + self.dx
            self.display.blit(self.tree, [self.alignment, x])
            self.display.blit(self.tree, [self.spacing+self.alignment, x])
            self.display.blit(
                self.tree, [(2*self.spacing+self.alignment), x])
            self.display.blit(
                self.tree, [(3*self.spacing+self.alignment), x])
            self.display.blit(
                self.tree, [self.width-(4*self.spacing-self.alignment), x])
            self.display.blit(
                self.tree, [self.width-(3*self.spacing-self.alignment), x])
            self.display.blit(
                self.tree, [self.width-(2*self.spacing-self.alignment), x])
            self.display.blit(
                self.tree, [self.width-self.spacing+self.alignment, x])

        self.dx -= speed
        if self.dx <= 0:
            self.dx += self.spacing

    def update_status(self, game_level, player_lives, player_points):
        """Affiche les informations de jeu en haut de l'écran.

        Args:
            game_level (int): Niveau actuel.
            player_lives (int): Nombre de vies restantes.
            player_points (int): Nombre de points actuel.
        """
        black = (0, 0, 0)
        self.show_text(
            f"Niveau : {game_level}",
            self.width // 4,
            20,
            black,
            self.font_retro
        )
        self.show_text(
            f"Vies : {player_lives}",
            self.width // 2,
            20,
            black,
            self.font_retro
        )
        self.show_text(
            f"Points : {player_points}",
            self.width*3 // 4,
            20,
            black,
            self.font_retro
        )

    def draw(self, image, x, y):
        """Dessine une image si elle est visible à l'écran.

        Args:
            image (pygame.Surface): Image à afficher.
            x (int): Position horizontale.
            y (int): Position verticale.
        """
        image_height = image.get_height()
        visible = -image_height < y < self.height

        if visible:
            self.display.blit(image, (x, y))

    def draw_player(self, player):
        """Affiche le joueur à l'écran.

        Cette méthode gère plusieurs états visuels du joueur :
        - **Invincibilité** : lorsque le joueur est invincible, son
          affichage alterne (effet de clignotement) afin d'indiquer
          visuellement qu'il ne peut pas subir de collision.
        - **Saut** : lorsque le joueur saute, son image est transformée
          (rotation et mise à l'échelle) pour simuler le mouvement aérien.

        Attention :
            Cette méthode utilise directement l'instance de l'objet joueur,
            qui est mutable.

        Args:
            player (Player): Instance du joueur contenant son état
                visuel (position, image, angle, échelle, saut et
                invincibilité).
        """
        transformed = self.transform_player_image(
            player.image, player.angle, player.scale)
        rect = transformed.get_rect(center=(
            player.x + player.image.get_width()//2,
            player.y + player.image.get_height()//2)
        )
        draw_player = True

        if player.invincible:
            draw_player = int(player.invincible_time * 10) % 2 == 0

        if draw_player:
            if player.jumping:
                self.display.blit(transformed, rect)
            else:
                self.draw(player.image, player.x, player.y)

    def transform_player_image(
        self, player_image, player_angle, player_scale
    ):
        """Applique une rotation et un redimensionnement au joueur.

        Args:
            player_image (pygame.Surface): Image du joueur.
            player_angle (float): Angle de rotation.
            player_scale (float): Facteur d'échelle.

        Returns:
            pygame.Surface: Image transformée.
        """
        return pygame.transform.rotozoom(
            player_image, -player_angle, player_scale
        )

    def flip(self):
        """Met à jour l'affichage de la fenêtre."""
        pygame.display.flip()

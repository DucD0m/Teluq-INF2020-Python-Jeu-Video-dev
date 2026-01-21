"""
Gestionnaire de ressources visuelles pour un jeu Pygame.

Ce module fournit la classe VisualAssetManager qui est
une sous-classe de la classe AssetManager.

Classes:
    AssetManager: Fournit des utilitaires simples pour signaler les problèmes
        de chargement de fichiers (images, sons, polices, etc.)
"""
import pygame
from classes.AssetManager import AssetManager


class VisualAssetManager(AssetManager):
    """Gestionnaire de ressources visuelles pour un jeu Pygame.

    Cette classe permet de charger des polices et des images, en fournissant
    des versions de secours si les fichiers sont introuvables ou si pygame
    n'a pas de mode vidéo actif.
    """

    def __init__(self):
        """Initialise les chemins des fichiers et la police par défaut."""
        self.font_default = pygame.font.SysFont(None, 36)
        self.font_retro_path = (
            "fonts/PressStart2P-Regular/PressStart2P-Regular.ttf"
        )
        self.font_snow_path = (
            "fonts/ice-and-snow-font/IceAndsnowNormal-2ve8.ttf"
        )

        # https://www.pngmart.com/image/706730
        self.big_skier_path = "images/Skier-PNG-Photos.png"
        self.skier_path = "images/Skier-PNG-Photos-sm.png"

        # https://www.pngmart.com/image/272420
        self.big_tree_path = "images/Winter-Tree-PNG-File.png"
        self.tree_path = "images/Winter-Tree-PNG-File-sm.png"

        # https://www.pngmart.com/image/490201
        self.rock_path = "images/Stones-Transparent-Isolated-Background-sm.png"

    # Polices
    def load_retro_font(self):
        """Charge la police rétro.

        Returns:
            pygame.font.Font: La police rétro chargée ou la police par défaut
                si le fichier est manquant.
        """
        try:
            font_retro = pygame.font.Font(self.font_retro_path, 18)
        except FileNotFoundError:
            font_retro = self.font_default
            super().print_file_missing_error(self.font_retro_path)

        return font_retro

    def load_snow_font(self):
        """Charge la police 'ice and snow'.

        Returns:
            pygame.font.Font: La police chargée ou la police par défaut
                si le fichier est manquant.
        """
        try:
            font_snow = pygame.font.Font(self.font_snow_path, 216)
        except FileNotFoundError:
            font_snow = self.font_default
            super().print_file_missing_error(self.font_snow_path)

        return font_snow

    # Images
    def load_big_skier(self):
        """Charge l'image grand skieur et la redimensionne.

        Returns:
            pygame.Surface: Surface de l'image ou une surface vide
                si fichier manquant.
        """
        try:
            big_skier = pygame.transform.scale(pygame.image.load(
                self.big_skier_path), (200, 200))
        except FileNotFoundError:
            big_skier = pygame.Surface((0, 0))
            super().print_file_missing_error(self.big_skier_path)

        return big_skier

    def load_big_tree(self):
        """Charge l'image grand arbre et la redimensionne.

        Returns:
            pygame.Surface: Surface de l'image ou une surface vide
                si fichier manquant.
        """
        try:
            big_tree = pygame.transform.scale(pygame.image.load(
                self.big_tree_path), (200, 200))
        except FileNotFoundError:
            big_tree = pygame.Surface((0, 0))
            super().print_file_missing_error(self.big_tree_path)

        return big_tree

    def load_skier(self):
        """Charge l'image du skieur et la redimensionne.

        Returns:
            pygame.Surface: Surface de l'image ou un skieur dessiné si fichier
                manquant ou erreur pygame.
        """
        try:
            skier_left = pygame.transform.scale(pygame.image.load(
                self.skier_path).convert_alpha(), (100, 100))
        except FileNotFoundError:
            skier_left = self.create_fallback_skier()
            super().print_file_missing_error(self.skier_path)
        except pygame.error:
            skier_left = self.create_fallback_skier()
            self.print_video_mode_error()

        return skier_left

    def load_tree(self):
        """Charge l'image de l'arbre ou crée un arbre si fichier manquant.

        Returns:
            pygame.Surface: Surface de l'arbre.
        """
        green = (0, 100, 50)
        triangle_points = [
            (35, 0),
            (0, 70),
            (70, 70)
        ]
        try:
            tree = pygame.transform.scale(pygame.image.load(
                self.tree_path).convert_alpha(), (70, 70))
        except FileNotFoundError:
            tree = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.polygon(tree, green, triangle_points)
            super().print_file_missing_error(self.tree_path)
        except pygame.error:
            tree = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.polygon(tree, green, triangle_points)
            self.print_video_mode_error()

        return tree

    def load_rock(self):
        """Charge l'image du rocher ou crée un rocher si fichier manquant.

        Returns:
            pygame.Surface: Surface du rocher.
        """
        grey = (150, 150, 150)

        try:
            rock = pygame.transform.scale(pygame.image.load(
                self.rock_path).convert_alpha(), (90, 60))
        except FileNotFoundError:
            rock = pygame.Surface((90, 60), pygame.SRCALPHA)
            pygame.draw.ellipse(rock, grey, rock.get_rect())
            super().print_file_missing_error(self.rock_path)
        except pygame.error:
            rock = pygame.Surface((90, 60), pygame.SRCALPHA)
            pygame.draw.ellipse(rock, grey, rock.get_rect())
            self.print_video_mode_error()

        return rock

    def print_video_mode_error(self):
        """Affiche un message d'erreur s'il n'y pas de mode vidéo actif."""
        print(
            "No video mode has been set: convert_alpha() "
            "doit être appelé après pygame.display.set_mode()"
        )

    def create_fallback_skier(self):
        """Crée un skieur stylisé dessiné avec des primitives Pygame.

        Returns:
            pygame.Surface: Surface représentant un skieur avec transparence.
        """
        size = (100, 100)
        surface = pygame.Surface(size, pygame.SRCALPHA)
        w, h = size

        # Couleurs
        skier_red = (220, 40, 30)
        skier_grey = (50, 60, 70)
        skier_black = (20, 20, 20)
        skier_white = (230, 240, 255)
        skier_blue = (80, 180, 255)

        # Surface skis
        skis = pygame.Surface((50, 100), pygame.SRCALPHA)

        # Skis (avant rotation)
        pygame.draw.rect(skis, skier_blue, (6, 45, 8, 40), border_radius=4)
        pygame.draw.rect(skis, skier_blue, (16, 45, 8, 40), border_radius=4)

        # Rotation vers la gauche (négatif = gauche)
        skis_rotated = pygame.transform.rotate(skis, -40)

        # Position des skis
        skis_rect = skis_rotated.get_rect(center=(w // 2, h - 30))
        surface.blit(skis_rotated, skis_rect)

        # Corps
        pygame.draw.ellipse(surface, skier_red, (15, 25, 35, 40))

        # Bras
        pygame.draw.ellipse(surface, skier_red, (5, 35, 15, 20))
        pygame.draw.ellipse(surface, skier_red, (45, 35, 15, 20))

        # Jambes
        pygame.draw.rect(
            surface, skier_grey, (22, h - 45, 10, 18), border_radius=4)
        pygame.draw.rect(
            surface, skier_grey, (34, h - 45, 10, 18), border_radius=4)

        # Tête / casque
        pygame.draw.circle(surface, skier_black, (32, 18), 12)

        # Lunettes
        pygame.draw.ellipse(surface, skier_white, (24, 14, 16, 8))

        return surface

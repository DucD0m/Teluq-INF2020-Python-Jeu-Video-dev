"""
Module obstacle.

Ce module définit la classe Obstacle, utilisée pour représenter les obstacles
du jeu (rochers ou arbres). Un obstacle possède une position, une image,
une rectangle de collision et une logique de déplacement vertical.

Les obstacles apparaissent aléatoirement en bas de l'écran et se déplacent
vers le haut à une vitesse donnée.
"""
import random


class Obstacle:
    """Représente un obstacle du jeu (arbre ou rocher).

    Un obstacle peut être soit franchissable (saut possible),
    soit bloquant. Il se déplace verticalement vers le haut
    et réapparaît en bas de l'écran lorsqu'il sort de la zone visible.

    Attributes:
        image (pygame.Surface): Image représentant l'obstacle.
        x (int): Position horizontale de l'obstacle.
        y (int): Position verticale de l'obstacle.
        rect (pygame.Rect): Rectangle de collision.
        cleared (bool): Indique si l'obstacle a déjà été franchi.
        jump_allowed (bool): Indique si l'obstacle peut être sauté.
    """

    def __init__(self, height, left_limit, right_limit, image, jump_allowed):
        """Initialise un obstacle.

        Args:
            height (int): Hauteur de la fenêtre de jeu.
            left_limit (int): Limite horizontale gauche autorisée.
            right_limit (int): Limite horizontale droite autorisée.
            image (pygame.Surface): Image associée à l'obstacle.
            jump_allowed (bool): Indique si le joueur peut sauter
                par-dessus cet obstacle.
        """
        self.image = image
        self.y = height + random.randint(0, height)
        self.x = random.randint(left_limit + 50, right_limit - 50)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.width = self.image.get_width() - 20
        self.rect.height = self.image.get_height() - 20
        self.cleared = False
        self.jump_allowed = jump_allowed

    def update_rect(self):
        """Met à jour la position du rectangle de collision de l'obstacle.

        Le rectangle est volontairement réduite et décalée afin de
        rendre les collisions plus naturelles visuellement.
        """
        self.rect.topleft = (self.x + 10, self.y + 10)

    def set_cleared(self):
        """Marque l'obstacle comme franchi par le joueur."""
        self.cleared = True

    def update_position(self, height, left_limit, right_limit, speed):
        """Met à jour la position de l'obstacle.

        L'obstacle se déplace vers le haut. Lorsqu'il sort de l'écran,
        il est repositionné en bas avec une position horizontale aléatoire.

        Args:
            height (int): Hauteur de la fenêtre de jeu.
            left_limit (int): Limite horizontale gauche autorisée.
            right_limit (int): Limite horizontale droite autorisée.
            speed (int): Vitesse de déplacement vertical.
        """
        self.y -= speed
        if self.y < -self.image.get_height():
            self.cleared = False
            self.y = height + random.randint(0, height)
            self.x = random.randint(left_limit + 50, right_limit - 50)

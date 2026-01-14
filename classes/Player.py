"""
Module définissant la classe Player.

Ce module contient la classe Player, qui représente le joueur principal
du jeu de ski. Elle gère :
- les déplacements horizontaux et verticaux,
- le saut avec animation (rotation et mise à l'échelle),
- l'invincibilité temporaire après une collision,
- le système de vies et de points.

La classe ne dépend pas directement de pygame pour la gestion des entrées,
ce qui facilite la séparation de la logique de jeu.
"""


class Player:
    """Représente le joueur contrôlé par l'utilisateur."""

    def __init__(self, window_width, image_left, image_right):
        """Initialise le joueur et ses états de départ.

        Args:
            window_width (int): Largeur de la fenêtre de jeu.
            image_left (Surface): Image du joueur orientée vers la gauche.
            image_right (Surface): Image du joueur orientée vers la droite.
        """
        self.image_left = image_left
        self.image_right = image_right
        self.image = self.image_left

        self.starting_x = window_width // 2 - self.image.get_width() // 2
        self.starting_y = self.image.get_height() + 20
        self.x = self.starting_x
        self.y = self.starting_y

        # Rectangle légèrement réduit pour des collisions plus permissives
        self.rect = self.image.get_rect(topleft=(self.x + 10, self.y + 10))
        self.rect.width -= 20
        self.rect.height -= 20

        self.speed = 5
        self.dx = 0
        self.mx = 0  # Dernière direction horizontale

        self.starting_lives = 3
        self.lives = self.starting_lives
        self.points = 0

        # Gestion de l'invincibilité temporaire
        self.invincible = False
        self.invincible_time = 0.0
        self.invincible_duration = 3.0

        # Blocage temporaire du gain de points
        self.stop_points = False
        self.stop_points_time = 0.0
        self.stop_points_duration = 3.0

        # Gestion du saut
        self.jumping = False
        self.jump_time = 0.0
        self.jump_duration = 1.5
        self.jump_x = self.x
        self.angle = 0.0
        self.scale = 1.0

    def input(self, keys, height, left_limit, right_limit):
        """Traite les entrées utilisateur et applique les déplacements.

        # pragma: no cover signifie que les lignes associées ne sont
        pas calculées dans le calcul de couverture des tests unittest.

        Args:
            keys (dict): Dictionnaire des touches actives.
            height (int): Hauteur de la fenêtre.
            left_limit (int): Limite horizontale gauche.
            right_limit (int): Limite horizontale droite.
        """
        self.horizontal_move(keys)  # pragma: no cover
        self.vertical_move(keys)  # pragma: no cover
        self.jump_move(keys)  # pragma: no cover
        self.position_limits(
            height, left_limit, right_limit)  # pragma: no cover

    def horizontal_move(self, keys):
        """Gère le déplacement horizontal du joueur."""
        if not self.jumping:
            if keys["left"]:
                self.dx = -self.speed
                self.mx = -self.speed
                self.image = self.image_left
            elif keys["right"]:
                self.dx = self.speed
                self.mx = self.speed
                self.image = self.image_right
            else:
                self.dx = self.mx
        else:
            self.dx = 0

        self.x += self.dx

    def vertical_move(self, keys):
        """Gère le déplacement vertical du joueur."""
        if keys["up"]:
            self.y -= self.speed
        if keys["down"]:
            self.y += self.speed

    def jump_move(self, keys):
        """Déclenche un saut si la touche espace est pressée."""
        if keys["space"] and not self.jumping:
            self.jumping = True
            self.jump_time = 0.0
            self.jump_x = self.x

    def position_limits(self, height, left_limit, right_limit):
        """Empêche le joueur de sortir de la zone jouable."""
        self.x = max(left_limit, min(self.x, right_limit))
        self.y = max(0, min(self.y, height - self.image.get_height()))

    def update(self, dt):
        """Met à jour l'état du joueur.

        Args:
            dt (float): Temps écoulé depuis la dernière frame (en secondes).
        """
        self.update_rect()
        self.update_invincibility(dt)
        self.update_stop_points(dt)
        self.update_jump(dt)

    def update_rect(self):
        """Met à jour le rectangle de collision du joueur."""
        self.rect.topleft = (self.x + 10, self.y + 10)

    def update_invincibility(self, dt):
        """Met à jour les paramètres d'invincibilité."""
        if self.invincible:
            self.invincible_time += dt
            if self.invincible_time >= self.invincible_duration:
                self.invincible = False

    def update_stop_points(self, dt):
        """Met à jour le blocage temporaire des points."""
        if self.stop_points:
            self.stop_points_time += dt
            if self.stop_points_time >= self.stop_points_duration:
                self.stop_points = False

    def update_jump(self, dt):
        """Anime le saut du joueur.

        Le saut est divisé en deux phases :
        - première moitié : agrandissement et rotation (0° → 180°),
        - deuxième moitié : rétrécissement et rotation (180° → 360°),
          puis remise à l'état normal.
        """
        if self.jumping:
            self.jump_time += dt
            t = self.jump_time / self.jump_duration
            if t >= 1.0:
                t = 1.0
                self.jumping = False
                self.angle = 0.0
                self.scale = 1.0
            else:
                if t < 0.5:
                    self.scale = 1.0 + t * 2
                    self.angle = t * 360
                else:
                    self.scale = 2.0 - (t - 0.5) * 2
                    self.angle = (t - 0.5) * 360 + 180

    def add_points(self, p, dp):
        """Ajoute des points au total actuel.

        Cette fonction est une démonstration de fonction pure
        en programmation fonctionnelle pour répondre aux exigences
        du 2e travail noté du cours INF2020 de l'Université Téluq.

        Args:
            p (int): Nombre de points actuels.
            dp (int): Nombre de points à ajouter.

        Returns:
            int: La somme des points actuels et des points à être ajoutés.
        """
        return p + dp

    def obstacle_cleared(self):
        """Ajoute des points lorsqu'un obstacle est évité."""
        self.points = self.add_points(self.points, 25)

    def obstacle_jumped(self):
        """Ajoute des points lorsqu'un obstacle est sauté."""
        self.points += 100
        self.stop_points = True
        self.stop_points_time = 0.0

    def obstacle_hit(self):
        """Réduit une vie et active l'invincibilité temporaire."""
        self.lives -= 1
        self.invincible = True
        self.invincible_time = 0.0

    def reset(self):
        """Réinitialise le joueur à son état initial."""
        self.lives = self.starting_lives
        self.points = 0
        self.x = self.starting_x
        self.y = self.starting_y
        self.invincible = True
        self.invincible_time = 0.0

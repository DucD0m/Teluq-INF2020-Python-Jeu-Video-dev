"""
Ce fichier contient des exemples de programmation fonctionnelle.

Les fonctions servent à répondre aux exigences du 2e travail noté
du cours INF2020 de l'Université Téluq.
"""


def add_points(p, dp):
    """Ajoute des points à un total existant.

    Démonstration d'une fonction pure en programmation fonctionnelle.

    Args:
        p (int): Total de points actuel.
        dp (int): Points à ajouter.

    Returns:
        int: Nouveau total de points.
    """
    return p + dp


def side_obstacles_positions(spacing, alignment, width, rows, dx, nb):
    """Calcule les positions (x, y) des obstacles décoratifs de bordure.

    Génère une liste de coordonnées pour les obstacles situés à gauche
    et à droite de la piste, répartis sur plusieurs rangées.
    Fonction déclarative et fonctionnelle.

    Args:
        spacing (int): Espacement horizontal et vertical entre obstacles.
        alignment (int): Décalage horizontal pour masquer partiellement
            les images.
        width (int): Largeur de la fenêtre de jeu en pixels.
        rows (int): Nombre de rangées d'obstacles.
        dx (int): Décalage vertical pour simuler le défilement.
        nb (int): Le nombre d'obstacles de chaque côté de la fenêtre.

    Returns:
        list[tuple[int, int]]: Liste des coordonnées (x, y) des obstacles.
    """
    # Positions horizontales (X) gauche et droite
    left_x = [alignment + i * spacing for i in range(nb)]
    right_x = [width - (nb - i) * spacing + alignment for i in range(nb)]
    x_positions = left_x + right_x

    # Positions verticales (Y) pour chaque ligne
    y_positions = [row * spacing + dx for row in range(-2, rows)]

    # Combinaison X, Y en tuples (x, y) - Liste en compréhension.
    positions = [(x, y) for y in y_positions for x in x_positions]

    return positions

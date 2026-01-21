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


def side_obstacles_positions(spacing, alignment, width, rows, dx):
    """Calcule les positions (x, y) des obstacles décoratifs de bordure.

    Génère une liste de coordonnées pour les obstacles situés à gauche
    et à droite de la piste, répartis sur plusieurs rangées.
    Fonction déclarative et purement fonctionnelle.

    Args:
        spacing (int): Espacement horizontal et vertical entre obstacles.
        alignment (int): Décalage horizontal pour masquer partiellement
            les images.
        width (int): Largeur de la fenêtre de jeu en pixels.
        rows (int): Nombre de rangées d'obstacles.
        dx (int): Décalage vertical pour simuler le défilement.

    Returns:
        list[tuple[int, int]]: Liste des coordonnées (x, y) des obstacles.
    """
    # Positions horizontales (X) gauche et droite
    left_x = [alignment + i * spacing for i in range(4)]
    right_x = [width - (4 - i) * spacing + alignment for i in range(4)]
    x_positions = left_x + right_x

    # Positions verticales (Y) pour chaque ligne
    y_positions = [row * spacing + dx for row in range(-1, rows)]

    # Combinaison X, Y en tuples (x, y)
    positions = sum(
        map(lambda y: list(map(lambda x: (x, y), x_positions)), y_positions),
        []
    )

    return positions

2e Travail du cours INF2020 de l'Université Téluq. Il s'agit d'un jeu de Ski Alpin en animation 2D programmé en Python avec le module Pygame. Le jeu est de style arcade et est inspiré des différents jeu de ski alpin produits sur la plateforme VIC-20 dans les années 80. Le package uv est utilisé pour la gestion des dépendances. La version de python requise est 3.12.4 (uv python pin 3.12.4).

Commandes de jeu:
- Déplacements avec les touches flèches du clavier.
- Barre ESPACE pour sauter.

Règles du jeu:
- Il est permis de sauter par dessus les roches.
- Il n'est pas permis de sauter par dessus les arbres.
- Une vie est perdue à chaque collision avec un obstacle ou les forêts en bordure.
- Un période d'invincibilité est appliquée après chaque collision.
- Aucun point n'est attribué durant la période d'invincililité.
- Un passage d'obstacle (arbre ou roche) vaut 25 points.
- Un saut par dessus une roche vaut 100 points.
- Le niveau augmente à chaque 1000 points.
- La vitesse du jeu augmente à chaque niveau.

Note:
- Les fichiers Python respectent les normes PEP8 et PEP257 pour le style et les docstrings. La vérification du style est accomplie avec l'outil Flake8 ainsi que celui trouvé à https://www.codewof.co.nz/style/python3/

import pygame, sys
from classes.Player import Player
from classes.Obstacle import Obstacle

pygame.init()
font = pygame.font.SysFont(None, 36)

LARGEUR_FENETRE = 1400
HAUTEUR_FENETRE = 750
fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))
pygame.display.set_caption("Exemple de jeu 2D avec pygame")
horloge = pygame.time.Clock()

NEIGE = (200, 200, 255)
RED = (250, 0, 0)

level = 1

tree_size = 70
tree = pygame.transform.scale(pygame.image.load("images/Winter-Tree-PNG-File-sm.png"), (tree_size, tree_size))
spacing = 50
px = HAUTEUR_FENETRE
vitesse = 2
num_rows = HAUTEUR_FENETRE // int(spacing/2) + 2
alignment = -(int(tree_size/6))

# Limites horizontales
left_limit = 4 * spacing - 50
right_limit = LARGEUR_FENETRE - 4 * spacing - 50

# Créer le joueur
player = Player(LARGEUR_FENETRE, right_limit, left_limit)

#Obstacles
num_rocks = 2
rocks = []
for i in range(num_rocks):
    obs = Obstacle(
        90,
        60,
        LARGEUR_FENETRE,
        HAUTEUR_FENETRE + i * 100 * vitesse - 100,
        spacing,
        "images/Stones-Transparent-Isolated-Background-sm.png"
    )
    rocks.append(obs)

num_trees = 3
trees = []
for i in range(num_trees):
    obs = Obstacle(
        70,
        70,
        LARGEUR_FENETRE,
        HAUTEUR_FENETRE + i * 50 * vitesse,
        spacing,
        "images/Winter-Tree-PNG-File-sm.png"
    )
    trees.append(obs)

# Boucle de jeu
fin = False
while not fin:
    dt = horloge.get_time() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fin = True

    keys = pygame.key.get_pressed()

    if player.lives == 0:
        fenetre.fill(RED)

        text = font.render("LA PARTIE EST TERMINÉE", True, (0, 0, 0))
        text_rect = text.get_rect(center=(
            LARGEUR_FENETRE // 2,
            HAUTEUR_FENETRE // 4
        ))
        fenetre.blit(text, text_rect)

        text = font.render(f"Niveau : {level}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(
            LARGEUR_FENETRE // 2,
            HAUTEUR_FENETRE // 2 - 25
        ))
        fenetre.blit(text, text_rect)

        text = font.render(f"Points : {player.points}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(
            LARGEUR_FENETRE // 2,
            HAUTEUR_FENETRE // 2 + 25
        ))
        fenetre.blit(text, text_rect)

        text = font.render("APPUYEZ SUR RETOUR POUR RECOMMENCER", True, (0, 0, 0))
        text_rect = text.get_rect(center=(
            LARGEUR_FENETRE // 2,
            HAUTEUR_FENETRE*2 // 3
        ))
        fenetre.blit(text, text_rect)

        if keys[pygame.K_RETURN]:
            level = 1
            player.reset()
            player.update(dt)

        pygame.display.flip()
        horloge.tick(60)
        continue

    level = player.points // 1000 + 1
    vitesse = level + 1

    player.handle_input(keys)
    player.update(dt)

    fenetre.fill(NEIGE)

    # Collision et passages
    for obs in rocks:
        obs.update_rect()
        player.check_collision(obs.rect, True)

    for obs in trees:
        obs.update_rect()
        player.check_collision(obs.rect, False)
        player.check_cleared(obs)

    # Dessin du joueur (clignotement si invincible)
    player.draw(fenetre)

    # Affichage d'obstacles
    for i, obs in enumerate(rocks):
        obs.draw(fenetre, HAUTEUR_FENETRE + i * 100 * vitesse -100, vitesse)

    for i, obs in enumerate(trees):
        obs.draw(fenetre, HAUTEUR_FENETRE + i * 50 * vitesse, vitesse)

    # Arbres
    for i in range(num_rows):
        x = i * spacing + px - HAUTEUR_FENETRE
        if x + spacing < 0 or x > HAUTEUR_FENETRE:
            continue
        fenetre.blit(tree,[alignment,x])
        fenetre.blit(tree,[spacing+alignment,x])
        fenetre.blit(tree,[(2*spacing+alignment),x])
        fenetre.blit(tree,[(3*spacing+alignment),x])
        fenetre.blit(tree,[LARGEUR_FENETRE-(4*spacing-alignment),x])
        fenetre.blit(tree,[LARGEUR_FENETRE-(3*spacing-alignment),x])
        fenetre.blit(tree,[LARGEUR_FENETRE-(2*spacing-alignment),x])
        fenetre.blit(tree,[LARGEUR_FENETRE-spacing+alignment,x])
    px -= vitesse
    if px <= 0:
        px += spacing * 2

    # Statut du jeu
    level_text = font.render(f"Niveau : {level}", True, (0, 0, 0))
    lives_text = font.render(f"Vies : {player.lives}", True, (0, 0, 0))
    points_text = font.render(f"Points : {player.points}", True, (0, 0, 0))
    fenetre.blit(level_text, (400, 20))
    fenetre.blit(lives_text, (600, 20))
    fenetre.blit(points_text, (800, 20))


    pygame.display.flip()
    horloge.tick(60)

pygame.quit()

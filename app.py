import pygame, sys
from classes.Game import Game
from classes.Player import Player
from classes.Obstacle import Obstacle

game = Game(1400, 750)

tree_size = 70
tree = pygame.transform.scale(pygame.image.load("images/Winter-Tree-PNG-File-sm.png"), (tree_size, tree_size))
spacing = 50
px = game.height
vitesse = 2
num_rows = game.height // int(spacing/2) + 2
alignment = -(int(tree_size/6))

# Limites horizontales
left_limit = 4 * spacing - 50
right_limit = game.width - 4 * spacing - 50

# Créer le joueur
player = Player(game.width, right_limit, left_limit)

#Obstacles
num_rocks = 2
rocks = []
for i in range(num_rocks):
    obs = Obstacle(
        90,
        60,
        game.width,
        game.height + i * 100 * vitesse - 100,
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
        game.width,
        game.height + i * 50 * vitesse,
        spacing,
        "images/Winter-Tree-PNG-File-sm.png"
    )
    trees.append(obs)

# Boucle de jeu
fin = False
while not fin:
    dt = game.clock.get_time() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fin = True

    keys = pygame.key.get_pressed()

    if player.lives == 0:
        game.window.fill(game.game_over_color)

        text = game.font.render("LA PARTIE EST TERMINÉE", True, (0, 0, 0))
        text_rect = text.get_rect(center=(
            game.width // 2,
            game.height // 4
        ))
        game.window.blit(text, text_rect)

        text = game.font.render(f"Niveau : {game.level}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(
            game.width // 2,
            game.height // 2 - 25
        ))
        game.window.blit(text, text_rect)

        text = game.font.render(f"Points : {player.points}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(
            game.width // 2,
            game.height // 2 + 25
        ))
        game.window.blit(text, text_rect)

        text = game.font.render("APPUYEZ SUR RETOUR POUR RECOMMENCER", True, (0, 0, 0))
        text_rect = text.get_rect(center=(
            game.width // 2,
            game.height*2 // 3
        ))
        game.window.blit(text, text_rect)

        if keys[pygame.K_RETURN]:
            game.level = 1
            player.reset()
            player.update(dt)

        pygame.display.flip()
        game.clock.tick(60)
        continue

    game.level = player.points // 1000 + 1
    vitesse = game.level + 1

    player.handle_input(keys)
    player.update(dt)

    game.window.fill(game.snow_color)

    # Collision et passages
    for obs in rocks:
        obs.update_rect()
        player.check_collision(obs.rect, True)

    for obs in trees:
        obs.update_rect()
        player.check_collision(obs.rect, False)
        player.check_cleared(obs)

    # Dessin du joueur (clignotement si invincible)
    player.draw(game.window)

    # Affichage d'obstacles
    for i, obs in enumerate(rocks):
        obs.draw(game.window, game.height + i * 100 * vitesse -100, vitesse)

    for i, obs in enumerate(trees):
        obs.draw(game.window, game.height + i * 50 * vitesse, vitesse)

    # Arbres
    for i in range(num_rows):
        x = i * spacing + px - game.height
        if x + spacing < 0 or x > game.height:
            continue
        game.window.blit(tree,[alignment,x])
        game.window.blit(tree,[spacing+alignment,x])
        game.window.blit(tree,[(2*spacing+alignment),x])
        game.window.blit(tree,[(3*spacing+alignment),x])
        game.window.blit(tree,[game.width-(4*spacing-alignment),x])
        game.window.blit(tree,[game.width-(3*spacing-alignment),x])
        game.window.blit(tree,[game.width-(2*spacing-alignment),x])
        game.window.blit(tree,[game.width-spacing+alignment,x])
    px -= vitesse
    if px <= 0:
        px += spacing * 2

    # Statut du jeu
    game.level_text =game.font.render(f"Niveau : {game.level}", True, (0, 0, 0))
    lives_text =game.font.render(f"Vies : {player.lives}", True, (0, 0, 0))
    points_text =game.font.render(f"Points : {player.points}", True, (0, 0, 0))
    game.window.blit(game.level_text, (400, 20))
    game.window.blit(lives_text, (600, 20))
    game.window.blit(points_text, (800, 20))


    pygame.display.flip()
    game.clock.tick(60)

pygame.quit()

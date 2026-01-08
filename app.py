from classes.Game import Game
from classes.Player import Player
from classes.Obstacle import Obstacle

# Initialiser de la partie
game = Game(1400, 750)

# Créer le joueur
player = Player(game.width, game.height, game.right_limit, game.left_limit)

#Obstacles
num_rocks = 2
rocks = []
for i in range(num_rocks):
    obs = Obstacle(
        game.width,
        game.height + i * 100 * game.speed - 100,
        game.spacing,
        game.rock
    )
    rocks.append(obs)

num_trees = 3
trees = []
for i in range(num_trees):
    obs = Obstacle(
        game.width,
        game.height + i * 50 * game.speed,
        game.spacing,
        game.tree
    )
    trees.append(obs)

# Boucle de jeu
quit = False
while not quit:

    dt = game.clock.get_time() / 1000

    quit = game.check_quit_event()

    game.update_key_pressed()

    if not game.started:
        game.show_start_screen()

    elif player.lives == 0:
        game.show_game_over_screen(player, dt)

    else:
        game.window.fill(game.snow_color)

        player.input(game.keys)
        player.update(dt)

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
            obs.draw(game.window, game.height + i * 100 * game.speed -100, game.speed)

        for i, obs in enumerate(trees):
            obs.draw(game.window, game.height + i * 50 * game.speed, game.speed)

        game.update_status(player)
        game.update_side_limit_fillers()

    game.flip()
    game.clock.tick(60)

game.quit()

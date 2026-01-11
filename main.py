from classes.Game import Game, Window
from classes.Player import Player
from classes.Obstacle import Obstacle

def main():
    # Initialiser de la partie
    game = Game()
    window = Window(1400, 750)
    player = Player(window.width)

    #Obstacles
    num_rocks = 2
    rocks = []
    for i in range(num_rocks):
        obs = Obstacle(
            window.width,
            window.height + i * 100 * game.speed - 100,
            window.spacing,
            window.rock,
            True
        )
        rocks.append(obs)

    num_trees = 3
    trees = []
    for i in range(num_trees):
        obs = Obstacle(
            window.width,
            window.height + i * 50 * game.speed,
            window.spacing,
            window.tree,
            False
        )
        trees.append(obs)

    # Boucle de jeu
    quit = False
    while not quit:
        dt = game.clock.get_time() / 1000

        if (quit := game.check_quit_event()):
            continue

        game.update_key_pressed()

        if not game.started:
            window.show_start_screen()
            game.check_game_started()

        elif player.lives == 0:
            window.show_game_over_screen(game, player)
            if (restart := game.check_restart_game()):
                player.reset()
                player.update(dt)

        else:
            window.display.fill(window.snow_color)

            player.input(game.keys, window)
            player.update(dt)

            # Collision et passages
            for obs in rocks:
                obs.update_rect()
                game.check_collision(window, player, obs)

            for obs in trees:
                obs.update_rect()
                game.check_collision(window, player, obs)
                if(cleared := game.check_obstacle_cleared(player, obs)):
                    obs.set_cleared()
                    player.add_obstacle_cleared_points()

            # Dessin du joueur (clignotement si invincible)
            player.draw(window.display)

            # Affichage d'obstacles
            for i, obs in enumerate(rocks):
                obs.draw(window.display, window.height + i * 100 * game.speed -100, game.speed)

            for i, obs in enumerate(trees):
                obs.draw(window.display, window.height + i * 50 * game.speed, game.speed)

            game.update_game_status(player)
            window.update_window_status(game, player)
            window.update_side_limit_fillers(game.speed)

        game.flip()
        game.clock.tick(60)

    game.quit()

if __name__ == '__main__':
    main()

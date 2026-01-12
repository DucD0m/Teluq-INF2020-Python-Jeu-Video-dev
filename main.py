import random
from classes.Game import Game
from classes.Window import Window
from classes.Player import Player
from classes.Obstacle import Obstacle


def main():
    # Initialiser de la partie
    game = Game()
    window = Window(1400, 750)
    player = Player(window.width)

    #Obstacles
    obstacles = []
    rocks = 2
    for i in range(rocks):
        obs = Obstacle(
            window.width,
            window.height + random.randint(0,window.height),
            window.spacing,
            window.rock,
            True
        )
        obstacles.append(obs)

    trees = 3
    for i in range(trees):
        obs = Obstacle(
            window.width,
            window.height + random.randint(0,window.height),
            window.spacing,
            window.tree,
            False
        )
        obstacles.append(obs)

    # Boucle de jeu
    quit = False
    while not quit:
        dt = game.clock.get_time() / 1000

        if (quit := game.check_quit_event()):
            continue

        game.update_status(player)
        game.update_key_pressed()

        if not game.started:
            window.show_start_screen()
            game.game_started()

        elif player.lives == 0:
            window.show_game_over_screen(game, player)
            if (restart := game.restart_game()):
                player.reset()
                player.update(dt)

        else:
            window.display.fill(window.snow_color)

            player.input(game.keys, window)
            player.update(dt)

            for obs in obstacles:
                obs.update_rect()
                collision = game.check_collision(window, player, obs)

                if collision == "jumped":
                    player.obstacle_jumped()
                    game.obstacle_jumped()

                elif collision == "hit":
                    player.obstacle_hit()
                    game.obstacle_hit(player.lives)

                if(cleared := game.check_obstacle_cleared(player, obs)):
                    obs.set_cleared()
                    if not player.invincible:
                        player.obstacle_cleared()
                        game.obstacle_cleared()

                obs.draw(window.display, window.height + random.randint(0,window.height), game.speed)

            # Dessin du joueur (clignotement si invincible)
            player.draw(window.display)
            window.update_status(game, player)
            window.update_side_limit_fillers(game.speed)

        game.flip()
        game.clock.tick(60)

    game.quit()

if __name__ == '__main__':
    main()

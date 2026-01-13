from classes.Game import Game
from classes.Window import Window
from classes.Player import Player
from classes.Obstacle import Obstacle


def main():
    game = Game()
    window = Window(1400, 750)
    player = Player(
        window.width,
        window.skier_left,
        window.skier_right
    )

    obstacles = []
    rocks = 3
    trees = 4

    for i in range(rocks):
        obs = Obstacle(
            window.height,
            window.left_limit,
            window.right_limit,
            window.rock,
            True
        )
        obstacles.append(obs)

    for i in range(trees):
        obs = Obstacle(
            window.height,
            window.left_limit,
            window.right_limit,
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

        game.update_status(player.points)
        game.update_key_pressed()

        if not game.started:
            window.show_start_screen()
            game.game_started()

        elif player.lives == 0:
            window.show_game_over_screen(game.level, player.points)
            if (restart := game.restart_game()):
                player.reset()
                player.update(dt)

        else:
            window.display.fill(window.snow_color)
            player.input(
                game.keys,
                window.height,
                window.left_limit,
                window.right_limit
            )
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

                if(cleared := game.check_obstacle_cleared(
                    player.y,
                    obs.y,
                    obs.cleared
                )):
                    obs.set_cleared()
                    if not player.invincible:
                        player.obstacle_cleared()
                        game.obstacle_cleared()

                obs.update_position(
                    window.height,
                    window.left_limit,
                    window.right_limit,
                    game.speed
                )
                window.draw(obs.image, obs.x, obs.y)

            window.draw_player(player)
            window.update_status(game.level, player.lives, player.points)
            window.update_side_limit_fillers(game.speed)

        game.flip()
        game.clock.tick(60)

    game.quit()

if __name__ == '__main__':
    main()

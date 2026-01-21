"""
Module principal pour le jeu Ski Alpin 2D.

Ce module initialise le jeu, la fenêtre, le joueur et les obstacles, puis
exécute la boucle principale du jeu qui gère :
    - La gestion des entrées et des événements de sortie
    - La mise à jour de l'état du jeu et du joueur
    - La détection de collision et la gestion des obstacles
    - L'affichage du joueur, des obstacles et de l'interface
    - Le contrôle du nombre d'images par seconde (60 FPS)

Classes:
    Game : Gestion de l'état du jeu, des entrées, des collisions,
        des sons, de la musique et du temps.
    Window : Gestion du rendu à l'écran.
    Player : Représente le joueur avec ses mouvements,
        sa logique de saut et ses points.
    Obstacle : Représente les rochers et arbres que le joueur rencontre.
"""
from classes.Game import Game
from classes.Window import Window
from classes.Player import Player
from classes.Obstacle import Obstacle


def main():
    """Initialise et lance la boucle principale du jeu.

    Cette fonction crée les objets du jeu (Game, Window, Player, Obstacle),
    puis entre dans la boucle principale.

    La boucle se termine lorsque l'utilisateur quitte ou que le joueur n'a plus
    de vies.
    """
    width = 1400
    height = 750
    obstacles = []
    rocks = 3
    trees = 4

    game = Game()
    window = Window(width, height)
    player = Player(
        window.width,
        window.skier_left,
        window.skier_right
    )

    # Création des rochers
    for i in range(rocks):
        obs = Obstacle(
            window.height,
            window.left_limit,
            window.right_limit,
            window.rock,
            True
        )
        obstacles.append(obs)

    # Création des arbres
    for i in range(trees):
        obs = Obstacle(
            window.height,
            window.left_limit,
            window.right_limit,
            window.tree,
            False
        )
        obstacles.append(obs)

    # Boucle principale du jeu
    quit = False
    while not quit:
        dt = game.clock.get_time() / 1000  # Temps écoulé en secondes

        if (quit := game.check_quit_event()):
            continue

        game.update_status(player.points)
        game.update_key_pressed()

        if not game.started:
            window.show_start_screen()
            game.game_started()

        elif player.lives == 0:
            window.show_game_over_screen(game.level, player.points)
            if game.restart_game():
                player.reset()
                player.update(dt)

        else:
            window.display.fill(window.snow_color)

            # Mettre à jour le joueur selon les entrées et sa position
            player.input(
                game.keys,
                window.height,
                window.left_limit,
                window.right_limit
            )
            player.update(dt)

            # Mettre à jour les obstacles
            for obs in obstacles:
                obs.update_rect()
                collision = game.check_collision(window, player, obs)

                if collision == "jumped":
                    player.obstacle_jumped()
                    game.obstacle_jumped()

                elif collision == "hit":
                    player.obstacle_hit()
                    game.obstacle_hit(player.lives)

                if game.check_obstacle_cleared(
                    player.y,
                    obs.y,
                    obs.cleared
                ):
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

            # Affichage du joueur, de l'état de la partie
            # et des arbres en bordure de fenêtre
            window.draw_player(player)
            window.update_status(game.level, player.lives, player.points)
            window.update_side_limit_obstacles(game.speed)

        # Mise à jour de l'affichage et contrôle du framerate
        window.flip()
        game.clock.tick(60)

    game.quit()


if __name__ == '__main__':
    main()

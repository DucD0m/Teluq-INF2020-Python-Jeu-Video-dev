import unittest
import pygame
from collections import defaultdict
from unittest.mock import Mock, patch
from classes.Game import Game


class TestGame(unittest.TestCase):
    """Tests unitaires pour la classe Game."""

    # ---------- SETUP ----------

    @patch("pygame.mixer")
    @patch("pygame.time.Clock")
    @patch("pygame.get_init", return_value=True)
    def setUp(self, mock_get_init, mock_clock, mock_mixer):
        """Initialisation des mocks et création d'une instance de Game."""
        # Mock audio system
        mock_mixer.Sound.return_value = Mock()
        mock_mixer.music = Mock()

        self.game = Game()

    # ---------- INIT ----------

    def test_initial_state(self):
        """Vérifie l'état initial du jeu."""
        self.assertFalse(self.game.started)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.speed, 2)

    # ---------- GAME START ----------

    @patch("pygame.mixer.music.play")
    def test_game_started_true(self, mock_play):
        """Test le démarrage du jeu avec Entrée pressée."""
        self.game.keys = {"return": True}
        self.game.game_started()
        self.assertTrue(self.game.started)
        mock_play.assert_called_once_with(-1)

    def test_game_started_false(self):
        """Test que le jeu ne démarre pas si Entrée n'est pas pressée."""
        self.game.keys = {"return": False}
        self.game.game_started()
        self.assertFalse(self.game.started)

    # ---------- RESTART ----------

    @patch("pygame.mixer.music.unpause")
    def test_restart_game_true(self, mock_unpause):
        """Test le redémarrage du jeu avec Entrée pressée."""
        self.game.keys = {"return": True}
        result = self.game.restart_game()
        self.assertTrue(result)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.speed, 2)
        mock_unpause.assert_called_once()

    def test_restart_game_false(self):
        """Test que le jeu ne redémarre pas si Entrée n'est pas pressée."""
        self.game.keys = {"return": False}
        self.assertFalse(self.game.restart_game())

    # ---------- KEY INPUT ----------

    @patch("pygame.key.get_pressed")
    def test_update_key_pressed(self, mock_pressed):
        """Test la mise à jour de l'état des touches pressées."""
        pressed = defaultdict(bool)
        pressed[pygame.K_LEFT] = True
        pressed[pygame.K_RIGHT] = True
        pressed[pygame.K_SPACE] = True
        pressed[pygame.K_RETURN] = True

        mock_pressed.return_value = pressed
        self.game.update_key_pressed()

        self.assertTrue(self.game.keys["left"])
        self.assertTrue(self.game.keys["right"])
        self.assertTrue(self.game.keys["space"])
        self.assertTrue(self.game.keys["return"])

    # ---------- COLLISIONS ----------

    def _mock_entities(self):
        """Crée des mocks pour la fenêtre, le joueur et l'obstacle."""
        window = Mock()
        window.left_limit = 10
        window.right_limit = 100
        window.height = 600

        # Player
        player_rect = pygame.Rect(50, 100, 30, 40)
        player = Mock()
        player.rect = player_rect
        player.invincible = False
        player.jumping = False
        player.stop_points = False
        player.x = 50

        # Obstacle
        obstacle_rect = pygame.Rect(50, 100, 30, 70)
        obstacle_surface = pygame.Surface((30, 70))
        obstacle = Mock()
        obstacle.rect = obstacle_rect
        obstacle.image = obstacle_surface
        obstacle.y = obstacle_rect.y
        obstacle.jump_allowed = False

        return window, player, obstacle

    def test_collision_hit(self):
        window, player, obstacle = self._mock_entities()
        result = self.game.check_collision(window, player, obstacle)
        self.assertEqual(result, "hit")

    def test_collision_jumped(self):
        window, player, obstacle = self._mock_entities()
        player.jumping = True
        obstacle.jump_allowed = True
        result = self.game.check_collision(window, player, obstacle)
        self.assertEqual(result, "jumped")

    def test_collision_side_limit(self):
        window, player, obstacle = self._mock_entities()
        player.rect.topleft = (0, 0)
        player.x = 5  # gauche du left_limit
        result = self.game.check_collision(window, player, obstacle)
        self.assertEqual(result, "hit")

    def test_collision_obstacle_not_visible(self):
        window, player, obstacle = self._mock_entities()
        obstacle.y = 1000
        obstacle.image = pygame.Surface((30, 70))
        result = self.game.check_collision(window, player, obstacle)
        self.assertFalse(result)

    # ---------- OBSTACLE CLEARED ----------

    def test_check_obstacle_cleared_true(self):
        self.assertTrue(self.game.check_obstacle_cleared(200, 100, False))

    def test_check_obstacle_cleared_false_y(self):
        self.assertFalse(self.game.check_obstacle_cleared(50, 100, False))

    def test_check_obstacle_cleared_false_flag(self):
        self.assertFalse(self.game.check_obstacle_cleared(200, 100, True))

    # ---------- OBSTACLE EVENTS ----------

    def test_obstacle_hit_last_life(self):
        self.game.sound_killed = Mock()
        with patch("pygame.mixer.music.pause") as mock_pause:
            self.game.obstacle_hit(0)
            self.game.sound_killed.play.assert_called_once()
            mock_pause.assert_called_once()

    def test_obstacle_hit_not_last_life(self):
        self.game.sound_doh = Mock()
        self.game.obstacle_hit(2)
        self.game.sound_doh.play.assert_called_once()

    def test_obstacle_cleared(self):
        self.game.sound_points = Mock()
        self.game.obstacle_cleared()
        self.game.sound_points.play.assert_called_once()

    def test_obstacle_jumped(self):
        self.game.sound_woohoo = Mock()
        self.game.obstacle_jumped()
        self.game.sound_woohoo.play.assert_called_once()

    # ---------- STATUS ----------

    def test_update_status(self):
        self.game.update_status(2500)
        self.assertEqual(self.game.level, 3)
        self.assertEqual(self.game.speed, 4)

    # ---------- QUIT ----------

    @patch("pygame.event.get")
    def test_check_quit_event_true(self, mock_get):
        mock_get.return_value = [Mock(type=pygame.QUIT)]
        self.assertTrue(self.game.check_quit_event())

    @patch("pygame.event.get")
    def test_check_quit_event_false(self, mock_get):
        mock_get.return_value = []
        self.assertFalse(self.game.check_quit_event())

    @patch("pygame.quit")
    def test_quit(self, mock_quit):
        self.game.quit()
        mock_quit.assert_called_once()


# ---------- AUDIO EXCEPTIONS ----------

class TestGameAudioExceptions(unittest.TestCase):
    """Test la gestion des fichiers audio manquants."""

    @patch("pygame.get_init", return_value=True)
    @patch("pygame.time.Clock")
    @patch("pygame.mixer")
    @patch("classes.AssetManager.AssetManager.print_file_missing_error")
    def test_all_audio_files_missing(
        self, mock_print, mock_mixer, mock_clock, mock_get_init
    ):
        """Vérifie que les fichiers manquants sont bien traités."""
        mock_mixer.Sound.side_effect = FileNotFoundError
        mock_mixer.music.load.side_effect = pygame.error

        game = Game()

        self.assertIsNone(game.sound_killed)
        self.assertIsNone(game.sound_points)
        self.assertIsNone(game.sound_doh)
        self.assertIsNone(game.sound_woohoo)
        self.assertFalse(game.music)

        self.assertGreaterEqual(mock_print.call_count, 5)


if __name__ == "__main__":
    unittest.main()

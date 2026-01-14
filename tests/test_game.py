import unittest
import pygame
from collections import defaultdict
from unittest.mock import Mock, patch
from classes.Game import Game


class TestGame(unittest.TestCase):

    @patch("pygame.mixer")
    @patch("pygame.time.Clock")
    @patch("pygame.get_init", return_value=True)
    def setUp(self, mock_get_init, mock_clock, mock_mixer):
        # Mock audio
        mock_mixer.Sound.return_value = Mock()
        mock_mixer.music = Mock()

        self.game = Game()

    # ---------- INIT ----------

    def test_initial_state(self):
        self.assertFalse(self.game.started)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.speed, 2)

    # ---------- GAME START ----------

    @patch("pygame.mixer.music.play")
    def test_game_started_true(self, mock_play):
        self.game.keys = {"return": True}
        self.game.game_started()
        self.assertTrue(self.game.started)
        mock_play.assert_called_once_with(-1)

    def test_game_started_false(self):
        self.game.keys = {"return": False}
        self.game.game_started()
        self.assertFalse(self.game.started)

    # ---------- RESTART ----------

    @patch("pygame.mixer.music.unpause")
    def test_restart_game_true(self, mock_unpause):
        self.game.keys = {"return": True}
        result = self.game.restart_game()
        self.assertTrue(result)
        self.assertEqual(self.game.level, 1)
        mock_unpause.assert_called_once()

    def test_restart_game_false(self):
        self.game.keys = {"return": False}
        self.assertFalse(self.game.restart_game())

    # ---------- KEY INPUT ----------

    @patch("pygame.key.get_pressed")
    def test_update_key_pressed(self, mock_pressed):
        pressed = defaultdict(bool)

        pressed[pygame.K_LEFT] = True
        pressed[pygame.K_RIGHT] = True
        pressed[pygame.K_UP] = False
        pressed[pygame.K_DOWN] = False
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
        window = Mock(left_limit=10, right_limit=100)

        player = Mock()
        player.rect.colliderect.return_value = True
        player.invincible = False
        player.jumping = False
        player.stop_points = False
        player.x = 50

        obstacle = Mock()
        obstacle.rect = Mock()
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
        player.rect.colliderect.return_value = False
        player.x = 5
        result = self.game.check_collision(window, player, obstacle)
        self.assertEqual(result, "hit")

    def test_collision_none(self):
        window, player, obstacle = self._mock_entities()
        player.rect.colliderect.return_value = False
        player.invincible = True
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
        mock_get.return_value = [Mock(type=256)]
        self.assertTrue(self.game.check_quit_event())

    @patch("pygame.event.get")
    def test_check_quit_event_false(self, mock_get):
        mock_get.return_value = []
        self.assertFalse(self.game.check_quit_event())

    @patch("pygame.quit")
    def test_quit(self, mock_quit):
        self.game.quit()
        mock_quit.assert_called_once()


if __name__ == "__main__":
    unittest.main()

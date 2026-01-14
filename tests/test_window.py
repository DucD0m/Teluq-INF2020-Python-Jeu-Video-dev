import unittest
from unittest.mock import Mock, patch
import pygame

from classes.Window import Window


class TestWindow(unittest.TestCase):

    @patch("pygame.display.set_mode")
    @patch("pygame.font.Font")
    @patch("pygame.font.SysFont")
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    @patch("pygame.transform.flip")
    def setUp(
        self,
        mock_flip,
        mock_scale,
        mock_load,
        mock_sysfont,
        mock_font,
        mock_set_mode,
    ):
        self.surface = pygame.Surface((50, 50))
        mock_load.return_value = self.surface
        mock_scale.return_value = self.surface
        mock_flip.return_value = self.surface

        self.display = Mock()
        mock_set_mode.return_value = self.display

        self.window = Window(800, 600)

    # ------------------------------------------------------------------
    # INIT
    # ------------------------------------------------------------------

    @patch("pygame.get_init", return_value=False)
    @patch("pygame.init")
    @patch("pygame.display.set_mode")
    @patch("pygame.font.Font")
    @patch("pygame.font.SysFont")
    @patch("pygame.image.load")
    @patch("pygame.transform.scale")
    @patch("pygame.transform.flip")
    def test_init_calls_pygame_init(
        self,
        mock_flip,
        mock_scale,
        mock_load,
        mock_sysfont,
        mock_font,
        mock_set_mode,
        mock_init,
        _,
    ):
        Window(800, 600)
        mock_init.assert_called_once()

    # ------------------------------------------------------------------
    # SHOW TEXT
    # ------------------------------------------------------------------

    def test_show_text_calls_blit(self):
        font = Mock()
        text_surface = pygame.Surface((10, 10))
        font.render.return_value = text_surface

        self.window.show_text("Test", 100, 100, (255, 255, 255), font)

        self.display.blit.assert_called_once()

    # ------------------------------------------------------------------
    # START SCREEN
    # ------------------------------------------------------------------

    def test_show_start_screen(self):
        self.window.show_start_screen()
        self.display.fill.assert_called_once()
        self.assertTrue(self.display.blit.called)

    # ------------------------------------------------------------------
    # GAME OVER SCREEN
    # ------------------------------------------------------------------

    def test_show_game_over_screen(self):
        self.window.show_game_over_screen(3, 150)
        self.display.fill.assert_called_once()
        self.assertTrue(self.display.blit.called)

    # ------------------------------------------------------------------
    # SIDE LIMIT FILLERS
    # ------------------------------------------------------------------

    def test_update_side_limit_fillers_dx_reset(self):
        self.window.dx = 0
        self.window.update_side_limit_fillers(speed=10)
        self.assertGreater(self.window.dx, 0)

    # ------------------------------------------------------------------
    # STATUS
    # ------------------------------------------------------------------

    def test_update_status(self):
        self.window.update_status(2, 3, 100)
        self.assertTrue(self.display.blit.called)

    # ------------------------------------------------------------------
    # DRAW
    # ------------------------------------------------------------------

    def test_draw_visible(self):
        image = pygame.Surface((50, 50))
        self.window.draw(image, 10, 10)
        self.display.blit.assert_called_once()

    def test_draw_not_visible(self):
        image = pygame.Surface((50, 50))
        self.window.draw(image, 10, 1000)
        self.display.blit.assert_not_called()

    # ------------------------------------------------------------------
    # TRANSFORM PLAYER IMAGE
    # ------------------------------------------------------------------

    @patch("pygame.transform.rotozoom")
    def test_transform_player_image(self, mock_rotozoom):
        image = pygame.Surface((50, 50))
        mock_rotozoom.return_value = image

        result = self.window.transform_player_image(image, 45, 1.5)

        mock_rotozoom.assert_called_once()
        self.assertEqual(result, image)

    # ------------------------------------------------------------------
    # DRAW PLAYER
    # ------------------------------------------------------------------

    def _mock_player(self):
        player = Mock()
        player.image = pygame.Surface((50, 50))
        player.x = 100
        player.y = 200
        player.angle = 0.0
        player.scale = 1.0
        player.jumping = False
        player.invincible = False
        player.invincible_time = 0.0
        return player

    def test_draw_player_normal(self):
        player = self._mock_player()
        self.window.draw_player(player)
        self.display.blit.assert_called()

    def test_draw_player_invincible_visible(self):
        player = self._mock_player()
        player.invincible = True
        player.invincible_time = 0.2  # pair → visible

        self.window.draw_player(player)
        self.display.blit.assert_called()

    def test_draw_player_invincible_not_visible(self):
        player = self._mock_player()
        player.invincible = True
        player.invincible_time = 0.15  # impair → invisible

        self.window.draw_player(player)
        self.display.blit.assert_not_called()

    def test_draw_player_jumping(self):
        player = self._mock_player()
        player.jumping = True
        player.angle = 180
        player.scale = 1.5

        self.window.draw_player(player)
        self.display.blit.assert_called()


if __name__ == "__main__":
    unittest.main()

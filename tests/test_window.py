import unittest
from unittest.mock import patch, MagicMock
import pygame
from classes.Window import Window


class MockPlayer:
    """Classe mock pour tester draw_player."""
    def __init__(self):
        self.image = pygame.Surface((50, 50))
        self.x = 100
        self.y = 100
        self.angle = 0
        self.scale = 1
        self.invincible = False
        self.invincible_time = 0
        self.jumping = False


class TestWindowFull(unittest.TestCase):
    """Tests unitaires complets pour la classe Window."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.width = 800
        cls.height = 600

        # Patch VisualAssetManager pour éviter le chargement réel de fichiers
        patcher = patch('classes.Window.VisualAssetManager')
        cls.MockAssets = patcher.start()
        cls.addClassCleanup(patcher.stop)

        # Mock des méthodes de chargement
        mock_assets = cls.MockAssets.return_value
        mock_assets.load_retro_font.return_value = pygame.font.SysFont(None, 20)
        mock_assets.load_snow_font.return_value = pygame.font.SysFont(None, 40)
        mock_assets.load_big_skier.return_value = pygame.Surface((100, 100))
        mock_assets.load_big_tree.return_value = pygame.Surface((100, 100))
        mock_assets.load_skier.return_value = pygame.Surface((50, 50))
        mock_assets.load_tree.return_value = pygame.Surface((30, 60))
        mock_assets.load_rock.return_value = pygame.Surface((30, 20))

        cls.window = Window(cls.width, cls.height)

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    # ------------------
    # Tests init
    # ------------------
    @patch("pygame.get_init", return_value=False)
    def test_init_pygame_not_initialized(self, mock_get_init):
        """Teste que pygame.init() est appelé si non initialisé."""
        window = Window(800, 600)
        self.assertIsInstance(window.display, pygame.Surface)

    def test_initialization(self):
        """Vérifie l'initialisation des attributs principaux."""
        self.assertEqual(self.window.width, self.width)
        self.assertEqual(self.window.height, self.height)
        self.assertIsInstance(self.window.display, pygame.Surface)
        self.assertIsInstance(self.window.skier_left, pygame.Surface)
        self.assertIsInstance(self.window.skier_right, pygame.Surface)

    # ------------------
    # Tests méthodes d'affichage
    # ------------------
    def test_show_text(self):
        """Teste show_text sans erreur."""
        try:
            self.window.show_text("Test", 100, 100, (255, 255, 255), self.window.font_retro)
        except Exception as e:
            self.fail(f"show_text raised an exception {e}")

    def test_show_start_screen(self):
        """Teste show_start_screen sans erreur."""
        try:
            self.window.show_start_screen()
        except Exception as e:
            self.fail(f"show_start_screen raised an exception {e}")

    def test_show_game_over_screen(self):
        """Teste show_game_over_screen sans erreur."""
        try:
            self.window.show_game_over_screen(game_level=1, player_points=100)
        except Exception as e:
            self.fail(f"show_game_over_screen raised an exception {e}")

    def test_update_side_obstacles(self):
        """Teste update_side_limit_obstacles sans erreur."""
        try:
            self.window.update_side_obstacles(speed=5)
        except Exception as e:
            self.fail(f"update_side_limit_obstacles raised an exception {e}")

    def test_update_side_obstacles_dx_reset(self):
        """Teste la branche où self.dx <= 0 et doit être réinitialisé."""
        self.window.dx = 2  # petit dx
        self.window.update_side_obstacles(speed=5)  # dx - 5 <= 0 déclenche la branche
        # Vérifie que dx a été réajusté
        self.assertGreater(self.window.dx, 0)

    def test_update_status(self):
        """Teste update_status sans erreur."""
        try:
            self.window.update_status(game_level=1, player_lives=3, player_points=50)
        except Exception as e:
            self.fail(f"update_status raised an exception {e}")

    # ------------------
    # Tests draw
    # ------------------
    def test_draw(self):
        """Teste draw avec image visible et non visible."""
        img = pygame.Surface((50, 50))
        # Cas visible
        self.window.draw(img, 100, 100)
        # Cas non visible (y en dehors)
        self.window.draw(img, 100, -60)

    # ------------------
    # Tests draw_player
    # ------------------
    def test_draw_player_normal(self):
        """Teste draw_player normal."""
        player = MockPlayer()
        self.window.draw_player(player)

    def test_draw_player_invincible_not_drawn(self):
        """Teste draw_player quand invincible et clignotant = False."""
        player = MockPlayer()
        player.invincible = True
        player.invincible_time = 0.1  # int(0.1*10) % 2 == 1 -> draw_player=False
        player.jumping = False
        self.window.draw_player(player)

    def test_draw_player_jumping(self):
        """Teste draw_player en saut."""
        player = MockPlayer()
        player.jumping = True
        self.window.draw_player(player)

    # ------------------
    # Tests transform et flip
    # ------------------
    def test_transform_player_image(self):
        """Teste transform_player_image renvoie bien une Surface."""
        img = pygame.Surface((50, 50))
        transformed = self.window.transform_player_image(img, 45, 1.2)
        self.assertIsInstance(transformed, pygame.Surface)

    def test_flip(self):
        """Teste flip sans erreur."""
        try:
            self.window.flip()
        except Exception as e:
            self.fail(f"flip raised an exception {e}")


if __name__ == "__main__":
    unittest.main()

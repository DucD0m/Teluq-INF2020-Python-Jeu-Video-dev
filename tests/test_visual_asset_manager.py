import unittest
from unittest.mock import patch
import pygame
from classes.VisualAssetManager import VisualAssetManager


class TestVisualAssetManagerFull(unittest.TestCase):
    """Tests complets pour VisualAssetManager, incluant tous les fallbacks."""

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.manager = VisualAssetManager()
        # Nécessaire pour convert_alpha()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    # ------------------
    # Tests normaux
    # ------------------
    def test_load_retro_font_normal(self):
        font = self.manager.load_retro_font()
        self.assertIsInstance(font, pygame.font.Font)

    def test_load_snow_font_normal(self):
        font = self.manager.load_snow_font()
        self.assertIsInstance(font, pygame.font.Font)

    def test_load_skier_normal(self):
        surface = self.manager.load_skier()
        self.assertIsInstance(surface, pygame.Surface)

    def test_load_big_skier_normal(self):
        surface = self.manager.load_big_skier()
        self.assertIsInstance(surface, pygame.Surface)

    def test_load_big_tree_normal(self):
        surface = self.manager.load_big_tree()
        self.assertIsInstance(surface, pygame.Surface)

    def test_create_fallback_skier(self):
        surface = self.manager.create_fallback_skier()
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_size(), (100, 100))

    # ------------------
    # Tests fallbacks FileNotFoundError
    # ------------------
    @patch("pygame.font.Font", side_effect=FileNotFoundError)
    def test_load_retro_font_file_missing(self, mock_font):
        font = self.manager.load_retro_font()
        self.assertIs(font, self.manager.font_default)

    @patch("pygame.font.Font", side_effect=FileNotFoundError)
    def test_load_snow_font_file_missing(self, mock_font):
        font = self.manager.load_snow_font()
        self.assertIs(font, self.manager.font_default)

    @patch("pygame.image.load", side_effect=FileNotFoundError)
    def test_load_skier_file_missing(self, mock_load):
        surface = self.manager.load_skier()
        fallback = self.manager.create_fallback_skier()
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_size(), fallback.get_size())

    @patch("pygame.image.load", side_effect=FileNotFoundError)
    def test_load_tree_file_missing(self, mock_load):
        surface = self.manager.load_tree()
        self.assertIsInstance(surface, pygame.Surface)

    @patch("pygame.image.load", side_effect=FileNotFoundError)
    def test_load_rock_file_missing(self, mock_load):
        surface = self.manager.load_rock()
        self.assertIsInstance(surface, pygame.Surface)

    @patch("pygame.image.load", side_effect=FileNotFoundError)
    def test_load_big_skier_file_missing(self, mock_load):
        surface = self.manager.load_big_skier()
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_size(), (0, 0))

    @patch("pygame.image.load", side_effect=FileNotFoundError)
    def test_load_big_tree_file_missing(self, mock_load):
        surface = self.manager.load_big_tree()
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_size(), (0, 0))

    # ------------------
    # Tests erreurs pygame.error
    # ------------------
    @patch("pygame.image.load", side_effect=pygame.error)
    def test_load_skier_pygame_error(self, mock_load):
        surface = self.manager.load_skier()
        fallback = self.manager.create_fallback_skier()
        self.assertIsInstance(surface, pygame.Surface)
        self.assertEqual(surface.get_size(), fallback.get_size())

    @patch("pygame.image.load", side_effect=pygame.error)
    def test_load_tree_pygame_error(self, mock_load):
        surface = self.manager.load_tree()
        self.assertIsInstance(surface, pygame.Surface)

    @patch("pygame.image.load", side_effect=pygame.error)
    def test_load_rock_pygame_error(self, mock_load):
        surface = self.manager.load_rock()
        self.assertIsInstance(surface, pygame.Surface)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import Mock, patch

from classes.Obstacle import Obstacle


class TestObstacle(unittest.TestCase):
    """Tests unitaires de la classe Obstacle."""

    def setUp(self):
        """Crée une image factice pour les tests."""
        self.image = Mock()
        self.image.get_width.return_value = 100
        self.image.get_height.return_value = 80

        rect = Mock()
        rect.topleft = (0, 0)
        self.image.get_rect.return_value = rect

    def test_init_sets_attributes(self):
        """Vérifie l'initialisation correcte d'un obstacle."""
        obstacle = Obstacle(
            height=600,
            left_limit=0,
            right_limit=800,
            image=self.image,
            jump_allowed=True,
        )

        self.assertEqual(obstacle.image, self.image)
        self.assertFalse(obstacle.cleared)
        self.assertTrue(obstacle.jump_allowed)

        self.assertTrue(600 <= obstacle.y <= 1200)
        self.assertTrue(50 <= obstacle.x <= 750)

        self.assertEqual(
            obstacle.rect.width,
            self.image.get_width() - 20
        )
        self.assertEqual(
            obstacle.rect.height,
            self.image.get_height() - 20
        )

    def test_update_rect_updates_position(self):
        """Vérifie que le rectangle de collision est correctement mis à jour."""
        obstacle = Obstacle(
            height=600,
            left_limit=0,
            right_limit=800,
            image=self.image,
            jump_allowed=False,
        )

        obstacle.x = 100
        obstacle.y = 200

        obstacle.update_rect()

        self.assertEqual(
            obstacle.rect.topleft,
            (110, 210)
        )

    def test_set_cleared_sets_flag(self):
        """Vérifie que l'obstacle est marqué comme franchi."""
        obstacle = Obstacle(
            height=600,
            left_limit=0,
            right_limit=800,
            image=self.image,
            jump_allowed=False,
        )

        obstacle.set_cleared()

        self.assertTrue(obstacle.cleared)

    def test_update_position_moves_up(self):
        """Vérifie que l'obstacle se déplace vers le haut."""
        obstacle = Obstacle(
            height=600,
            left_limit=0,
            right_limit=800,
            image=self.image,
            jump_allowed=False,
        )

        start_y = obstacle.y

        obstacle.update_position(speed=5)

        self.assertEqual(obstacle.y, start_y - 5)

    def test_update_position_resets_when_off_screen(self):
        """Vérifie le repositionnement lorsque l'obstacle sort de l'écran."""
        obstacle = Obstacle(
            height=600,
            left_limit=0,
            right_limit=800,
            image=self.image,
            jump_allowed=False,
        )

        obstacle.y = -100
        obstacle.cleared = True

        with patch("random.randint", side_effect=[50, 200]):
            obstacle.update_position(speed=5)

        self.assertFalse(obstacle.cleared)
        self.assertEqual(obstacle.y, 650)
        self.assertEqual(obstacle.x, 200)


if __name__ == "__main__":
    unittest.main()

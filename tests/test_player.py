import unittest
from unittest.mock import Mock
from classes.Player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        # Crée des images mock pour le joueur
        self.image_left = Mock()
        self.image_right = Mock()
        self.image_left.get_width.return_value = 50
        self.image_left.get_height.return_value = 50
        self.image_left.get_rect.return_value = Mock(
            topleft=(0, 0), width=50, height=50
        )
        self.image_right.get_width.return_value = 50
        self.image_right.get_height.return_value = 50
        self.image_right.get_rect.return_value = Mock(
            topleft=(0, 0), width=50, height=50
        )

        self.player = Player(200, self.image_left, self.image_right)

    def test_horizontal_move_left_right_no_jump(self):
        keys = {"left": True, "right": False, "up": False, "down": False, "space": False}
        self.player.jumping = False
        old_x = self.player.x
        self.player.horizontal_move(keys)
        self.assertLess(self.player.x, old_x)
        self.assertEqual(self.player.image, self.image_left)

        keys = {"left": False, "right": True, "up": False, "down": False, "space": False}
        old_x = self.player.x
        self.player.horizontal_move(keys)
        self.assertGreater(self.player.x, old_x)
        self.assertEqual(self.player.image, self.image_right)

        keys = {"left": False, "right": False, "up": False, "down": False, "space": False}
        old_x = self.player.x
        self.player.horizontal_move(keys)
        self.assertEqual(self.player.dx, self.player.mx)

    def test_horizontal_move_while_jumping(self):
        keys = {"left": True, "right": True, "up": False, "down": False, "space": False}
        self.player.jumping = True
        old_x = self.player.x
        self.player.horizontal_move(keys)
        self.assertEqual(self.player.dx, 0)
        self.assertEqual(self.player.x, old_x)

    def test_vertical_move_up_down(self):
        keys = {"up": True, "down": False, "left": False, "right": False, "space": False}
        old_y = self.player.y
        self.player.vertical_move(keys)
        self.assertLess(self.player.y, old_y)

        keys = {"up": False, "down": True, "left": False, "right": False, "space": False}
        old_y = self.player.y
        self.player.vertical_move(keys)
        self.assertGreater(self.player.y, old_y)

    def test_jump_move(self):
        keys = {"space": True}
        self.player.jumping = False
        self.player.jump_move(keys)
        self.assertTrue(self.player.jumping)
        self.assertEqual(self.player.jump_time, 0.0)
        self.assertEqual(self.player.jump_x, self.player.x)

    def test_position_limits(self):
        self.player.x = -100
        self.player.y = -50
        self.player.position_limits(200, 0, 150)
        self.assertGreaterEqual(self.player.x, 0)
        self.assertGreaterEqual(self.player.y, 0)
        self.player.x = 200
        self.player.y = 300
        self.player.position_limits(200, 0, 150)
        self.assertLessEqual(self.player.x, 150)
        self.assertLessEqual(self.player.y, 150)

    def test_update_invincibility_and_stop_points(self):
        # Invincibility active, dt < duration
        self.player.invincible = True
        self.player.invincible_time = 1.0
        self.player.update_invincibility(0.5)
        self.assertTrue(self.player.invincible)
        # Invincibility ends
        self.player.update_invincibility(3)
        self.assertFalse(self.player.invincible)

        # Stop points active, dt < duration
        self.player.stop_points = True
        self.player.stop_points_time = 1.0
        self.player.update_stop_points(0.5)
        self.assertTrue(self.player.stop_points)
        # Stop points ends
        self.player.update_stop_points(3)
        self.assertFalse(self.player.stop_points)

    def test_update_jump_full_cycle(self):
        self.player.jumping = True
        self.player.jump_time = 0
        dt = self.player.jump_duration / 2
        # Première moitié
        self.player.update_jump(dt)
        self.assertTrue(self.player.jumping)
        self.assertGreater(self.player.scale, 1.0)
        self.assertGreater(self.player.angle, 0)
        # Deuxième moitié
        self.player.update_jump(dt)
        self.assertFalse(self.player.jumping)
        self.assertEqual(self.player.scale, 1.0)
        self.assertEqual(self.player.angle, 0.0)

    def test_obstacle_methods(self):
        # obstacle_cleared
        pts = self.player.points
        self.player.obstacle_cleared()
        self.assertEqual(self.player.points, pts + 25)
        # obstacle_jumped
        self.player.stop_points = False
        self.player.obstacle_jumped()
        self.assertEqual(self.player.points, pts + 25 + 100)
        self.assertTrue(self.player.stop_points)
        self.assertEqual(self.player.stop_points_time, 0.0)
        # obstacle_hit
        lives = self.player.lives
        self.player.obstacle_hit()
        self.assertEqual(self.player.lives, lives - 1)
        self.assertTrue(self.player.invincible)
        self.assertEqual(self.player.invincible_time, 0.0)

    def test_update_rect(self):
        self.player.x = 100
        self.player.y = 200
        self.player.update_rect()
        self.assertEqual(self.player.rect.topleft, (110, 210))

    def test_update_method_calls_all(self):
        # Just test that update calls all submethods without error
        self.player.jumping = True
        self.player.invincible = True
        self.player.stop_points = True
        self.player.update(0.1)  # dt = 0.1

    def test_reset(self):
        self.player.x = 999
        self.player.y = 999
        self.player.lives = 0
        self.player.points = 100
        self.player.invincible = False
        self.player.reset()
        self.assertEqual(self.player.x, self.player.starting_x)
        self.assertEqual(self.player.y, self.player.starting_y)
        self.assertEqual(self.player.lives, self.player.starting_lives)
        self.assertEqual(self.player.points, 0)
        self.assertTrue(self.player.invincible)
        self.assertEqual(self.player.invincible_time, 0.0)


if __name__ == "__main__":
    unittest.main()

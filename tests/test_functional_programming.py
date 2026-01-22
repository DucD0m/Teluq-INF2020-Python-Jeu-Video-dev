import unittest
from utils.FunctionalProgramming import add_points, side_obstacles_positions

class TestFunctionalExamples(unittest.TestCase):
    """Tests unitaires pour les fonctions de programmation fonctionnelle."""

    # ---------- add_points ----------

    def test_add_points_positive(self):
        self.assertEqual(add_points(10, 5), 15)

    def test_add_points_zero(self):
        self.assertEqual(add_points(0, 0), 0)

    def test_add_points_negative(self):
        self.assertEqual(add_points(10, -3), 7)

    # ---------- side_obstacles_positions ----------

    def test_side_obstacles_positions_basic(self):
        spacing = 50
        alignment = 5
        width = 400
        rows = 3
        dx = 0
        nb = 3

        positions = side_obstacles_positions(spacing, alignment, width, rows, dx, nb)

        # Vérifie le type
        self.assertIsInstance(positions, list)
        self.assertTrue(all(isinstance(pos, tuple) for pos in positions))
        self.assertTrue(all(len(pos) == 2 for pos in positions))

        # Vérifie la longueur : obstacles gauche + obstacles droite par ligne
        expected_length = 2*nb * (rows + 2)  # +2 car range(-2, rows)
        self.assertEqual(len(positions), expected_length)

    def test_side_obstacles_positions_dx_offset(self):
        spacing = 40
        alignment = 0
        width = 200
        rows = 2
        dx = 10
        nb = 3

        positions = side_obstacles_positions(spacing, alignment, width, rows, dx, nb)

        # Vérifie que le premier y correspond à row=-1
        y_values = sorted(set(pos[1] for pos in positions))
        self.assertEqual(y_values[0], -2*spacing + dx)
        self.assertEqual(y_values[-1], (rows - 1) * spacing + dx)

if __name__ == "__main__":
    unittest.main()

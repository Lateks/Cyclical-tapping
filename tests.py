import unittest
from math import radians, degrees
from geometry import CircleOfPlates, Trig

class TrigCircleCentralAngleTest(unittest.TestCase):
    def test_divide_into_4(self):
        angles = Trig.circle_central_angles(4)
        angles.sort()
        expected = list([0, 90, 180, 270])
        self.assertEqual(expected, angles)

    def test_divide_into_9(self):
        angles = Trig.circle_central_angles(9)
        angles.sort()
        expected = list([0, 40, 80, 120, 160, 200, 240, 280, 320])
        self.assertEqual(expected, angles)

class CircleOf4Plates(unittest.TestCase):
    def setUp(self):
        self.width, self.height = 640, 640
        self.circle = CircleOfPlates(270, (self.width/2, self.height/2), 4)

    def test_number_of_positions(self):
        positions = self.circle.positions
        positions.sort()
        expected_positions = list([(320, 50), (590, 320),
                                   (320, 590), (50, 320)])
        expected_positions.sort()

        self.assertEqual(4, len(positions))
        self.assertEqual(expected_positions, positions)

    def test_object_distance(self):
        self.assertEqual(540, self.circle.get_object_distance())

class CircleOf9Plates(unittest.TestCase):
    def setUp(self):
        self.height = 600
        self.width = 1000
        self.circle = CircleOfPlates(250, (self.width/2, self.height/2), 9)

    def test_number_of_positions(self):
        positions = self.circle.positions
        self.assertEqual(9, len(positions))

if __name__ == '__main__':
    unittest.main()

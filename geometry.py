from math import floor, sin, cos, radians

class CircleOfPlates:
    def __init__(self, screen_width, plate_radius, number_of_plates):
        self.plate_radius = plate_radius
        self.circle_radius = self.__get_circle_radius(screen_width)
        self.circle_midpoint = plate_radius + self.circle_radius
        self.number_of_plates = number_of_plates
        self.__initialize_plate_positions()

    def __get_circle_radius(self, screen_width):
        return int(floor((screen_width - 2 * self.plate_radius) / 2))

    def __initialize_plate_positions(self):
        positions = list()
        angles = self.__get_plate_angles()
        for angle in angles:
            positions.append(self.__position(angle))
        self.positions = positions

    def __get_plate_angles(self):
        angle_difference = radians(int(floor(360 / self.number_of_plates)))
        multiply = lambda x: angle_difference * x
        angles = map(multiply, range(1, self.number_of_plates + 1))
        return angles

    def __position(self, angle):
        if angle == 0:
            return self.circle_midpoint, self.plate_radius
        adjacent = Trig.adjacent_edge(angle, self.circle_radius)
        opposite = Trig.opposite_edge(angle, self.circle_radius)
        return (self.circle_midpoint + adjacent,
            self.circle_midpoint - opposite)

    def __iter__(self):
        for pos in self.positions:
            yield pos

class Trig:
    @staticmethod
    def adjacent_edge(angle, hypotenuse):
        return int(floor(sin(angle) * hypotenuse))

    @staticmethod
    def opposite_edge(angle, hypotenuse):
        return int(floor(cos(angle) * hypotenuse))

from math import floor, ceil, sin, cos, radians, sqrt

class CircleOfPlates(object):
    def __init__(self, screen_width, plate_radius, number_of_plates):
        self.plate_radius = plate_radius
        self.circle_radius = self.__get_circle_radius(screen_width)
        self.circle_midpoint = plate_radius + self.circle_radius
        self.number_of_plates = number_of_plates
        self.__initialize_plate_positions()

    def __get_circle_radius(self, screen_width):
        return int(floor((screen_width - 2 * self.plate_radius) / 2))

    def __initialize_plate_positions(self):
        angles = Trig.circle_central_angles(self.number_of_plates)
        self.positions = map(self.__position, angles)

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

    def get_object_distance(self):
        first_pos = self.__position(0)
        angle = int(ceil(self.number_of_plates / 2.0)) * \
                Trig.divide_circle_by(self.number_of_plates)
        second_pos = self.__position(angle)
        return Trig.euclidean_distance(first_pos, second_pos)

class Trig(object):
    @staticmethod
    def adjacent_edge(deg_angle, hypotenuse):
        angle = radians(deg_angle)
        return int(round(sin(angle) * hypotenuse))

    @staticmethod
    def opposite_edge(deg_angle, hypotenuse):
        angle = radians(deg_angle)
        return int(round(cos(angle) * hypotenuse))

    @staticmethod
    def circle_central_angles(divisor):
        angle_difference = Trig.divide_circle_by(divisor)
        multiply = lambda x: angle_difference * x
        angles = map(multiply, range(0, divisor))
        return angles

    @staticmethod
    def divide_circle_by(divisor):
        return int(floor(360 / divisor))

    @staticmethod
    def euclidean_distance(point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return sqrt((x2 - x1)**2 + (y2 - y1)**2)

from math import floor, ceil, sin, cos, radians, sqrt

class CircleCircumference(object):
    """Calculate evenly spaced positions on the circumference
       of a circle."""

    def __init__(self, circle_radius, circle_midpoint, number_of_points):
        self.circle_radius = circle_radius
        self.number_of_points = number_of_points
        self.mid_x, self.mid_y = circle_midpoint
        self.__initialize_target_positions()

    def __initialize_target_positions(self):
        angles = Trig.circle_central_angles(self.number_of_points)
        self.positions = map(self.__position, angles)

    def __position(self, angle):
        """Calculates the position of a point on the circumference
        given a central angle relative to the vertical diameter of
        the circle."""
        if angle == 0:
            return self.mid_x, self.__vertical_offset()
        adjacent = Trig.adjacent_edge(angle, self.circle_radius)
        opposite = Trig.opposite_edge(angle, self.circle_radius)
        return (self.mid_x + adjacent, self.mid_y - opposite)

    def __vertical_offset(self):
        """Calculates the minimum distance from the circle
        circumference to the edge of the screen/coordinates."""
        return self.mid_y - self.circle_radius

    def __iter__(self):
        for pos in self.positions:
            yield pos

    def get_position_at(self, index):
        return self.positions[index]

    def get_object_distance(self):
        """Returns the Euclidean distance between two successive
        targets on the perimeter. "Successive" here is defined
        in terms of the trial environment: the successor of a
        target is the one slightly clockwise from the opposite
        side of the circle."""
        first_pos = self.__position(0)
        angle = int(ceil(self.number_of_points / 2.0)) * \
                Trig.divide_circle_by(self.number_of_points)
        second_pos = self.__position(angle)
        return Trig.euclidean_distance(first_pos, second_pos)

class Trig(object):
    """Some static trigonometric helper functions."""
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

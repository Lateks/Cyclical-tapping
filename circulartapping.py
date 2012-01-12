import sys, pygame
from math import floor, sin, cos, radians

def main():
    width = height = 640 # TODO: read these variables from a settings file
    plate_radius = 50    # (should be given as a parameter?)
    num_plates = 9
    plate_color = 244, 238, 224

    plate_circle = CircleOfPlates(width, plate_radius, num_plates)
    plate_positions = plate_circle.positions

    pygame.init()
    screensize = width, height
    window = pygame.display.set_mode(screensize)

    for pos in plate_positions:
        pygame.draw.circle(window, plate_color, pos, plate_radius)

    pygame.display.flip()

    while True:
    # TODO: quit when ESC is pressed
    # TODO: log mouse into file
    # TODO: changing colors for the ball markers
    # (next one highlights on mouseclick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

class CircleOfPlates:
    def __init__(self, screen_width, plate_radius, number_of_plates):
        self.circle_radius = self.get_circle_radius(screen_width, plate_radius)
        self.circle_midpoint = plate_radius + self.circle_radius
        self.number_of_plates = number_of_plates
        self.plate_radius = plate_radius
        self.initialize_plate_positions()

    def initialize_plate_positions(self):
        positions = list()
        first_pos = self.circle_midpoint, self.plate_radius
        positions.append(first_pos)

        angle_difference = radians(int(floor(360 / self.number_of_plates)))
        angle = radians(0)
        for i in range(1, self.number_of_plates):
            angle += angle_difference
            positions.append(self.position(angle))
        self.positions = positions

    def get_circle_radius(self, screen_width, plate_radius):
        return int(floor((screen_width - 2 * plate_radius) / 2))

    def position(self, angle):
        adjacent = Trig.adjacent_edge(angle, self.circle_radius)
        opposite = Trig.opposite_edge(angle, self.circle_radius)
        return (self.circle_midpoint + adjacent,
            self.circle_midpoint - opposite)

class Trig:
    @staticmethod
    def adjacent_edge(angle, hypotenuse):
        return int(floor(sin(angle) * hypotenuse))

    @staticmethod
    def opposite_edge(angle, hypotenuse):
        return int(floor(cos(angle) * hypotenuse))

if __name__ == '__main__':
    main()

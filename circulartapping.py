import sys, pygame, time
from Xlib import X, display
from math import floor, sin, cos, radians

def main():
    width = height = 640 # TODO: read these variables from a settings file
    plate_radius = 50    # (should be given as a parameter?)
    num_plates = 9
    plate_color = 244, 238, 224

    plate_circle = CircleOfPlates(width, plate_radius, num_plates)

    screensize = width, height
    screen = CircleScreen(screensize)
    screen.draw_circles(plate_circle, plate_radius, plate_color)

    mouselog = MouseLog()
    runner = ProgRunner(screen, mouselog)
    runner.run()

class ProgRunner:
    def __init__(self, screen, mouselog):
        self.screen = screen
        self.mouselog = mouselog

    def run(self):
        self.screen.draw()
        self.__init_screen_root()
        while True:
        # TODO: quit when ESC is pressed
        # TODO: changing colors for the ball markers
        # (next one highlights on mouseclick)
            self.__log_mouse()
            self.__handle_pygame_events()

    def __handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.mouselog.write()
                sys.exit(0)

    def __log_mouse(self):
        self.display.sync()
        mouse_pos = self.root.query_pointer()._data
        self.mouselog.log_position(mouse_pos["root_x"],
            mouse_pos["root_y"])

    def __init_screen_root(self):
        self.display = display.Display()
        Xscreen = self.display.screen()
        self.root = Xscreen.root

class CircleScreen:
    def __init__(self, screensize):
        pygame.init()
        self.window = pygame.display.set_mode(screensize)

    def draw_circles(self, circle_positions, circle_radius, circle_color):
        for pos in circle_positions:
            pygame.draw.circle(self.window, circle_color, pos, circle_radius)

    def draw(self):
        pygame.display.flip()

class MouseLog:
    def __init__(self):
        self.mouse_positions = list()

    def log_position(self, x, y):
        self.mouse_positions.append(Coordinate(x, y))

    def write(self):
        # TODO: write to file
        for pos in self.mouse_positions:
            print pos

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%d\t%d" % (self.x, self.y)

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
        angles = list()
        for i in range(0, self.number_of_plates):
            angles.append(i * angle_difference)
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

if __name__ == '__main__':
    main()

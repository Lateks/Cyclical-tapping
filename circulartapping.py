import sys, pygame, time
from geometry import CircleOfPlates
from screen import PygameDisplayWindow
from logmouse import MouseLogger

def main():
    params = Parameters()
    width = params.width
    height = params.height
    plate_radius = params.plate_radius
    num_plates = params.num_plates
    plate_color = params.plate_color

    plate_circle = CircleOfPlates(width, plate_radius, num_plates)

    screensize = width, height
    screen = PygameDisplayWindow(screensize)
    screen.draw_circles(plate_circle, plate_radius, plate_color)

    runner = ProgRunner(screen)
    runner.run()

class Parameters(object):
    width = height = 640
    plate_radius = 50
    num_plates = 9
    plate_color = 244, 238, 224

    def __init__(self):
        try:
            self.config_file = open("config", "r")
            self.__read_parameters()
        except IOError:
            print "Could not open the config file. Using defaults."
        except ParameterError as value:
            print "Invalid config file or parameters:\n" + \
                  "%s\nUsing defaults." % value
        self.config_file.close()

    def __read_parameters(self):
        parameters = list()
        for line in self.config_file:
            if self.__line_is_not_comment(line):
                tokens = self.__tokenize_line(line)
                parameters += tokens
        self.__unlist_parameters(parameters)

    def __line_is_not_comment(self, line):
        return not line[0] == '#'

    def __tokenize_line(self, line):
        tokens = list()
        line_params = line.split(' ')
        for token in line_params:
            token = self.__param_to_int(token)
            tokens.append(token)
        return tokens

    def __param_to_int(self, string):
        try:
            integer = int(string)
            if integer < 0:
                raise ParameterError("Negative parameters given. Should be positive.")
            return integer
        except ValueError:
            raise ParameterError("Non-numeric parameters given.")

    def __unlist_parameters(self, parameters):
        if len(parameters) < 6:
            raise ParameterError("Parameters missing.")
        self.width = self.height = parameters[0]
        self.plate_radius = parameters[1]
        self.num_plates = parameters[2]
        self.plate_color = parameters[3], parameters[4], parameters[5]

class ParameterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ProgRunner(object):
    def __init__(self, screen):
        self.screen = screen
        self.mouselog = MouseLogger()

    def run(self):
        self.screen.draw()
        while True:
            self.mouselog.log_mouse()
            self.__handle_pygame_events()

    def __handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.mouselog.write_log()
                sys.exit(0)

if __name__ == '__main__':
    main()

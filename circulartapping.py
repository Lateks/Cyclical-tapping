import sys, pygame, time
from math import floor
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

    circle_radius = int(floor((height - 2 * plate_radius) / 2))
    circle_midpoint = width / 2, height / 2
    plate_circle = CircleOfPlates(circle_radius, circle_midpoint, num_plates)

    screensize = width, height
    screen = PygameDisplayWindow(screensize)
    screen.draw_circles(plate_circle, plate_radius, plate_color)

    target_distance = plate_circle.get_object_distance()
    trialdata = {'target_width': 2 * plate_radius,
                 'target_dist': target_distance}
    mouselog = MouseLogger(trialdata)
    mouse_fps = 100
    runner = ProgRunner(screen, mouselog, mouse_fps, 3 * num_plates)
    runner.run()

class Parameters(object):
    width, height = 640, 640
    plate_radius = 50
    num_plates = 9
    plate_color = 244, 238, 224

    def __init__(self):
        try:
            self.config_file = open("config", "r")
            self.__read_parameters()
            self.config_file.close()
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
        if len(parameters) < 7:
            raise ParameterError("Parameters missing.")
        self.width, self.height = parameters[0], parameters[1]
        self.plate_radius = parameters[2]
        self.num_plates = parameters[3]
        self.plate_color = parameters[4], parameters[5], parameters[6]

class ParameterError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ProgRunner(object):
    def __init__(self, screen, mouselogger, log_fps, trial_length_in_clicks):
        self.screen = screen
        self.mouselog = mouselogger
        self.logger_sleep_time = 1.0/log_fps
        self.trial_length = trial_length_in_clicks
        self.clicks = 0

    def run(self):
        self.screen.draw()
        while True:
            self.__log_mouse()
            self.__handle_pygame_events()

    def __log_mouse(self):
        time.sleep(self.logger_sleep_time)
        self.mouselog.log_mouse()

    def __handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouselog.log_mouseclick(event)
                self.clicks += 1
                if self.__trial_done():
                    self.__exit()

    def __exit(self):
        self.screen.draw_text("Trial done!", (0, 200, 0))
        self.screen.draw()
        self.mouselog.write_log()
        sys.exit(0)

    def __trial_done(self):
        return self.clicks >= self.trial_length

if __name__ == '__main__':
    main()

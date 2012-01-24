import sys, pygame, time
from math import floor
from geometry import CircleCircumference
from screen import PygameDisplayWindow
from logmouse import MouseLogger
from parameter_parser import Parameters

def main():
    params = Parameters()
    width = params.width
    height = params.height
    plate_radius = params.plate_radius
    num_plates = params.num_plates
    plate_color = params.plate_color

    circle_radius = int(floor((height - 2 * plate_radius) / 2))
    circle_midpoint = width / 2, height / 2
    plate_circle = CircleCircumference(circle_radius, circle_midpoint, num_plates)

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

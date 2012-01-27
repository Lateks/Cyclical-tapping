import sys, pygame, time
from math import floor
from geometry import CircleCircumference
from screen import PygameDisplayWindow
from logmouse import MouseLogger
from parameter_parser import Parameters

class TrialRunner(object):
    def __init__(self):
        self.params = Parameters()

    def new_trial(self, subject_name):
        self.subject_name = subject_name
        self.circle_radius, self.target_radius = self.params.get_test_setup()

        self.__init_screen()
        self.__calculate_circle()
        self.screen.draw_circles(self.circle, self.target_radius,
            self.params.get_target_color())

        self.__init_mouselogger()
        self.__init_click_counter()

    def __init_screen(self):
        screensize = self.params.get_screensize()
        self.screen = PygameDisplayWindow(screensize)

    def __calculate_circle(self):
        width, height = self.params.get_screensize()
        circle_midpoint = width / 2, height / 2
        self.circle = CircleCircumference(self.circle_radius, circle_midpoint,
            self.params.get_number_of_targets())

    def __init_mouselogger(self):
        trialdata = {'target_width': 2 * self.target_radius,
                     'target_dist': self.circle.get_object_distance(),
                     'subject_name': self.subject_name}
        self.mouselog = MouseLogger(trialdata)
        log_fps = 100
        self.logger_sleep_time = 1.0/log_fps

    def __init_click_counter(self):
        self.trial_length = 3 * self.params.get_number_of_targets()
        self.clicks = 0

    def run(self):
        self.screen.draw()
        self.running = True
        self.logging = False
        while self.running:
            if self.logging:
                self.__log_mouse()
            self.__handle_pygame_events()

    def __log_mouse(self):
        time.sleep(self.logger_sleep_time)
        self.mouselog.log_mouse()

    def __handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__exit()
                return
            if (event.type == pygame.KEYUP or event.type == pygame.KEYDOWN) and \
                event.key == pygame.K_ESCAPE:
                self.__exit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.__log_mouseclick(event)
                if self.__trial_done():
                    self.__exit()
                    return

    def __log_mouseclick(self, event):
        if self.logging:
            self.mouselog.log_mouseclick(event)
        else:
            self.logging = True
        self.clicks += 1

    def __exit(self):
        self.running = False
        self.screen.draw_text("Trial done!", (0, 200, 0))
        self.screen.draw()
        self.mouselog.write_log()
        time.sleep(2)
        pygame.display.quit()

    def __trial_done(self):
        return self.clicks >= self.trial_length

import sys, pygame, time
from math import floor
from geometry import CircleCircumference
from screen import PygameDisplayWindow
from logmouse import MouseLogger
from parameter_parser import Parameters

class TrialRunner(object):
    """Sets up trial environments and handles screens, mouseloggers
    and everything else related to running trials."""
    HILIGHT_COLOR = (255, 165, 0)

    def __init__(self):
        self.params = Parameters()
        self.trials = 0
        self.rounds = 3

    def new_trial(self, subject_name):
        """Sets up a new trial (must be called before run)"""
        self.subject_name = subject_name
        self.trials += 1
        self.circle_radius, self.target_radius = self.params.get_test_setup()

        self.__init_screen()
        self.__calculate_circle()
        self.__calculate_targets()
        self.screen.draw_circles(self.circle, self.target_radius,
            self.params.get_target_color())

        self.__init_mouselogger()
        self.__init_click_counter()

    def __init_screen(self):
        screensize = self.params.get_screensize()
        self.screen = PygameDisplayWindow(screensize, self.trials)

    def __calculate_circle(self):
        """Calculates target positions on the circle perimeter"""
        width, height = self.params.get_screensize()
        circle_midpoint = width / 2, height / 2
        self.circle = CircleCircumference(self.circle_radius, circle_midpoint,
            self.params.get_number_of_targets())

    def __calculate_targets(self):
        """Calculates the indices of successive targets"""
        num_targets = self.params.get_number_of_targets()
        half = num_targets / 2
        current = half + 1
        self.targets = list([0])
        while current < num_targets:
            self.targets.append(current)
            self.targets.append(current - half)
            current = current + 1

    def __init_mouselogger(self):
        trialdata = {'target_width': 2 * self.target_radius,
                     'target_dist': self.circle.get_object_distance(),
                     'subject_name': self.subject_name}
        self.mouselog = MouseLogger(trialdata)
        log_fps = 100
        self.logger_sleep_time = 1.0/log_fps

    def __init_click_counter(self):
        self.trial_length = self.rounds * self.params.get_number_of_targets()
        self.clicks = 0

    def run(self):
        "Runs a trial with the current setup"
        self.running = True
        self.logging = False
        self.prevtarget = None
        self.__hilight_next_target()
        while self.running:
            if self.logging:
                self.__log_mouse()
            self.__handle_pygame_events()

    def __log_mouse(self):
        """Sends a command to mouse logger to log mouse position.
        A brief sleep time is included before logging the mouse
        to keep the fps close to constant."""
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
                self.__set_new_target()
                self.__hilight_next_target()

    def __log_mouseclick(self, event):
        "Logs a mouse click or starts logging if not already started."
        if self.logging:
            self.mouselog.log_mouseclick(event)
        else:
            self.logging = True
        self.clicks += 1

    def __set_new_target(self):
        """Sends the next target position to the mouse logger."""
        target = self.__get_next_target()
        self.mouselog.set_current_target(target)

    def __hilight_next_target(self):
        """Highlights next target and unhighlights the previous one."""
        target = self.__get_next_target()
        self.screen.draw_circles([target], self.target_radius, self.HILIGHT_COLOR)
        if self.prevtarget:
            self.screen.draw_circles([self.prevtarget], self.target_radius,
                self.params.get_target_color())
        self.screen.draw()
        self.prevtarget = target

    def __get_next_target(self):
        """Finds the position of the next target and returns it."""
        target_i = self.targets[self.clicks % self.params.get_number_of_targets()]
        return self.circle.get_position_at(target_i)

    def __exit(self):
        "Writes log to file and does a clean exit."
        self.running = False
        self.screen.draw_text("Trial done!", (0, 200, 0))
        self.screen.draw()
        self.mouselog.write_log()
        time.sleep(1)
        pygame.display.quit()

    def __trial_done(self):
        """Checks if the trial is done (a certain number of mouseclicks
        must have been observed)."""
        return self.clicks >= self.trial_length

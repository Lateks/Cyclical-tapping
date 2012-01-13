import sys, pygame, time
from geometry import CircleOfPlates
from screen import CircleScreen
from logmouse import MouseLogger

def main():
    width = height = 640 # TODO: read these variables from a settings file
    plate_radius = 50    # (should be given as a parameter?)
    num_plates = 9
    plate_color = 244, 238, 224

    plate_circle = CircleOfPlates(width, plate_radius, num_plates)

    screensize = width, height
    screen = CircleScreen(screensize)
    screen.draw_circles(plate_circle, plate_radius, plate_color)

    mouselog = MouseLogger()
    runner = ProgRunner(screen, mouselog)
    runner.run()

class ProgRunner:
    def __init__(self, screen, mouselog):
        self.screen = screen
        self.mouselog = mouselog

    def run(self):
        self.screen.draw()
        while True:
        # TODO: quit when ESC is pressed
        # TODO: changing colors for the ball markers
        # (next one highlights on mouseclick)
            self.mouselog.log_mouse()
            self.__handle_pygame_events()

    def __handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.mouselog.write_log()
                sys.exit(0)

if __name__ == '__main__':
    main()

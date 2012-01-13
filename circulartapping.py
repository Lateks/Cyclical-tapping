import sys, pygame, time
from geometry import CircleOfPlates
from screen import CircleScreen
from mouselog import MouseLog
from Xlib import X, display

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

if __name__ == '__main__':
    main()

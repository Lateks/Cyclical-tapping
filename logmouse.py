from Xlib import X, display
import time

class MouseLogger(object):
    def __init__(self):
        self.mouse_positions = list()
        self.timestamps = list()
        self.display = display.Display()
        Xscreen = self.display.screen()
        self.root = Xscreen.root
        self.started = False

    def log_mouse(self):
        self.__sync()
        logtime = self.__time_in_ms_since_start()
        pointer_x, pointer_y = self.__pointer_position()
        self.__log_position_and_time(logtime, pointer_x, pointer_y)

    def __sync(self):
        time.sleep(0.01)
        self.display.sync()

    def __time_in_ms_since_start(self):
        current_time = time.time()
        if not self.started:
            self.start_time = current_time
            self.started = True
        return current_time - self.start_time

    def __pointer_position(self):
        pointer_pos = self.root.query_pointer()._data
        return pointer_pos["root_x"], pointer_pos["root_y"]

    def __log_position_and_time(self, time, x, y):
        self.timestamps.append(time)
        self.mouse_positions.append(Coordinate(x, y))

    def write_log(self):
        for pos in self.mouse_positions:
            print pos

class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%d\t%d" % (self.x, self.y)

from Xlib import X, display
import os, time, datetime

class MouseLogger(object):
    def __init__(self, trialdata):
        self.mouse_positions = list()
        self.timestamps = list()
        self.trialdata = trialdata
        self.mouse_pointer = PointerTracker()

    def log_mouse(self):
        time, pointer_x, pointer_y = self.mouse_pointer.get_timed_position()
        self.timestamps.append(time)
        self.mouse_positions.append(Coordinate(pointer_x, pointer_y))

    def write_log(self):
        log_file = self.__fetch_log_file()
        self.__write_trialdata(log_file)
        for i in range(0, len(self.mouse_positions)):
            line = self.__format_output_line(i)
            log_file.write(line)
        log_file.close()

    def __fetch_log_file(self):
        self.log_file_handler = LogFileHandler()
        return self.log_file_handler.get_logfile()

    def __write_trialdata(self, log_file):
        data = "# Target width = %d\n" % (self.trialdata['target_width']) + \
               "# Target distance = %d\n\n" % (self.trialdata['target_dist'])
        log_file.write(data)

    def __format_output_line(self, log_index):
        return "%.4f\t%s\n" % (self.timestamps[log_index],
            str(self.mouse_positions[log_index]))

class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%d\t%d" % (self.x, self.y)

class PointerTracker(object):
    def __init__(self):
        self.display = display.Display()
        Xscreen = self.display.screen()
        self.root = Xscreen.root
        self.timer = Timer()

    def get_timed_position(self):
        self.display.sync()
        timestamp = self.timer.get_time_in_ms_since_start()
        pointer_pos = self.root.query_pointer()._data
        return timestamp, pointer_pos["root_x"], pointer_pos["root_y"]

class Timer(object):
    def __init__(self):
        self.started = False

    def get_time_in_ms_since_start(self):
        current_time = time.time()
        if not self.started:
            self.start_time = current_time
            self.started = True
        return current_time - self.start_time

class LogFileHandler(object):
    def __init__(self):
        self.log_dir = "logs"

    def get_logfile(self):
        self.__ensure_log_directory_exists()
        log_file_name = self.__make_log_name()
        log_file = self.__get_file_for_writing(
                    "%s/%s" % (self.log_dir, log_file_name))
        return log_file

    def __ensure_log_directory_exists(self):
        try:
            os.mkdir(self.log_dir)
        except OSError:
            pass

    def __make_log_name(self):
        timestamp = str(datetime.datetime.now())
        timestamp = timestamp.replace(' ', '-')
        logname = timestamp + '.log'
        return logname

    def __get_file_for_writing(self, filename):
        try:
            file = open(filename, "w")
            return file
        except IOError as (errno, strerror):
            raise LogFileError("Could not open file %s." % filename + \
                  "Error %d: %s" % (errno, strerror))

class LogFileError(Exception):
    def __init__(self):
        self.value = value

    def __str__(self):
        return repr(self.value)

from Xlib import X, display
import os, time, datetime

class MouseLogger(object):
    def __init__(self, trialdata):
        self.mouse_positions = list()
        self.timestamps = list()
        self.started = False
        self.log_dir = "logs"
        self.trialdata = trialdata

        self.display = display.Display()
        Xscreen = self.display.screen()
        self.root = Xscreen.root

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
        log_file = self.__get_logfile()
        self.__write_trialdata(log_file)
        for i in range(0, len(self.mouse_positions)):
            line = self.__format_output_line(i)
            log_file.write(line)
        log_file.close()

    def __write_trialdata(self, log_file):
        data = "Target width = %d\n" % (self.trialdata['target_width']) + \
               "Target distance = %d\n" % (self.trialdata['target_dist']) + \
               "##########\n\n"
        log_file.write(data)

    def __format_output_line(self, log_index):
        return "%.4f\t%s\n" % (self.timestamps[log_index],
            str(self.mouse_positions[log_index]))

    def __get_logfile(self):
        logdir_exists = self.__check_for_and_create_log_directory()
        if not logdir_exists:
            self.log_dir = '.'
        log_file_name = self.__make_log_name()
        log_file = self.__get_file_for_writing(
                    "%s/%s" % (self.log_dir, log_file_name))
        return log_file

    def __check_for_and_create_log_directory(self):
        if not os.path.exists(self.log_dir):
            try:
                os.mkdir(self.log_dir)
            except OSError as (errno, strerror):
                print "Encountered an error while creating log file directory:\n" + \
                      "%d: %s\n" % (errno, strerror) + \
                      "Attempting to write log to current directory."
                return False
        return True

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
            raise LoggingError("Could not open file %s." % filename + \
                  "Error %d: %s" % (errno, strerror))

class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%d\t%d" % (self.x, self.y)

class LoggingError(Exception):
    def __init__(self):
        self.value = value

    def __str__(self):
        return repr(self.value)

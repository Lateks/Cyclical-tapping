import pygame, os, time, datetime, codecs

class MouseLogger(object):
    CLICK = 'CLICK'
    NO_EVENT = ''

    def __init__(self, trialdata):
        self.mouse_positions = list()
        self.timestamps = list()
        self.trialdata = trialdata
        self.timer = Timer()

    def log_mouse(self):
        time = self.timer.get_time_in_ms_since_start()
        pointer_x, pointer_y = self.__get_pointer_position()
        self.timestamps.append(time)
        self.mouse_positions.append({'pos': Coordinate(pointer_x, pointer_y),
            'event_type': self.NO_EVENT})

    def __get_pointer_position(self):
        pos_x, pos_y = pygame.mouse.get_pos()
        return pos_x, pos_y

    def log_mouseclick(self, click_event):
        time = self.timer.get_time_in_ms_since_start()
        pointer_x, pointer_y = click_event.pos
        self.timestamps.append(time)
        self.mouse_positions.append({'pos': Coordinate(pointer_x, pointer_y),
            'event_type': self.CLICK})

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
        data = '# Subject name: %s\n' % (self.trialdata['subject_name']) + \
               '# Target width: %d\n' % (self.trialdata['target_width']) + \
               '# Target distance: %d\n\n' % (self.trialdata['target_dist'])
        log_file.write(data)

    def __format_output_line(self, log_index):
        mouse_event = self.mouse_positions[log_index]
        output = "%.4f\t%s" % (self.timestamps[log_index],
            str(mouse_event['pos']))
        if mouse_event['event_type'] == self.CLICK:
            output += '\t%s' % self.CLICK
        output += '\n'
        return output

class Coordinate(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%d\t%d" % (self.x, self.y)

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
            file = codecs.open(filename, "w", "utf-8")
            return file
        except IOError as (errno, strerror):
            raise LogFileError("Could not open file %s." % filename + \
                  "Error %d: %s" % (errno, strerror))

class LogFileError(Exception):
    def __init__(self):
        self.value = value

    def __str__(self):
        return repr(self.value)

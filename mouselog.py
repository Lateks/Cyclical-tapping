class MouseLog:
    def __init__(self):
        self.mouse_positions = list()

    def log_position(self, x, y):
        self.mouse_positions.append(Coordinate(x, y))

    def write(self):
        # TODO: write to file
        for pos in self.mouse_positions:
            print pos

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "%d\t%d" % (self.x, self.y)

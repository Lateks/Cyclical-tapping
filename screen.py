import pygame

class PygameDisplayWindow(object):
    def __init__(self, screensize, trial_num):
        pygame.init()
        self.window = pygame.display.set_mode(screensize)
        pygame.display.set_caption('Trial %d' % trial_num)
        x, y = screensize
        self.mid_x = x / 2
        self.mid_y = y / 2

    def draw_circles(self, circle_positions, circle_radius, circle_color):
        for pos in circle_positions:
            pygame.draw.circle(self.window, circle_color, pos, circle_radius)

    def draw_text(self, text, rgb_color):
        font = pygame.font.Font(None, 40)
        label = font.render(text, 1, rgb_color)
        pos_x, pos_y = self.__get_center_position_for_label(label)
        self.window.blit(label, (pos_x, pos_y))

    def __get_center_position_for_label(self, label):
        width = label.get_width()
        height = label.get_height()
        pos_x = self.mid_x - (width/2)
        pos_y = self.mid_y - (height/2)
        return pos_x, pos_y

    def draw(self):
        pygame.display.flip()

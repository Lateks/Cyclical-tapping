import pygame

class PygameDisplayWindow:
    def __init__(self, screensize):
        pygame.init()
        self.window = pygame.display.set_mode(screensize)

    def draw_circles(self, circle_positions, circle_radius, circle_color):
        for pos in circle_positions:
            pygame.draw.circle(self.window, circle_color, pos, circle_radius)

    def draw(self):
        pygame.display.flip()

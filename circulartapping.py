import sys, pygame
from math import floor, sin, cos, radians
pygame.init()

def initialize_ball_positions(screen_width, ball_radius, number_of_balls):
    positions = list()
    first_pos = int(floor(screen_width/2)), ball_radius
    positions.append(first_pos)

    circle_radius = get_circle_radius(screen_width, ball_radius)
    circle_mid = ball_radius + circle_radius
    angle_difference = radians(int(floor(360 / num_balls)))
    angle = radians(0)
    for i in range(1, number_of_balls):
        angle += angle_difference

    return positions

def next_position(angle, circle_radius, circle_midpoint):
    adjacent = adjacent_edge(angle, circle_radius)
    opposite = opposite_edge(angle, circle_radius)
    positions.append((circle_midpoint + adjacent,
        circle_midpoint - opposite))

def adjacent_edge(angle, hypotenuse):
    return int(floor(sin(angle) * hypotenuse))

def opposite_edge(angle, hypotenuse):
    return int(floor(cos(angle) * hypotenuse))

def get_circle_radius(screen_width, ball_radius):
    return int(floor((screen_width - 2 * ball_radius) / 2))

if __name__ == '__main__':
    width = height = 640 # TODO: read these variables from a settings file
    ball_radius = 50     # (should be given as a parameter?)
    num_balls = 9
    ball_positions = initialize_ball_positions(width, ball_radius, num_balls)

    screensize = width, height
    ball_color = 244, 238, 224

    window = pygame.display.set_mode(screensize)

    for pos in ball_positions:
        pygame.draw.circle(window, ball_color, pos, ball_radius)

    pygame.display.flip()

    while True:
    # TODO: quit when ESC is pressed
    # TODO: log mouse into file
    # TODO: changing colors for the ball markers
    # (next one highlights on mouseclick)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)


import pygame
import sys
import random
from pygame import *
from random import randint, seed
from os import environ

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
width, height, = 800, 600
back_color = (255, 255, 255)
clock = pygame.time.Clock()
screen = display.set_mode((width, height), RESIZABLE)
display.set_caption("PID simulator")

pygame.font.init()
font = pygame.font.SysFont("Consolas", 20)

RED = (255, 0, 0)
BLACK = (0, 0, 0)

class particle_1d(object):
    def __init__(self, mass, pos, vel, static_thres, kinetic_fric):
        self.mass = mass
        self.pos = pos
        self.vel = vel
        self.static_thres = static_thres
        self.kinetic_fric = kinetic_fric

    def update(self, impulse):
        """Update the pos of the particle based on the magnitude
        of the impulse."""
        # Apply impulse only if it exceeds the static threshold.
        if abs(impulse) > self.static_thres:
            self.vel += impulse / self.mass
        else:
            self.vel = 0
        if self.vel != 0:
            vel_sign = sign(self.vel)
            vel_mag = max(0, abs(self.vel) - self.kinetic_fric)
            self.vel = vel_sign * vel_mag
        self.pos += self.vel

    def get_copy(self):
        return particle_1d(self.mass, self.pos, self.vel, self.static_thres, self.kinetic_fric)

random.seed(2)
def events():
    global done, width, height
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            done = True
        if event.type == VIDEORESIZE:
            width, height = event.size
            screen = display.set_mode((width, height), RESIZABLE)
        if event.type == KEYDOWN and event.key == K_SPACE:
            render_path(dx=1, var=particle_1d(mass=1, pos=200, vel=0, static_thres=1, kinetic_fric=0.1),
                        seed=randint(0, 100), draw_path=True,
                        K_proportional=0.05, K_integral=(0, 0.0004), K_derivative=0.5)
# (1, 0.1)
# (0.05, 0.0004, 0.5)

def render_path(dx, var, seed, draw_path, K_proportional, K_integral, K_derivative):
    random.seed(seed)
    steps = 100000
    # steps = 100000
    step = 1/steps
    for K in (K_proportional, K_integral, K_derivative):
        if type(K) == tuple:
            for K_iterator in [i * step for i in range(
                    int(K[0] * steps), int(K[1] * steps))]:
                var_copy = var.get_copy()
                clock.tick(K_iterator * 5 + 100)
                if K == K_proportional:
                    render_path(dx, var_copy, seed, True, K_iterator, K_integral, K_derivative)
                if K == K_integral:
                    render_path(dx, var_copy, seed, True, K_proportional, K_iterator, K_derivative)
                if K == K_derivative:
                    render_path(dx, var_copy, seed, True, K_proportional, K_integral, K_iterator)
            return
    x = 0
    set_point = []
    while len(set_point) <= width:
        set_point.extend([randint(100, height - 100)] * 300)
    set_point = set_point[:width]
    integral = 0
    prev_error = set_point[0] - var.pos
    point_list = []
    while 0 <= x < width:
        point_list.append((x, var.pos))
        error = set_point[x] - var.pos
        integral += error
        derivative = error - prev_error
        prev_error = error
        impulse = K_proportional*error + K_integral*integral + K_derivative*derivative
        var.update(impulse)
        x += 1
    screen.fill(back_color)
    pygame.draw.lines(screen, (255, 100, 100), False, list(zip(range(len(set_point)), set_point)), 4)
    if draw_path:
        pygame.draw.lines(screen, BLACK, False, point_list, 2)
        if K_proportional:
            draw_path = font.render('Proportional factor: ' + str(round(K_proportional, 3)), True, BLACK)
            screen.blit(draw_path, (0, 0))
        if K_integral:
            draw_path = font.render('Integral factor: ' + str(round(K_integral, 8)), True, BLACK)
            screen.blit(draw_path, (0, 20))
        if K_derivative:
            draw_path = font.render('Derivative factor: ' + str(round(K_derivative, 3)), True, BLACK)
            screen.blit(draw_path, (0, 40))
    display.update()

def sign(number):
    if number > 0:
        return 1
    return -1

done = False
display.update()
while not done:
    clock.tick(1000)
    events()
pygame.quit()
sys.exit()
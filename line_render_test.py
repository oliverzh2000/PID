import pygame
from pygame import *
from pygame import surface
import sys
from random import randint
from os import environ

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
width, height, = 800, 600
back_color = (255, 255, 255)
clock = pygame.time.Clock()
screen = display.set_mode((width, height), RESIZABLE)
display.set_caption("Line render simulator")

def events():
    global done, width, height
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == VIDEORESIZE:
            width, height = event.size
            screen = display.set_mode((width, height), RESIZABLE)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

def render_path():
    screen.fill(back_color)
    cols = 10
    rows = 10
    values = [(randint(0, 256), randint(0, 256), randint(0, 256))
              for col in range(cols)
              for row in range(rows)]
    pxarray = PixelArray(screen)
    pxarray[3, 5] = (255, 0, 0)
    pxarray[8, 15] = (0, 255, 0)
    render_surf = pxarray.make_surface()
    del pxarray
    transform.scale(render_surf, (600, 800))
    screen.blit(render_surf, (50, 50))
    display.update()


done = False

display.update()
while not done:
    print(clock.tick(60))
    events()
    render_path()
pygame.quit()
sys.exit()
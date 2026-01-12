import pygame as pg
import random as rd 
from settings import *
from object import *

pg.init()


screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Tutorial")
clock = pg.time.Clock()
run = True

board = Board(WINDOW_WIDTH, WINDOW_HEIGHT)
player = Human(WINDOW_WIDTH // 8, WINDOW_HEIGHT // 2)
board.addObjects(player)


while run:
    dt = clock.tick(60) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    board.update(dt)
    board.draw()
    pg.display.flip()

pg.quit()



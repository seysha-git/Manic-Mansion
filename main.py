import pygame as pg
from pygame.locals import *
from settings import *
from object import *

pg.init()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Tutorial")
clock = pg.time.Clock()





game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, screen)

game.init()

while game.run:
    dt = clock.tick(60) / 1000
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.run = False
    game.update(dt)
    game.draw()
    pg.display.flip()

pg.quit()



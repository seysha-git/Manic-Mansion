from settings import *
import pygame as pg
import random as rd

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height 

        self.objects = []
        self.saved_sheeps = []
        self.dangered_sheeps = []
        self.ghosts = []
        self.obstacles = []

        self.ghosts_count = 1
        self.obstacles_count = 3

        self.screen = pg.display.set_mode((self.width, self.height))
    def draw(self):
        self.screen.fill("dark blue")
        pg.draw.rect(self.screen, "grey", (0, 0, ZONES_WIDTH, WINDOW_HEIGHT))
        pg.draw.rect(self.screen, "silver", (WINDOW_WIDTH - ZONES_WIDTH, 0, ZONES_WIDTH, WINDOW_HEIGHT))
        for object in self.objects:
            object.draw(self.screen)
    def update(self, dt=1):
        while len(self.dangered_sheeps) < SHEEPS:
            collide = True
            while collide:
                x = rd.randint(WINDOW_WIDTH-ZONES_WIDTH, WINDOW_WIDTH - SHEEP_SIZE)
                #x = rd.randint(WINDOW_WIDTH-ZONES_WIDTH, WINDOW_WIDTH - 150)
                y = rd.randint(0, WINDOW_HEIGHT - SHEEP_SIZE)
                #y = rd.randint(0, 80)
                sheep = Sheep(x, y)
                collide = False
                for s in self.dangered_sheeps:
                    if(sheep.rect.colliderect(s.rect)):
                        collide = True
            self.addObjects(sheep)
            self.dangered_sheeps.append(sheep)
        
        while len(self.ghosts) < self.ghosts_count:
            collide = True
            while collide:
                x = rd.randint(ZONES_WIDTH + GHOST_SIZE, WINDOW_WIDTH - ZONES_WIDTH - GHOST_SIZE)
                #x = rd.randint(WINDOW_WIDTH-ZONES_WIDTH, WINDOW_WIDTH - 150)
                y = rd.randint(0, WINDOW_HEIGHT - GHOST_SIZE)
                #y = rd.randint(0, 80)
                new_ghost = Ghost(x, y)
                collide = False
                for g in self.ghosts:
                    if(new_ghost.rect.colliderect(g.rect)):
                        collide = True
            self.addObjects(new_ghost)
            self.ghosts.append(new_ghost)
        
        while len(self.obstacles) < self.obstacles_count:
            collide = True
            while collide:
                x = rd.randint(ZONES_WIDTH, WINDOW_WIDTH - ZONES_WIDTH - OBSTACLE_SIZE)
                #x = rd.randint(WINDOW_WIDTH-ZONES_WIDTH, WINDOW_WIDTH - 150)
                y = rd.randint(0, WINDOW_HEIGHT - OBSTACLE_SIZE)
                #y = rd.randint(0, 80)
                new_obst = Obstacle(x, y)
                collide = False
                for obst in self.obstacles:
                    if(new_obst.rect.colliderect(obst.rect)):
                        collide = True
            self.addObjects(new_obst)
            self.obstacles.append(new_obst)
        
        
        for object in self.objects:
            object.update(dt)
    def addObjects(self, object):
        self.objects.append(object)
    def removeObjects(self, object):
        self.objects.remove(object)

class gameObject(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pg.Vector2(x, y)
        self.width = 0
        self.height = 0
        self.color = " "
        self.type = " "
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.width, self.height)
    def place(self, x, y):
        self.x = x
        self.y = y
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
    def move(self, x, y):
        pass


class Human(gameObject):
    def __init__(self, x, y):
        gameObject.__init__(self, x, y)
        self.vx = HUMAN_VEL_X
        self.vy = HUMAN_VEL_Y
        self.width = HUMAN_SIZE
        self.height = HUMAN_SIZE
        self.points = 0
        self.color = HUMAN_COLOR
        self.carrySheep = False
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def move(self):
        pass
    def update(self, dt=1):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.rect.y > 0:
            self.pos.y -= self.vy*dt
        if keys[pg.K_s] and self.rect.y < WINDOW_HEIGHT - self.rect.height:
            self.pos.y += self.vy*dt
        if keys[pg.K_a] and self.rect.x > 0: #and self.x > 0:
            self.pos.x -= self.vx*dt
        if keys[pg.K_d] and self.rect.x < WINDOW_WIDTH - self.rect.width: #and self.x > WINDOW_WIDTH - self.width:
            self.pos.x += self.vx*dt
        
        self.rect.topleft = self.pos
        
    def decrease_speed(self):
        pass
    def increasePoint(self):
        pass
    def carrySheep(self):
        pass
    def checkColission():
        pass

class Ghost(gameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = GHOST_COLOR
        self.width = GHOST_SIZE
        self.height = GHOST_SIZE
        self.speed_vx = 200
        self.speed_vy = 200
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.width, self.height)
    def update(self, dt):
        self.rect.x +=  self.speed_vx * dt
        self.rect.y += self.speed_vy * dt

        if(self.rect.x + GHOST_SIZE > WINDOW_WIDTH - ZONES_WIDTH or
           self.rect.x < ZONES_WIDTH):
            self.speed_vx *= -1
        if(self.rect.y < 0 or self.rect.y + self.height > WINDOW_HEIGHT):
            self.speed_vy *= -1


class Obstacle(gameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = OBSTACLE_COLOR
        self.width = OBSTACLE_SIZE
        self.height = OBSTACLE_SIZE
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.width, self.height)

class Sheep(gameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = SHEEP_COLOR
        self.width = SHEEP_SIZE
        self.height = SHEEP_SIZE
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.width, self.height)
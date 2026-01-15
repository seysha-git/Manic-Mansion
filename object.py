from settings import *
import pygame as pg
import random as rd

class Game:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height 
        self.screen = screen

        self.objects = []
        self.saved_sheeps = []
        self.dangered_sheeps = []
        self.ghosts = []
        self.obstacles = []

        self.ghosts_count = 1
        self.obstacles_count = 3
        self.saved_sheeps_count = 0
        self.dangered_sheep_count = 3

        self.run = True

    def init(self):
        self.fonts = pg.font.get_fonts()
        self.system_font = pg.font.SysFont("arial", 40)

        self.system_font = self.system_font.render("Bring the sheeps home", True, "blue", "Silver")
        self.system_font_rect = self.system_font.get_rect()
        self.system_font_rect.center = (WINDOW_WIDTH/2, 40)

        self.bg = pg.image.load("images/22033.jpg")

        self.player = Human(WINDOW_WIDTH // 8, WINDOW_HEIGHT // 2)
        self.addObjects(self.player)

        
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        pg.draw.rect(self.screen, "dark blue", (0, 0, ZONES_WIDTH, WINDOW_HEIGHT))
        pg.draw.rect(self.screen, "light blue", (WINDOW_WIDTH - ZONES_WIDTH, 0, ZONES_WIDTH, WINDOW_HEIGHT))
        self.screen.blit(self.system_font, self.system_font_rect)
        for object in self.objects:
            object.draw(self.screen)

    def update(self, dt=1):
        while len(self.dangered_sheeps) < self.dangered_sheep_count:
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

        while len(self.saved_sheeps) < self.saved_sheeps_count:
            collide = True
            while collide:
                x = rd.randint(0, ZONES_WIDTH - GHOST_SIZE)
                #x = rd.randint(WINDOW_WIDTH-ZONES_WIDTH, WINDOW_WIDTH - 150)
                y = rd.randint(0, WINDOW_HEIGHT - GHOST_SIZE)
                #y = rd.randint(0, 80)
                new_sheep = Sheep(x, y)
                collide = False
                for s in self.saved_sheeps:
                    if(new_sheep.rect.colliderect(s.rect)):
                        collide = True
            self.addObjects(new_sheep)
            self.saved_sheeps.append(new_sheep)
        
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
        
        #automatic spawn obstacles
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
        
        #player and obstacle collision
        for obst in self.obstacles:
            collide = pg.Rect.colliderect(self.player.rect, obst.rect)
            overlap_x = min(self.player.rect.right, obst.rect.right) - max(self.player.rect.left, obst.rect.left)
            overlap_y = min(self.player.rect.bottom, obst.rect.bottom) - max(self.player.rect.top, obst.rect.top)
            if collide:
                if(overlap_x < overlap_y): #horisontal collision
                    if(self.player.rect.center[0] < obst.rect.center[0]):
                        self.player.place_x(obst.rect.left-self.player.rect.width)
                    if(self.player.rect.center[0] > obst.rect.center[0]):
                        self.player.rect.left = obst.rect.right
                        self.player.place_x(obst.rect.right)
                elif(overlap_y < overlap_x):
                     if(self.player.rect.center[1] < obst.rect.center[1]):
                        self.player.place_y(obst.rect.top - self.player.rect.height)
                     if(self.player.rect.center[1] > obst.rect.center[1]):
                         self.player.place_y(obst.rect.bottom)
                        
        for sheep in self.dangered_sheeps:
            if(pg.Rect.colliderect(self.player.rect, sheep.rect)):
                self.dangered_sheeps.remove(sheep)
                self.removeObjects(sheep)
                self.player.toggleSheep()
                self.saved_sheeps_count += 1
                self.dangered_sheep_count -= 1
                #self.removeObjects(sheep)
        
        if self.player.carrysheep and self.player.rect.left < ZONES_WIDTH:
            self.player.toggleSheep()
            self.dangered_sheep_count += 1
            self.ghosts_count += 1
            self.obstacles_count += 1
        
        for ghost in self.ghosts:
            if pg.Rect.colliderect(self.player.rect, ghost.rect):
                self.run = False

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
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.width, self.height)
    def place_x(self, x):
        self.pos.x = x
    def place_y(self, y):
        self.pos.y = y
    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)

class Human(gameObject):
    def __init__(self, x, y):
        gameObject.__init__(self, x, y)
        self.vx = HUMAN_VEL_X
        self.vy = HUMAN_VEL_Y
        self.width = HUMAN_SIZE
        self.height = HUMAN_SIZE
        self.points = 0
        self.color = HUMAN_COLOR
        self.carrysheep = False
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.width, self.height)

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
    def toggleSheep(self):
        if(self.carrysheep == False):
            self.carrysheep = True
            self.vx = HUMAN_VEL_X*0.5
            self.vy = HUMAN_VEL_Y*0.5
        else:
            self.carrysheep = False
            self.vx = HUMAN_VEL_X
            self.vy = HUMAN_VEL_Y

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
# Разработай свою игру в этом файле!
import pygame as pg
import time
import random


class GameSprite(pg.sprite.Sprite):
    def __init__(self, pic, w, h, x, y):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(pic), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def ris(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, pic, w, h, x, y, x_change=0, y_change=0):
        self.x_change = x_change
        self.y_change = y_change
        super().__init__(pic, w, h, x, y)
        self.image = [pg.transform.scale(pg.image.load(pic), (w, h)), pg.transform.flip(pg.transform.scale(pg.image.load(pic), (w, h)), 1, 0)]
        self.x = x
        self.y = y

    def ris(self):
        global photo
        if self.x_change < 0:
            photo = self.image[1]
        if self.x_change > 0:
            photo = self.image[0]
        screen.blit(photo, (self.rect.x, self.rect.y))

    def update(self):
        player.rect.x += self.x_change
        platform_touches = pg.sprite.spritecollide(player, barries, False)
        
        if self.x_change > 0:
            for p in platform_touches:
                self.rect.right = p.rect.left
        elif self.x_change < 0:
            for p in platform_touches:
                self.rect.left = p.rect.right

        player.rect.y += self.y_change
        platform_touches = pg.sprite.spritecollide(player, barries, False)
        if self.y_change > 0:
            for p in platform_touches:
                self.rect.bottom = p.rect.top
        elif self.y_change < 0:
            for p in platform_touches:
                self.rect.top = p.rect.bottom

class Enemy(GameSprite):
    def __init__(self, pic, w, h, x, y, speed, x2y2):
        self.speed = speed
        self.image = pic
        self.x1y1 = (x, y)
        self.x2y2 = x2y2
        self.direction = 'right'
        super().__init__(pic, w, h, x, y)
    def ris(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        if self.direction == "right":
            if self.rect.x < self.x2y2[0] and not self.rect.x == self.x2y2[0]:
                self.rect.x += self.speed
            else:
                self.direction = "left"
        if self.direction == "left":
            if self.rect.x > self.x1y1[0] and not self.rect.x == self.x1y1[0]:
                self.rect.x -= self.speed
            else:
                self.direction = "right"
        

#lib
WHITE = (250, 250, 250)

pg.init()
screen = pg.display.set_mode((1300, 800))
pg.display.set_caption("Chorus")
timer = pg.time.Clock()
bg = GameSprite("floor.jpg", 1300, 800, 0, 0)
player = Player("player.png", 100, 100, 450, 700)
End = GameSprite("finish.png", 100, 100, 1100, 700)
wall_picture = 'wall.jpg'
skrimer = GameSprite("skrimer.jpg", 1300, 800, 0, 0)
win = GameSprite("win.jpg", 1300, 800, 0, 0)
enemys = [
    Enemy("enemy.png", 100, 100, 700, 700, 5, (900, 700))
]
walls = [GameSprite(wall_picture, 30, 700, 600, 600),
    GameSprite(wall_picture, 700, 30, 200, 600),
    GameSprite(wall_picture, 500, 30, 0, 400),
    GameSprite(wall_picture, 30, 400, 670, 200),
    GameSprite(wall_picture, 800, 30, 200, 170),
    GameSprite(wall_picture, 400, 30, 900, 425)
   # GameSprite(wall_picture, 500, 50, 0, 200)
]
barries = pg.sprite.Group()
for wall in walls:
    barries.add(wall)
photo = player.image[0]
# game variales
FPS = 60
play = True
x_change = 0
y_change = 0
finish = False

def check_collide():
    global finish
    global player
    if pg.sprite.collide_rect(player , End):
        finish = True

    
    if player.rect.x < 0:
        player.rect.x = 0
    if player.rect.x > 1200:
        player.rect.x = 1200
    if player.rect.y < 0:
        player.rect.y = 0
    if player.rect.y > 700:
        player.rect.y = 700

while play:
    player.update()
    timer.tick(FPS)
    bg.ris()
    check_collide()

    barries.draw(screen)

    End.ris()
    player.ris()
    if finish:
        if random.random() > 0.7:
            kon = skrimer
        else:
            kon = win
        while finish:
            kon.ris()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finish = False
                    play = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        finish = False
            pg.display.flip()
        player = Player("player.png", 100, 100, 450, 700)
    for enemy in enemys:
        enemy.ris()
        enemy.update()



    for event in pg.event.get():
        if event.type == pg.QUIT:
            play = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                player.y_change = -5
            if event.key == pg.K_s:
                player.y_change = 5
            if event.key == pg.K_d:
                player.x_change = 5
            if event.key == pg.K_a:
                player.x_change = -5
            if event.key == pg.K_SPACE and finish:
                finish = False

        if event.type == pg.KEYUP:
            if event.key == pg.K_w or pg.K_s:
                player.y_change = 0
            if event.key == pg.K_a or pg.K_d:
                player.x_change = 0 




    pg.display.flip()
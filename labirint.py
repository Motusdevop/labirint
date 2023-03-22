# Разработай свою игру в этом файле!
import pygame as pg
import random

def restart():
    global player
    global enemys
    global monsters
    monsters = pg.sprite.Group()
    for enemy in enemys:
        monsters.add(enemy)
    player = Player("player.png", 100, 100, 450, 700)
    pg.mixer.music.play()
def check_finish():
    global play
    global finish
    global player
    if finish:
        pg.mixer.music.stop()
        if random.random() > 0.7:
            kon = skrimer
            sd_skrimer.play()
        else:
            kon = win
            sd_win.play()
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
        restart()

def check_die():
    global die
    global play
    global player
    if die:
        pg.mixer.music.stop()
        while die:
            DIE.ris()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    play = False
                    die = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        die = False
            pg.display.flip()
        restart()


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
        self.rg = True

    def ris(self):
        global photo
        if self.x_change < 0:
            photo = self.image[1]
            self.rg = False
        if self.x_change > 0:
            photo = self.image[0]
            self.rg = True
        screen.blit(photo, (self.rect.x, self.rect.y))

    def update(self):
        global sd_walk
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
    
    def fire(self):
        global bullets
        if self.rg:
            bullets.add(bullet(self.rect.right, self.rect.centery))
        else:
            bullets.add(bullet2(self.rect.left, self.rect.centery))
        sd_fire.play()

class Enemy(GameSprite):
    def __init__(self, pic, w, h, x, y, speed, x2y2):
        self.speed = speed
        self.image = pic
        self.x1y1 = (x, y)
        self.x2y2 = x2y2
        self.direction = 'right'
        self.direction2 = "down"
        super().__init__(pic, w, h, x, y)
    def ris(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        if self.direction == "right":
            if self.rect.x < self.x2y2[0] and self.rect.x != self.x2y2[0]:
                self.rect.x += self.speed
            else:
                self.direction = "left"
        if self.direction == "left":
            if self.rect.x > self.x1y1[0] and self.rect.x != self.x1y1[0]:
                self.rect.x -= self.speed
            else:
                self.direction = "right"
        if self.direction2 == "down":
            if self.rect.y < self.x2y2[1] and self.rect.y != self.x2y2[1]:
                self.rect.y += self.speed
            else:
                self.direction2 = "up"
        if self.direction2 == "up":
            if self.rect.y > self.x1y1[1] and self.rect.y != self.x1y1[1]:
                self.rect.y -= self.speed
            else:
                self.direction2 = "down"
        
        if pg.sprite.collide_rect(player, self):
            global die
            global sd_die
            die = True
            sd_die.play()

class bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load("bullet.png"), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.x += 20
        if self.rect.x > 1300:
                self.kill()
class bullet2(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.transform.flip(pg.transform.scale(pg.image.load("bullet.png"), (20, 20)), 1, 0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.rect.x -= 20
        if self.rect.x < 0:
                self.kill()



        

#lib

pg.init()

pg.mixer.init()
pg.mixer.music.load("Source/Sound/BG.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.5)

screen = pg.display.set_mode((1300, 800))
pg.display.set_caption("Chebubeli")
pg.display.set_icon(pg.image.load("Source/image/bullet.png"))
timer = pg.time.Clock()

bg = GameSprite("Source/image/floor.jpg", 1300, 800, 0, 0)
player = Player("Source/image/player.png", 100, 100, 450, 700)
End = GameSprite("Source/image/finish.png", 100, 100, 1100, 700)
DIE = GameSprite("Source/image/DIE.jpg", 1300, 800, 0, 0)
wall_picture = 'Source/image/wall.jpg'
skrimer = GameSprite("Source/image/skrimer.jpg", 1300, 800, 0, 0)
win = GameSprite("Source/image/win.jpg", 1300, 800, 0, 0)
enemys = [
    Enemy("Source/image/enemy.png", 100, 100, 700, 660, 5, (1100, 730)),
    Enemy("Source/image/enemy.png", 150, 150, 100, 20, 2, (1200, 25)),
    Enemy("Source/image/enemy.png", 100, 100, 40, 450, 7, (230, 500)),
    Enemy("Source/image/enemy.png", 100, 100, 520, 300, 5, (530, 500)),
    Enemy("Source/image/enemy.png", 100, 100, 900, 200, 7, (1100, 300))
]
monsters = pg.sprite.Group()
for enemy in enemys:
    monsters.add(enemy)
walls = [GameSprite(wall_picture, 30, 700, 600, 600),
    GameSprite(wall_picture, 700, 30, 200, 600),
    GameSprite(wall_picture, 500, 30, 0, 400),
    GameSprite(wall_picture, 30, 400, 670, 200),
    GameSprite(wall_picture, 800, 30, 200, 170),
    GameSprite(wall_picture, 400, 30, 900, 425),
    GameSprite(wall_picture, 230, 30, 1070, 625)
]

sd_win = pg.mixer.Sound("Source/Sound\win.wav")
sd_skrimer = pg.mixer.Sound("Source/Sound\skrim.wav")
sd_die = pg.mixer.Sound("Source/Sound\die.wav")
sd_fire = pg.mixer.Sound("Source/Sound/fire.wav")

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
die = False
bullets = pg.sprite.Group()

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
    barries.draw(screen)
    End.ris()
    player.ris()
    bullets.update()
    bullets.draw(screen)
    monsters.update()
    monsters.draw(screen)

    check_collide()
    pg.sprite.groupcollide(bullets, barries, True, False)
    pg.sprite.groupcollide(bullets, monsters, True, True)
    check_finish()
    check_die()

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

        if event.type == pg.MOUSEBUTTONDOWN:
            player.fire()




    pg.display.flip()
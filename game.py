from tkinter import HIDDEN
import pygame as py
import random as ra
import os
#初始化AND視窗
py.init()
py.mixer.init()
screen = py.display.set_mode((500,600))
py.display.set_caption("我他媽不會取名")
clock = py.time.Clock()
FPS=60

#載入圖片
background_img = py.image.load(os.path.join("img","background.png")).convert()
start_img = py.image.load(os.path.join("img","start.jpg")).convert()
player_img = py.image.load(os.path.join("img","player.png")).convert()
player_img.set_colorkey((0,0,0))
playerL_img = py.image.load(os.path.join("img","playerL.png")).convert()
playerL_img.set_colorkey((0,0,0))
RPG_bomb_img = py.image.load(os.path.join("img","RPG_bomb.png")).convert()
RPG_bomb_img.set_colorkey((0,0,0))
player_mini_img=py.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey((0,0,0))

py.display.set_icon(player_mini_img)

power_imgs={}
bullet_img = py.image.load(os.path.join("img","bullet1.png")).convert()
bullet_img.set_colorkey((0,0,0))
grenade_img = py.image.load(os.path.join("img","grenade.png")).convert()
grenade_img.set_colorkey((0,0,0))
seed_img = py.image.load(os.path.join("img","seed.png")).convert()
seed_img.set_colorkey((0,0,0))
RPG_img = py.image.load(os.path.join("img","RPG.png")).convert()
RPG_img.set_colorkey((0,0,0))
power_imgs["grenade"]=grenade_img
power_imgs["seed"]=seed_img
power_imgs["RPG"]=py.transform.scale(RPG_img,(35,50))

enemy_imgs = []
for i in range(4) :
    enemy_imgs.append(py.image.load(os.path.join("img",f"enemy{i}.png ")).convert())
expl_anim = {}
expl_anim["lg"] = []
expl_anim['sm'] = []
expl_anim['bm'] = []
for i in range(9):
    expl_img= py.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey((0,0,0))
    expl_anim["lg"].append(py.transform.scale(expl_img,(75,75)))
    expl_anim["sm"].append(py.transform.scale(expl_img,(30,30)))
    expl_anim["bm"].append(py.transform.scale(expl_img,(150,150)))

font_name = os.path.join("font.ttf")

def new_rock() :
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):
    if hp < 0 :
        hp=0
    BAR_LENGTH =100
    BAR_HEIGTH =10
    fill =(hp/100)*BAR_LENGTH
    outline_rect = py.Rect(x,y,BAR_LENGTH,BAR_HEIGTH)
    fill_rect = py.Rect(x,y,fill,BAR_HEIGTH)
    py.draw.rect(surf,(128,0,128),fill_rect)
    py.draw.rect(surf,(255,255,255),outline_rect,2)

def draw_picture(picture,surf, x, y):
    img_rect=picture.get_rect()
    img_rect.x=x
    img_rect.y=y
    surf.blit(py.transform.scale(picture,(25,25)),img_rect)

def draw_lives(surf, lives,img,x,y):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        surf.blit(img, img_rect)

def draw_text(surf,text,size,x,y,color): #寫入的平面、寫入之文字、XY
    font = py.font.Font(font_name, size)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_init():
    screen.blit(py.transform.scale(start_img,(500,600)),(0,0))
    draw_text(screen,"← →左右移動/空白鍵發射子彈",22,250,10,(0,0,0))
    draw_text(screen,"A丟手榴彈/S設置飛彈",22,250,40,(0,0,0))
    draw_text(screen,'按任意鍵開始遊戲',18,250,270,(0,0,0))
    py.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
    #取得輸入
        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                return True
            elif event.type == py.KEYUP :
                waiting=False
                return False
#載入音樂
shoot_sound=py.mixer.Sound(os.path.join("img","shoot3.mp3"))
hurt_sound=py.mixer.Sound(os.path.join("img","hurt1.mp3"))
died_sound=py.mixer.Sound(os.path.join("img","died.mp3"))
kill_sound=py.mixer.Sound(os.path.join("img","kill2.mp3"))
recover_sound=py.mixer.Sound(os.path.join("img","pow1.wav"))

py.mixer.music.load(os.path.join("img","bgm1.mp3"))
py.mixer.music.set_volume(0.3)

#遊戲物件
class Bullet(py.sprite.Sprite) :
    def __init__(self,x,y) :
        py.sprite.Sprite.__init__(self)
        self.image = py.transform.scale(bullet_img,(13,40))
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=y
        self.speed=20
    def update(self) :
        self.rect.bottom-=10
        if self.rect.bottom<0 :
            self.kill()

class Grenade(py.sprite.Sprite) :
    def __init__(self,x,y) :
        py.sprite.Sprite.__init__(self)
        self.image_ori = py.transform.scale(grenade_img,(50,45))
        self.image_ori.set_colorkey((0,0,0))
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=y
        self.speed=-12
        self.total_degree = 0
        self.rot_degree = 35
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = py.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    def update(self) :
        self.rotate()
        if self.rect.centery>150 :
            self.rect.centery+=self.speed
        else :
            bomb=Explosion(self.rect.center,"bm")
            all_sprites.add(bomb)
            bombs.add(bomb)
            self.rect.center=(10000,10000)
            if not(bomb.alive()):
                self.kill()

class RPG(py.sprite.Sprite) :
    def __init__(self,x) :
        py.sprite.Sprite.__init__(self)
        self.image = RPG_img
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=550
        self.speed=6
        self.times=3
        self.delay=py.time.get_ticks()
    def update(self) :
        now=py.time.get_ticks()
        if self.rect.bottom<595 :
            self.rect.bottom+=self.speed
        else :
            if self.times>0 :
                if now - self.delay>3000:
                    self.delay=py.time.get_ticks()
                    a=RPG_bomb(self.rect.centerx,self.rect.top)
                    all_sprites.add(a)
                    self.times-=1
            else :
                self.kill()

class RPG_bomb(py.sprite.Sprite) :
    def __init__(self,x,y) :
        py.sprite.Sprite.__init__(self)
        self.image = RPG_bomb_img
        self.rect = self.image.get_rect()
        self.rect.centerx=x
        self.rect.bottom=y
        self.speed=-9
    def update(self) :
        if self.rect.centery>ra.randrange(50,250) :
            self.rect.centery+=self.speed
        else :
            bomb=Explosion(self.rect.center,"bm")
            all_sprites.add(bomb)
            bombs.add(bomb)
            self.rect.center=(10000,10000)
            if not(bomb.alive()):
                self.kill()

class Power(py.sprite.Sprite) :
    def __init__(self,center) :
        py.sprite.Sprite.__init__(self)
        self.type = ra.choice(["grenade","seed","RPG"])
        self.image = power_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy= 3
    def update(self) :
        self.rect.y+=self.speedy
        if self.rect.bottom<0 :
            self.kill()

class Explosion(py.sprite.Sprite) :
    def __init__(self,center,size) :
        py.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = py.time.get_ticks()
        self.frame_rate=50
    def update(self) :
        now=py.time.get_ticks()
        if now - self.last_update >self.frame_rate:
            self.last_update = now
            self.frame+=1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else :
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center =center

class Player(py.sprite.Sprite) :
    def __init__(self) :
        py.sprite.Sprite.__init__(self)
        self.image = py.transform.scale(player_img,(60,70))
        self.rect = self.image.get_rect()
        self.radius = 33
        #py.draw.circle(self.image,(10,10,10),self.rect.center,self.radius)
        self.rect.centerx=250
        self.rect.bottom=590
        self.speed=8
        self.health=100
        self.lives=3
        self.hidden=False
        self.hide_time= 0
        self.grenade_num=2
        self.RPG_num=2
        self.grenade_time=py.time.get_ticks()
        self.RPG_time=py.time.get_ticks()
    def update(self) :
        now=py.time.get_ticks()
        key_pressed = py.key.get_pressed()
        if key_pressed[py.K_RIGHT] and self.rect.right<500:
            self.rect.x +=self.speed
            self.image=py.transform.scale(player_img,(60,70))
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center =center
        if key_pressed[py.K_LEFT] and self.rect.left>0:
            self.rect.x -=self.speed
            self.image=py.transform.scale(playerL_img,(60,70))
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center =center
        if key_pressed[py.K_a] and now-self.grenade_time>300:
            self.grenade_time=now
            self.throw()
        if key_pressed[py.K_s] and now-self.RPG_time>300:
            self.RPG_time=now
            self.set()
        if self.rect.right>500 :
            self.rect.right=500
        if self.rect.left<0 :
            self.rect.left=0
        if self.hidden and py.time.get_ticks()-self.hide_time>1000 :
            self.hidden= False
            self.rect.centerx=250
            self.rect.bottom=590
    def throw(self):
        if not(self.hidden):
            if self.grenade_num>0 and not(self.hidden):
                self.grenade_num-=1
                grenade= Grenade(self.rect.centerx,self.rect.top)
                all_sprites.add(grenade)
                grenades.add(grenade)
    def set(self):
        if not(self.hidden):
            if self.RPG_num>0:
                self.RPG_num-=1
                R=RPG(self.rect.centerx)
                all_sprites.add(R)
    def shoot(self):
        if not(self.hidden):
            bullet = Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
    def hide(self):
        self.hidden=True
        self.hide_time = py.time.get_ticks()
        self.rect.center=(1000,1000)

class Rock(py.sprite.Sprite) :
    def __init__(self) :
        py.sprite.Sprite.__init__(self)
        self.image_ori = ra.choice(enemy_imgs)
        self.image_ori.set_colorkey((0,0,0))
        self.image = self.image_ori.copy()
        self.rect =self.image.get_rect()
        self.radius = self.rect.width*0.85/2
        #py.draw.circle(self.image,(10,10,10),self.rect.center,self.radius)
        self.rect.x=ra.randrange(0,500)
        self.rect.y=ra.randrange(-150,-100)
        self.xspeed=ra.randrange(-3,3)
        self.yspeed=ra.randrange(1,8)
        self.total_degree = 0
        self.rot_degree = ra.randrange(-3,3)
    def stop(self):
        self.xpeed=0
        self.yspeed=0
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = py.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    def update(self) :
        self.rotate()
        self.rect.x+=self.xspeed
        self.rect.y+=self.yspeed
        if self.rect.top>600 or self.rect.right<0 or self.rect.left>500 :
            self.rect.x=ra.randrange(0,500)
            self.rect.y=0
            self.xspeed=ra.randrange(-3,3)
            self.yspeed=ra.randrange(1,10)           
#群組    
all_sprites = py.sprite.Group()
rocks = py.sprite.Group()
bullets = py.sprite.Group()
powers = py.sprite.Group()
grenades = py.sprite.Group()
bombs = py.sprite.Group()
player=Player()
for i in range(8) :
    new_rock()
all_sprites.add(player)
score = 0
probability=0.1
py.mixer.music.play(-1) #變數表示撥放次數(-1為無限撥放)
#遊戲迴圈
show_init =True
run=True
while run :
    if show_init:
        close=draw_init()
        if close:
            break
        show_init=False
        all_sprites = py.sprite.Group()
        rocks = py.sprite.Group()
        bullets = py.sprite.Group()
        powers = py.sprite.Group()
        grenades = py.sprite.Group()
        bombs = py.sprite.Group()
        player=Player()
        for i in range(8) :
            new_rock()
        all_sprites.add(player)
        score = 0
    
    clock.tick(FPS)
    #取得輸入
    for event in py.event.get():
        if event.type == py.QUIT:
            run=False
        elif event.type == py.KEYDOWN :
            if event.key == py.K_SPACE :
                player.shoot()

    #更新遊戲
    all_sprites.update()
    hits = py.sprite.groupcollide(rocks, bullets, True, True) #回傳字典{子彈(key):石頭(value)}
    for hit in hits:
        kill_sound.play()
        score +=int(hit.radius)
        expl = Explosion(hit.rect.center,"lg")
        all_sprites.add(expl)
        if ra.random() <probability:
            pow=Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    hits = py.sprite.groupcollide(rocks, grenades, True, True)
    for hit in hits:
        kill_sound.play()
        score +=int(hit.radius)
        expl = Explosion(hit.rect.center,"bm")
        bombs.add(expl)
        all_sprites.add(expl)
        if ra.random() <probability:
            pow=Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    hits = py.sprite.groupcollide(rocks,bombs, True, False)
    for hit in hits:
        kill_sound.play()
        score +=int(hit.radius)
        expl = Explosion(hit.rect.center,"lg")
        all_sprites.add(expl)
        if ra.random() <probability:
            pow=Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()
    hits = py.sprite.spritecollide(player, powers, True)
    for hit in hits :
        recover_sound.play()
        if hit.type =="seed" :
            player.health+=20
            if player.health>100:
                player.health=100
        if hit.type =="grenade" :
            player.grenade_num+=1
        if hit.type=="RPG" :
            player.RPG_num+=1
        
    hits = py.sprite.spritecollide(player, rocks, True, py.sprite.collide_circle)
    for hit in hits :
        if player.health>0 :
            hurt_sound.play()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center,"sm")
        all_sprites.add(expl)
        new_rock()
        if player.health<=0 :
            died_sound.play()
            die = Explosion(player.rect.center,"lg")
            all_sprites.add(die)
            player.lives-=1
            if player.lives >0 :
                player.health=100
            player.hide()
    if player.lives==0 and not(die.alive()):
        show_init=True
    #圖示
    screen.fill((0,0,0))
    screen.blit(py.transform.scale(background_img,(500,600)),(0,0))
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,250,10,(255,255,255))

    draw_text(screen,str(player.grenade_num),18,455,48,(0,0,0))
    draw_text(screen,"x",18,435,48,(0,0,0))
    draw_picture(grenade_img,screen,400,48)

    draw_text(screen,str(player.RPG_num),18,455,78,(0,0,0))
    draw_text(screen,"x",18,435,78,(0,0,0))
    draw_picture(RPG_img,screen,400,78)

    draw_health(screen,player.health,8,15)
    draw_lives(screen,player.lives,player_mini_img,400,15)
    py.display.update()

py.quit()
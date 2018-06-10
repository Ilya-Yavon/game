import pygame
from pygame import *

#Характеристики персонажа
SPEED = 20
WIDTH = 22
HEIGHT = 32
COLOR =  "#000000"

JUMP_POWER = 15
GRAVITY = 1.5

#Характеристики стен
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#800000"

#Характеристики фона
window_w = 800
window_h = 640
display = (window_w, window_h)
bg_color = "#696969"

#Основная функция
def main():
    pygame.init()
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("Square")
    bg = Surface((window_w, window_h))

    #Движение персонажа
    class character(sprite.Sprite):
        def __init__(self, x, y):
            sprite.Sprite.__init__(self)
            self.xvel = 0
            self.yvel = 0
            self.startX = x
            self.startY = y
            self.image = Surface((WIDTH,HEIGHT))
            self.image.fill(Color(COLOR))
            self.rect = Rect(x, y, WIDTH, HEIGHT)
            self.onGround = False

        def update(self, left, right, space):
            if space:
                if self.onGround:
                    self.yvel = -JUMP_POWER

            #if up:
                #self.yvel = -SPEED

            #if down:
                #self.yvel = SPEED

            if left:
                self.xvel = -SPEED

            if right:
                self.xvel = SPEED

            if not(left or right):
                self.xvel = 0

            #if not(up or down):
                #self.yvel = 0

            if not self.onGround:
                self.yvel +=  GRAVITY

            self.onGround = False;   

            self.rect.y += self.yvel
            self.collide(0, self.yvel, platforms)

            self.rect.x += self.xvel
            self.collide(self.xvel, 0, platforms)


        def collide(self, xvel, yvel, platforms):
            for p in platforms:
                if sprite.collide_rect(self, p):

                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0


    hero = character(55,55)
    left = right = False
    #up = down = False
    space = False


    entities = pygame.sprite.Group()
    platforms = []
    entities.add(hero)

    #Платформы
    class Platform(sprite.Sprite):
        def __init__(self, x, y):
            sprite.Sprite.__init__(self)
            self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image.fill(Color(PLATFORM_COLOR))
            self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


    #Камера        
    class Camera(object):
        def __init__(self, camera_func, width, height):
            self.camera_func = camera_func
            self.state = Rect(0, 0, width, height)
        
        def apply(self, target):
            return target.rect.move(self.state.topleft)

        def update(self, target):
            self.state = self.camera_func(self.state, target.rect)

    def camera_configure(camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l+window_w / 2, -t+window_h / 2
        l = min(0, l)
        l = max(-(camera.width-window_w), l)
        t = max(-(camera.height-window_h), t)
        t = min(0, t)
        return Rect(l, t, w, h) 


    #Уровень
    level = [
       "----------------------------------",
       "-                                -",
       "-                       --       -",
       "-                                -",
       "-            --                  -",
       "-                                -",
       "--                               -",
       "-                                -",
       "-                   ----     --- -",
       "-                                -",
       "--                              --",
       "-                                -",
       "-                            --- -",
       "-              --                -",
       "-                                -",
       "-      ---                       -",
       "-                                -",
       "-   -------         ----         -",
       "-                                -",
       "-                         -      -",
       "-                            --  -",
       "-                                -",
       "-                                -",
       "----------------------------------"]

    total_level_width  = len(level[0])*PLATFORM_WIDTH
    total_level_height = len(level)*PLATFORM_HEIGHT
    camera = Camera(camera_configure, total_level_width, total_level_height)

    timer = pygame.time.Clock()

    bg.fill(Color(bg_color))
    #Основной цикл
    while 1:
        timer.tick(60)
        #Назнаяения клавиш
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            #if e.type == KEYDOWN and e.key == K_UP:
                #up = True
            #if e.type == KEYDOWN and e.key == K_DOWN:
                #down = True
            #if e.type == KEYUP and e.key == K_UP:
                #up = False
            #if e.type == KEYUP and e.key == K_DOWN:
                #down = False
            if e.type == KEYDOWN and e.key == K_SPACE:
                space = True
            if e.type == KEYUP and e.key == K_SPACE:
                space = False

        screen.blit(bg, (0,0))
        hero.update(left, right, space)
        camera.update(hero)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        
        x=y=0
        for row in level:
            for col in row:
                if col == "-":
                    pf = Platform(x,y)
                    entities.add(pf)
                    platforms.append(pf)

                    
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0


        pygame.display.update()


if __name__ == "__main__":
    main()
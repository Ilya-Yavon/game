#Моули
import pygame
from pygame import Surface, mixer, Color, Rect, QUIT, KEYDOWN, K_LEFT, K_RIGHT, KEYUP, K_SPACE
import pyganim
import random

#Звук
mixer.pre_init(44100, -16, 1, 512)
mixer.init()
music = pygame.mixer.Sound('C:/project/music.wav')
music.play(-1)

#Характеристики персонажа
SPEED = 6
WIDTH = 22
HEIGHT = 30
COLOR =  "#00FFFF"
JUMP_POWER = 10

GRAVITY = 0.5

#Анимация
ANIMATION_DELAY = 1
ANIMATION_RIGHT = [('C:/project/hero_right1.png'),
            ('C:/project/hero_right1.png'),
            ('C:/project/hero_right1.png'),
            ('C:/project/hero_right1.png'),
            ('C:/project/hero_right2.png'),
            ('C:/project/hero_right2.png'),
            ('C:/project/hero_right2.png'),
            ('C:/project/hero_right2.png'),
            ('C:/project/hero_right3.png'),
            ('C:/project/hero_right3.png'),
            ('C:/project/hero_right3.png'),
            ('C:/project/hero_right3.png'),
            ('C:/project/hero_right2.png'),
            ('C:/project/hero_right2.png'),
            ('C:/project/hero_right2.png'),
            ('C:/project/hero_right2.png')]
ANIMATION_LEFT = [('C:/project/hero_left1.png'),
            ('C:/project/hero_left1.png'),
            ('C:/project/hero_left1.png'),
            ('C:/project/hero_left1.png'),
            ('C:/project/hero_left2.png'),
            ('C:/project/hero_left2.png'),
            ('C:/project/hero_left2.png'),
            ('C:/project/hero_left2.png'),
            ('C:/project/hero_left3.png'),
            ('C:/project/hero_left3.png'),
            ('C:/project/hero_left3.png'),
            ('C:/project/hero_left3.png'),
            ('C:/project/hero_left2.png'),
            ('C:/project/hero_left2.png'),
            ('C:/project/hero_left2.png'),
            ('C:/project/hero_left2.png')]
ANIMATION_STAY = [('C:/project/hero.png', 1)]
ANIMATION_JUMP_LEFT = [('C:/project/hero_left3.png', 1)]
ANIMATION_JUMP_RIGHT = [('C:/project/hero_right3.png', 1)]

# ANIMATION_MONSTER = [('C:/project/monster1.png'),
#                 ('C:/project/monster1.png'),
#                 ('C:/project/monster1.png'),
#                 ('C:/project/monster1.png'),
#                 ('C:/project/monster2.png'),
#                 ('C:/project/monster2.png'),
#                 ('C:/project/monster2.png'),
#                 ('C:/project/monster2.png')]

#Характеристики монстров
monster_speed = 3
monster_width = 44
monster_height = 24
monster_color = "#000000"

#Характеристики платформ
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#858872"
platform_texture = pygame.image.load('C:/project/platform.png')

#Характеристики монет
coin_width = 15
coin_height = 15
coin_color = "#FFFF00"
coin_texture = pygame.image.load('C:/project/coin.png')

#Характеристики фона
window_w = 800
window_h = 640
display = (window_w, window_h)
bg_color = "#303030"

#Счет
pygame.init()
font = pygame.font.SysFont(None, 38)
coin_s = pygame.image.load('C:/project/coin_s.png')
heart = pygame.image.load('C:/project/heart.png')


#Объекты
class Objects(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.startX = x
        self.startY = y
        self.onGround = False

    #Движение объектов
    def update(self, left, right, map):
        if not self.onGround:
            self.yvel +=  GRAVITY

        self.onGround = False;

        self.rect.y += self.yvel
        self.collide(0, self.yvel, map)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, map)

        if map.state > Rect(0, -100, 800, 704) and map.state != Rect(0, 0, 800, 896):
            self.rect.y += 3*PLATFORM_HEIGHT

    #Столкновение с платформами
    def collide(self, xvel, yvel, map):
        for p in map.platforms:
            if pygame.sprite.collide_rect(self, p):

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


#Монстр
class Monster(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = Surface((monster_width, monster_height))
        self.image.set_colorkey(Color(COLOR))
        self.image = pygame.image.load('C:/project/monster.png')
        self.rect = Rect(x, y, monster_width, monster_height)
        #
        # boltAnim = []
        # for anim in ANIMATION_MONSTER:
        #    boltAnim.append((anim, ANIMATION_DELAY))
        # self.boltAnimMonster = pyganim.PygAnimation(boltAnim)
        # self.boltAnimMonster.play()

    #Движение монстра
    def update(self, left, right, map):
        if left:
            self.xvel = -monster_speed
            # self.boltAnimMonster.blit(self.image, (0, 0))

        if right:
            self.xvel = monster_speed
            # self.boltAnimMonster.blit(self.image, (0, 0))

        if not(left or right):
            self.xvel = 0

        super().update(left, right, map)

        if self.rect.y > 862:
            self.rect.y -= 27*PLATFORM_HEIGHT
            self.rect.x == random.randint(32, 724)


#Персонаж
class Character(Objects):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sound_play = True
        self.life = 3
        self.score = 0
        self.score2 = 0
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)
        #Анимация
        self.image.set_colorkey(Color(COLOR))
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))
        #Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
           boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #Анимация движения влево        
        boltAnim = []
        for anim in ANIMATION_LEFT:
           boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        #Анимация движения в прыжке
        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        #Звуки
        self.jump_sound = mixer.Sound('C:/project/jump.wav')
        self.game_over_sound = mixer.Sound('C:/project/game_over.wav')
        self.coin_sound = mixer.Sound('C:/project/coin.wav')
        self.monster_kill = mixer.Sound('C:/project/monster_kill.wav')
        self.life_sound = mixer.Sound('C:/project/life.wav')
        self.heart_sound = mixer.Sound('C:/project/heart.wav')

    #Движение персонажа
    def update(self, left, right, space, map):
        if space:
            if self.onGround:
                self.yvel = -JUMP_POWER
                self.jump_sound.play()

        #if up:
            #self.yvel = -SPEED

        #if down:
            #self.yvel = SPEED

        if left:
            self.xvel = -SPEED
            self.image.fill(Color(COLOR))
            if space:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = SPEED
            self.image.fill(Color(COLOR))
            if space:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not(left or right):
            self.xvel = 0
            self.image.fill(Color(COLOR))
            self.boltAnimStay.blit(self.image, (0, 0))

        #if not(up or down):
            #self.yvel = 0

        super().update(left, right, map)

        if self.rect.y > 1000:
            music.stop()
            map.level = ["                         ",
"                         ", "                         ",
"                         ", "                         ",
"                         ", "                         ",
"                         ", "                         ",
                       "-------------------------",
                       "-                       -",
                       "-                       -",
                       "- ----- ---- ----- ---- -",
                       "- -     -  - - - - -    -",
                       "- -  -- ---- - - - ---  -",
                       "- -   - -  - - - - -    -",
                       "- ----- -  - - - - ---- -",
                       "-                       -",
                       "-                       -",
                       "-                       -",
                       "- ---- -  - ---- ---- - -",
                       "- -  - -  - -    -  - - -",
                       "- -  - -  - ---  ---  - -",
                       "- -  - -  - -    -  -   -",
                       "- ----  --  ---- -  - - -",
                       "-                       -",
                       "-                       -",
                       "-------------------------"]
        if self.rect.y > 1000:
            if self.sound_play == True:
                self.game_over_sound.play()
                self.sound_play = False
        if self.rect.y > 40000:
            raise SystemExit

    #Подбор монет и взаимодействие с монстром
    def collide(self, xvel, yvel, map):
        super().collide(xvel, yvel, map)
        for c in map.coins:
            number_of_line = c.rect.y // PLATFORM_HEIGHT
            coordinate_y = number_of_line * PLATFORM_HEIGHT
            number_of_column = c.rect.x // PLATFORM_WIDTH
            coordinate_x = number_of_column * PLATFORM_WIDTH
            if pygame.sprite.collide_rect(self, c):
                if c.rect.y > coordinate_y:
                    record = map.level.pop(number_of_line)
                    if c.rect.x > coordinate_x:
                        record = record[:number_of_column] + ' ' + record[(number_of_column+1):]
                        self.coin_sound.play()
                map.level.insert(number_of_line, record)
                self.score += 1

        for m in map.villain:
            if pygame.sprite.collide_rect(self, m):
                if self.rect.bottom <= m.rect.top + 9:
                    self.yvel = -5
                    m.rect.y -= 27*PLATFORM_HEIGHT
                    m.rect.x == random.randint(32, 724)
                    self.monster_kill.play()
                    self.score2 += 1
                else:
                    self.life -= 1
                    m.rect.y -= 27*PLATFORM_HEIGHT
                    m.rect.x == random.randint(32, 724)
                    if self.life > 0:
                        self.life_sound.play()
                if self.life == 0:
                    self.rect.y = 1000
                if self.score2 == 10:
                    self.life += 1
                    self.heart_sound.play()
                    self.score2 = 0


#Платформа
class Platform(pygame.sprite.Sprite):
    image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
    image.set_colorkey(Color(COLOR))
    image = platform_texture
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


#Монетка
class Coin(pygame.sprite.Sprite):
    image = Surface((coin_width, coin_height))
    image.set_colorkey(Color(COLOR))
    image = coin_texture
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x, y, coin_width, coin_height)     


#Камера        
class Map(object):
    def __init__(self):
        #Уровень
        self.level = []
        for vertical in range(9):
            number = '-'
            horizontal = 75
            while len(number) < horizontal:
                platform_lenght = random.choice(['--', '---'])
                spaces = random.choice(['  ', '   ', '    '])
                number = random.choice([number + platform_lenght + spaces, number + spaces + platform_lenght])
            while len(number) > horizontal - 3:
                number = number[:-1]
            while len(number) > horizontal - 52:
                number = number[1:]
            number = '-' + number
            number = number + '-'
            self.level.append(number)
            self.level.append('-                       -')
            line = '-'
            while len(line) != 24:
                if random.random() > 0.022:
                    line += ' '
                else:
                    line += '*'
            line += '-'
            self.level.append(line)
        self.level.append('-------------------------')

        width  = len(self.level[0])*PLATFORM_WIDTH
        height = len(self.level)*PLATFORM_HEIGHT

        self.state = Rect(0, 0, width, height)

        self.entities = pygame.sprite.Group()
        self.platforms = []
        self.coins = []
        self.villain = []
        for i in range(4):
            self.villain.append(Monster(random.randint(32, 724), random.randint(32, 672)))
    
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    #Генерация уровня
    def update(self, target):
        self.state = self.camera_configure(self.state, target.rect)
        limit = -100
        if self.state > Rect(0, limit, 800, 896):
            number = '-'
            horizontal = 75
            while len(number) < horizontal:
                platform_lenght = random.choice(['--', '---'])
                spaces = random.choice(['  ', '   ', '    '])
                number = random.choice([number + platform_lenght + spaces, number + spaces + platform_lenght])
            while len(number) > horizontal - 3:
                number = number[:-1]
            while len(number) > horizontal - 52:
                number = number[1:]
            number = '-' + number + '-'
            line = '-'
            while len(line) != 24:
                if random.random() > 0.022:
                    line += ' '
                else:
                    line += '*'
            line += '-'
            self.level.insert(0, line)
            self.level.insert(0, '-                       -')
            self.level.insert(0, number)
        while(len(self.level)) > 28:
            self.level.pop()

        self.entities = pygame.sprite.Group()
        self.platforms = []
        self.coins = []
        self.entities.add(target)
        self.entities.add(self.villain)

        x = y = 0
        w = 0
        h = coin_height / 2

        for row in self.level:
            for col in row:
                if col == "-":
                    pf = Platform(x,y)
                    self.entities.add(pf)
                    self.platforms.append(pf)
                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0
        
        for row in self.level:
            for col in row: 
                if col == "*":
                    cn = Coin(w,h)
                    self.entities.add(cn)
                    self.coins.append(cn)
                w += PLATFORM_WIDTH
            h += PLATFORM_HEIGHT
            w = coin_width / 2


    #Настройка размера камеры
    def camera_configure(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l+window_w / 2, -t+window_h / 2
        l = min(0, l)
        l = max(-(camera.width-window_w), l)
        t = max(-(camera.height-window_h), t)
        t = min(0, t)
        return Rect(l, t, w, h)

#Основная функция
def main():
    pygame.init()
    screen = pygame.display.set_mode(display)
    pygame.display.set_caption("Game")
    bg = Surface((window_w, window_h))
    header = Surface((window_w, window_h / 16))


    hero = Character(50, 840)
    camera = Map()
    camera.entities.add(hero)
    space = left = right = False
    m_left = []
    m_right = []
    for i in range(len(camera.villain)):
        m_left.append(False)
        m_right.append(False)
    #up = down = False


    timer = pygame.time.Clock()


    bg.fill(Color(bg_color))
    header.fill(Color('#202020'))
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
        
        #Логика движения монстров
        def monster_motion(i):
            number_of_line = camera.villain[i].rect.y // PLATFORM_HEIGHT
            number_of_column1 = (camera.villain[i].rect.x + monster_width) // PLATFORM_WIDTH
            number_of_column2 = camera.villain[i].rect.x // PLATFORM_WIDTH
            number_of_column3 = (camera.villain[i].rect.x + PLATFORM_HEIGHT-1) // PLATFORM_WIDTH
            record1 = camera.level[number_of_line+1]
            record2 = camera.level[number_of_line]
            try:
                if record1[number_of_column1] == '-' and m_left[i] == False and record2[number_of_column1] != '-':
                    m_right[i] = True
                else:
                    m_right[i] = False
                if record1[number_of_column2] == '-' and m_right[i] == False and record2[number_of_column3-1] != '-':
                    m_left[i] = True
                else:
                    m_left[i] = False
            except IndexError:
                nothing = 0
            return m_left[i], m_right[i]
        m_left0, m_right0 = monster_motion(0)
        m_left1, m_right1 = monster_motion(1)
        m_left2, m_right2 = monster_motion(2)
        m_left3, m_right3 = monster_motion(3)


        #Блитирование и обновление объектов
        text = font.render('Score: ' + str(hero.score), True, (225, 225, 225))
        text2 = font.render('x' + str(hero.life), True, (225, 225, 225))
        screen.blit(bg, (0,0))
        hero.update(left, right, space, camera)
        camera.villain[0].update(m_left0, m_right0, camera)
        camera.villain[1].update(m_left1, m_right1, camera)
        camera.villain[2].update(m_left2, m_right2, camera)
        camera.villain[3].update(m_left3, m_right3, camera)
        camera.update(hero)
        for e in camera.entities:
            screen.blit(e.image, camera.apply(e))
        screen.blit(header, (0, 0))
        screen.blit(coin_s, (40, 5))
        if 4 > hero.life > 2:
            screen.blit(heart, (730, 8))
        if 4 > hero.life > 1:
            screen.blit(heart, (700, 8))
        if 4 > hero.life > 0:
            screen.blit(heart, (670, 8))
        if hero.life > 3:
            screen.blit(heart, (700, 8))
            screen.blit(text2, (730, 9))
        screen.blit(text, (80, 9))
        pygame.display.update()


if __name__ == "__main__":
    main()
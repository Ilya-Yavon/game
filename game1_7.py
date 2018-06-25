import pygame
from pygame import *
import random

#Характеристики персонажа
SPEED = 7
WIDTH = 22
HEIGHT = 32
COLOR =  "#00FFFF"

JUMP_POWER = 10
GRAVITY = 0.5

#Характеристики платформ
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#858872"

#Характеристики монет
coin_width = 15
coin_height = 20
coin_color = "#FFFF00"

#Характеристики фона
window_w = 800
window_h = 640
display = (window_w, window_h)
bg_color = "#303030"


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


	def update(self, left, right, space, map):
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
		self.collide(0, self.yvel, map)

		self.rect.x += self.xvel
		self.collide(self.xvel, 0, map)

		limit = -100
		if map.state > Rect(0, limit, 800, 704) and map.state != Rect(0, 0, 800, 896):
			self.rect.y += 3*PLATFORM_HEIGHT


	def collide(self, xvel, yvel, map):
		for p in map.platforms:
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


#Платформа
class Platform(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
		self.image.fill(Color(PLATFORM_COLOR))
		self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


#Монетка
class Coin(sprite.Sprite):
	def __init__(self, x, y):
		sprite.Sprite.__init__(self)
		self.image = Surface((coin_width, coin_height))
		self.image.fill(Color(coin_color))
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
				line += random.choice([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*'])
			line += '-'
			self.level.append(line)
		self.level.append('-------------------------')

		width  = len(self.level[0])*PLATFORM_WIDTH
		height = len(self.level)*PLATFORM_HEIGHT

		self.state = Rect(0, 0, width, height)

		self.entities = pygame.sprite.Group()
		self.platforms = []
		self.coins = []
	
	def apply(self, target):
		return target.rect.move(self.state.topleft)

	def update(self, target):
		self.state = self.camera_configure(self.state, target.rect)
		#Генерация уровня
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
				line += random.choice([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*'])
			line += '-'
			self.level.insert(0, line)
			self.level.insert(0, '-                       -')
			self.level.insert(0, number)
		while(len(self.level)) > 30:
			self.level.pop()

		self.entities = pygame.sprite.Group()
		self.platforms = []
		self.coins = []
		self.entities.add(target)

		x=y=0
		w=h=0

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
				w += 17 + coin_width
			h += 12 + coin_height
			w = 8.5


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
	pygame.display.set_caption("Square")
	bg = Surface((window_w, window_h))


	hero = character(50,840)
	left = right = False
	#up = down = False
	space = False

	
	camera = Map()
	camera.entities.add(hero)


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
		hero.update(left, right, space, camera)
		camera.update(hero)
		for e in camera.entities:
			screen.blit(e.image, camera.apply(e))

		pygame.display.update()


if __name__ == "__main__":
	main()
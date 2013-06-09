import sys, pygame, random, math

from objects import *

class Player(pygame.sprite.OrderedUpdates):

  def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		self.add(PlayerSprite(Game.width/2, Game.height/2))

class PlayerSprite(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.speed = 5

		self.imgdown  = pygame.image.load('gfx/player_down.png').convert_alpha()
		self.imgup    = pygame.image.load('gfx/player_up.png').convert_alpha()
		self.imgleft  = pygame.image.load('gfx/player_left.png').convert_alpha()
		self.imgright = pygame.image.load('gfx/player_right.png').convert_alpha()

		self.image = self.imgdown
		self.rect  = self.image.get_rect(center = [x, y])

	def update(self):
		if isDown(pygame.K_LEFT) or isDown(pygame.K_a):
			self.image = self.imgleft
			self.rect = self.rect.move([-self.speed, 0])
		elif isDown(pygame.K_RIGHT) or isDown(pygame.K_d):
			self.image = self.imgright
			self.rect = self.rect.move([self.speed, 0])
		elif isDown(pygame.K_UP) or isDown(pygame.K_w):
			self.image = self.imgup
			self.rect = self.rect.move([0, -self.speed])
		elif isDown(pygame.K_DOWN) or isDown(pygame.K_s):
			self.image = self.imgdown
			self.rect = self.rect.move([0, self.speed])	

		if len(Game.groups) > 0:
			if len(Game.groups[-2].sprites()) > 0:
				if pygame.sprite.groupcollide(Game.player, Game.groups[-3], False, False):
					# throw notice to collect flames
					if isDown(pygame.K_LEFT) or isDown(pygame.K_a):
						self.rect = self.rect.move([self.speed, 0])
					elif isDown(pygame.K_RIGHT) or isDown(pygame.K_d):
						self.rect = self.rect.move([-self.speed, 0])
					elif isDown(pygame.K_UP) or isDown(pygame.K_w):
						self.rect = self.rect.move([0, self.speed])
					elif isDown(pygame.K_DOWN) or isDown(pygame.K_s):
						self.rect = self.rect.move([0, -self.speed])

			if pygame.sprite.groupcollide(Game.player, Game.groups[-1], False, False):
				if isDown(pygame.K_LEFT) or isDown(pygame.K_a):
					self.rect = self.rect.move([self.speed, 0])
				elif isDown(pygame.K_RIGHT) or isDown(pygame.K_d):
					self.rect = self.rect.move([-self.speed, 0])
				elif isDown(pygame.K_UP) or isDown(pygame.K_w):
					self.rect = self.rect.move([0, self.speed])
				elif isDown(pygame.K_DOWN) or isDown(pygame.K_s):
					self.rect = self.rect.move([0, -self.speed])

		Game.playerX, Game.playerY = self.rect.center

class PlayerLight(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.life      = 180
		self.lifecount = 0

		self.image     = pygame.Surface([Game.width, Game.height])
		self.rect      = self.image.get_rect(center = [x, y])
		self.image.fill([0, 0, 0])

		self.orb       = pygame.image.load('gfx/light.png').convert()
		self.orb_rect  = self.orb.get_rect(center = [x, y])

		# STARTED TO ADD SHADOWS BUT WE CAN A SUBSTANTIAL PERFORMANCE HIT
		#self.shad      = pygame.Surface([Game.width, Game.height])
		#self.shad_rect = self.image.get_rect(center = [x, y])
		#self.shad.set_alpha(40)

		self.frame     = 0
		self.forward   = True

	def update(self):
		self.image.fill([0, 0, 0])

		if self.forward and self.frame < 8:
			self.frame  += 2
		elif self.frame == 8:
			self.forward = False
			self.frame  -= 2
		elif not self.forward and self.frame > 0:
			self.frame  -= 2
		elif self.frame == 0:
			self.lifecount += 1
			if self.lifecount == 2:
				self.life -= 1
				self.lifecount = 0

			self.forward = True
			self.frame  += 2

		self.orb_rect.center  = [Game.playerX, Game.playerY]

		self.orb.set_alpha((255-25)*(self.life+self.frame)/180+25)
		self.image.blit(self.orb, self.orb_rect)

		if Game.light.life <= 0:
			for i in range(len(Game.groups)):
				Game.groups[i].empty(); i -= 1
			del Game.groups[:]

			Game.playerOn = False
			Game.groups.append(TitleScreen())
			Game.player.sprites()[0].rect.center = [Game.width/2, Game.height/2]

		# STARTED TO ADD SHADOWS BUT WE CAN A SUBSTANTIAL PERFORMANCE HIT
		#self.shad.fill([0, 0, 0])

		#sprites = Game.groups[-2].sprites()
		#for i in range(len(sprites)):
		#	rect = sprites[i].rect

		#	points = []
		#	points.append([rect.left, rect.top])
		#	points.append([rect.right, rect.top])
		#	points.append([15*(rect.center[0]-Game.playerX)+rect.center[0], 15*(rect.center[1]-Game.playerY)+rect.center[1]])

		#	pygame.draw.polygon(self.shad, [4, 4, 4], points)

# == Level1 entities
class Level2(pygame.sprite.OrderedUpdates):

	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		layout = [
			[None, None, 0x00, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x03, 0x03, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x03, 0x03, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x02, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x02, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00],
			[0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03],
		]

		offsetX, offsetY = 0, 5*32

		# remember to empty this
		self.doors      = pygame.sprite.Group()
		self.enemies    = pygame.sprite.Group()
		self.collidable = pygame.sprite.Group()

		for col in range(len(layout)):
			for row in range(len(layout[col])):
				if layout[col][row] == Game.WALL:
					self.collidable.add(Wall(32*row+offsetX, 32*col+offsetY, 'gfx/wall.png'))
				if layout[col][row] == Game.WALLTOP:
					self.collidable.add(Wall(32*row+offsetX, 32*col+offsetY, 'gfx/wall_top.png'))
				if layout[col][row] == Game.DOOR:
					self.doors.add(Floor(32*row+offsetX, 32*col+offsetY, 'gfx/floor.png'))
				if layout[col][row] == Game.FLOOR:
					self.add(Floor(32*row+offsetX, 32*col+offsetY, 'gfx/floor.png'))
					if random.randint(1, 10) == 1:
						self.enemies.add(Rat(32*row+offsetX, 32*col+offsetY))

		while len(self.enemies.sprites()) == 0:
			for col in range(len(layout)):
				for row in range(len(layout[col])):
					if layout[col][row] == Game.FLOOR:
						if random.randint(1, 10) == 1:
							self.enemies.add(Rat(32*row+offsetX, 32*col+offsetY))

		Game.groups.append(self.doors)
		Game.groups.append(self.enemies)
		Game.groups.append(self.collidable)

	def update(self):
		if Game.playerX < 0:
			for i in range(len(Game.groups)):
				Game.groups[i].empty(); i -= 1
			del Game.groups[:]

			Game.groups.insert(0, Level1())
			Game.player.sprites()[0].rect.right = Game.width-32

			return False

# == Level1 entities
class Level1(pygame.sprite.OrderedUpdates):

	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		layout = [
			[None, 0x00, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x00],
			[None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x03],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x03, 0x01, 0x01, 0x01, 0x01, 0x00, 0x03, 0x03, 0x03, 0x01, 0x01, 0x03, 0x03, 0x03, 0x00],
			[0x02, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x02, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x01, 0x01, 0x03, 0x03, 0x00, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, None, 0x00, 0x03, 0x03, 0x03, 0x03, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x03, 0x00, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x03, 0x00, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, None, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03]
		]

		offsetX, offsetY = 0, 0

		# remember to empty this
		self.doors      = pygame.sprite.Group()
		self.enemies    = pygame.sprite.Group()
		self.collidable = pygame.sprite.Group()

		for col in range(len(layout)):
			for row in range(len(layout[col])):
				if layout[col][row] == Game.WALL:
					self.collidable.add(Wall(32*row+offsetX, 32*col+offsetY, 'gfx/wall.png'))
				if layout[col][row] == Game.WALLTOP:
					self.collidable.add(Wall(32*row+offsetX, 32*col+offsetY, 'gfx/wall_top.png'))
				if layout[col][row] == Game.DOOR:
					self.doors.add(Floor(32*row+offsetX, 32*col+offsetY, 'gfx/floor.png'))
				if layout[col][row] == Game.FLOOR:
					self.add(Floor(32*row+offsetX, 32*col+offsetY, 'gfx/floor.png'))
					if random.randint(1, 10) == 1:
						self.enemies.add(Rat(32*row+offsetX, 32*col+offsetY))

		while len(self.enemies.sprites()) == 0:
			for col in range(len(layout)):
				for row in range(len(layout[col])):
					if layout[col][row] == Game.FLOOR:
						if random.randint(1, 10) == 1:
							self.enemies.add(Rat(32*row+offsetX, 32*col+offsetY))

		Game.groups.append(self.doors)
		Game.groups.append(self.enemies)
		Game.groups.append(self.collidable)

	def update(self):
		if Game.playerX < 0:
			for i in range(len(Game.groups)):
				Game.groups[i].empty(); i -= 1
			del Game.groups[:]

			Game.groups.insert(0, DemoLevel())
			Game.player.sprites()[0].rect.right = Game.width-32

			return False

		if Game.playerX > Game.width:
			for i in range(len(Game.groups)):
				Game.groups[i].empty(); i -= 1
			del Game.groups[:]

			Game.groups.insert(0, Level2())
			Game.player.sprites()[0].rect.left = 32

			return False

# == DemoLevel entities
class DemoLevel(pygame.sprite.OrderedUpdates):

	def __init__(self):
		pygame.sprite.OrderedUpdates.__init__(self)

		layout = [
			[None, None, 0x00, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[None, None, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x03, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x02],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x03, 0x03],
			[0x00, 0x01, 0x01, 0x03, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x03, 0x03, 0x00, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, None, None, 0x00, 0x01, 0x01, 0x01, 0x00],
			[0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, None, None, 0x03, 0x03, 0x03, 0x03, 0x03],
			[0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03]
		]

		offsetX, offsetY = 32*6, 32*5

		# remember to empty this
		self.doors      = pygame.sprite.Group()
		self.enemies    = pygame.sprite.Group()
		self.collidable = pygame.sprite.Group()

		for col in range(len(layout)):
			for row in range(len(layout[col])):
				if layout[col][row] == Game.WALL:
					self.collidable.add(Wall(32*row+offsetX, 32*col+offsetY, 'gfx/wall.png'))
				if layout[col][row] == Game.WALLTOP:
					self.collidable.add(Wall(32*row+offsetX, 32*col+offsetY, 'gfx/wall_top.png'))
				if layout[col][row] == Game.DOOR:
					self.doors.add(Floor(32*row+offsetX, 32*col+offsetY, 'gfx/floor.png'))
				if layout[col][row] == Game.FLOOR:
					self.add(Floor(32*row+offsetX, 32*col+offsetY, 'gfx/floor.png'))
					if random.randint(1, 10) == 1:
						self.enemies.add(Rat(32*row+offsetX, 32*col+offsetY))

		while len(self.enemies.sprites()) == 0:
			for col in range(len(layout)):
				for row in range(len(layout[col])):
					if layout[col][row] == Game.FLOOR:
						if random.randint(1, 10) == 1:
							self.enemies.add(Rat(32*row+offsetX, 32*col+offsetY))

		Game.groups.append(self.doors)
		Game.groups.append(self.enemies)
		Game.groups.append(self.collidable)

	def update(self):
		if Game.playerX > Game.width:
			for i in range(len(Game.groups)):
				Game.groups[i].empty(); i -= 1
			del Game.groups[:]

			Game.groups.insert(0, Level1())
			Game.player.sprites()[0].rect.left = 32

			return False

class Rat(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)

		self.speed     = 2
		self.isHostile = False

		self.image     = pygame.image.load('gfx/rat.png').convert_alpha()
		self.rect      = self.image.get_rect(left = x, top = y)

	def update(self):

		diffX = self.rect.center[0] - Game.playerX
		diffY = self.rect.center[1] - Game.playerY

		if self.isHostile and (abs(diffX)+abs(diffY)) < 300:
			if random.randint(1, 250) == 1:
				self.isHostile = False
				moveX = self.speed * diffX / (abs(diffX)+abs(diffY))
				moveY = self.speed * diffY / (abs(diffX)+abs(diffY))
			else:
				moveX = -self.speed * diffX / (abs(diffX)+abs(diffY))
				moveY = -self.speed * diffY / (abs(diffX)+abs(diffY))
		else:
			if random.randint(1, 500) == 1:
				# % to become hostile / not hostile
				self.isHostile = True
				moveX = -self.speed * diffX / (abs(diffX)+abs(diffY))
				moveY = -self.speed * diffY / (abs(diffX)+abs(diffY))
			elif (abs(diffX)+abs(diffY)) > 300:
				# if far away just move ramdomly
				randn = random.randint(-1, 1)
				moveX = self.speed * randn
				randn = random.randint(-1, 1)
				moveY = self.speed * randn
			else:
				moveX = self.speed * diffX / (abs(diffX)+abs(diffY))
				moveY = self.speed * diffY / (abs(diffX)+abs(diffY))

		self.rect = self.rect.move([moveX, moveY])

		if pygame.sprite.spritecollide(self, Game.groups[-1], False) or pygame.sprite.spritecollide(self, Game.groups[-3], False):
			self.rect = self.rect.move([-moveX, -moveY])
		if pygame.sprite.spritecollide(self, Game.player, False):
			if self.isHostile:
				Game.light.life -= random.randint(20, 30)
			else:
				Game.light.life += 15
				if Game.light.life > 180:
					Game.light.life = 180
			self.kill()
			# check for the length of rats
			# - if zero then display a notice to proceed to next level

class Wall(pygame.sprite.Sprite):

	def __init__(self, x, y, url):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(url).convert()
		self.rect  = self.image.get_rect(left = x, top = y)

class Floor(pygame.sprite.Sprite):

	def __init__(self, x, y, url):
		pygame.sprite.Sprite.__init__(self)

		self.image = pygame.image.load(url).convert()
		self.rect  = self.image.get_rect(left = x, top = y)

# == TitleScreen entities
class TitleScreen(pygame.sprite.Group):

	def __init__(self):
		pygame.sprite.Group.__init__(self)

		self.add(Text('Lights Out!!', Game.width/2, Game.height/4    , [255, 255, 255], 70))
		self.add(Text('Play'        , Game.width/2, Game.height/2+25 , [255, 255, 255], 40))
		self.add(Text('Exit'        , Game.width/2, Game.height/2+100, [255, 255, 255], 40))

		self.add(Text('- Move from room to room collecting flames', Game.width/2, Game.height/4+75, [255, 255, 255], 20))
		self.add(Text('- You must collect all flames before moving to the next room', Game.width/2, Game.height/4+105, [255, 255, 255], 20))
		self.add(Text('- Flames may become hostile and attack you! (watch out!!)', Game.width/2, Game.height/4+135, [255, 255, 255], 20))

		self.add(Text('Programming: Stephen Meier - Artwork: Completeli', 240, Game.height-35, [255, 255, 255], 20))

		self.add(TitleCursor())

class Text(pygame.sprite.Sprite):

	def __init__(self, text, x, y, color, size):
		pygame.sprite.Sprite.__init__(self)

		titleFont  = pygame.font.Font('munro.ttf', size)
		self.image = titleFont.render(text, False, color)
		self.rect  = self.image.get_rect(center = [x, y])

class TitleCursor(Text):

	def __init__(self):
		Text.__init__(self, '<        >', Game.width/2, Game.height/2+25, [255, 255, 255], 40)
		self.playselected = True

	def update(self):
		if isDown(pygame.K_DOWN) and self.playselected:
			self.rect = self.rect.move([0, 75])
			self.playselected = False
		if isDown(pygame.K_UP) and not self.playselected:
			self.rect = self.rect.move([0, -75])
			self.playselected = True
		if isDown(pygame.K_RETURN):
			Game.light.life = 180
			if self.playselected:
				for i in range(len(Game.groups)):
					Game.groups[i].empty()
					i -= 1
				del Game.groups[:]
				Game.groups.insert(0, DemoLevel())
				Game.playerOn = True
			else: sys.exit()

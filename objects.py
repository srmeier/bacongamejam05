import pygame

class Game(object):

  font     = pygame.font.Font('munro.ttf', 20)
	timer    = pygame.time.Clock()

	groups   = []
	keysdown = []

	width    = None
	height   = None
	screen   = None

	light    = None
	player   = None
	playerX  = 0
	playerY  = 0
	playerOn = False

	# entity flags
	WALL      = 0x00
	FLOOR     = 0x01
	DOOR      = 0x02
	WALLTOP   = 0x03
	FLOORTOP  = 0x04
	FLOORTOPL = 0x05
	FLOORTOPR = 0x06
	FLOORBOT  = 0x07

def isDown(key):
	for downkey in Game.keysdown:
		if key == downkey:
			return True
	return False

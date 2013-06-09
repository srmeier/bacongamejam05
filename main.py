import sys, pygame, math
pygame.init()

from objects import *
from entities import *

# == init baseline game object
Game.width  = 960
Game.height = 768
Game.screen = pygame.display.set_mode([Game.width, Game.height])

# == game groups
Game.groups.append(TitleScreen())

# == player
Game.player = Player()
Game.light  = PlayerLight(Game.width/2, Game.height/2)

# == game loop
while True:
  # == set FPS
	Game.timer.tick(30)

	# == update
	for i in range(len(Game.groups)):
		if Game.groups[i].update() == False:
			break
	if Game.playerOn: Game.player.update()
	if Game.playerOn: Game.light.update()

	# == poll for events
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYUP:
			Game.keysdown.remove(event.key)
		if event.type == pygame.KEYDOWN:
			Game.keysdown.append(event.key)

	# == draw to screen
	Game.screen.fill([0, 0, 0])

	for i in range(len(Game.groups)):
		Game.groups[i].draw(Game.screen)
	if Game.playerOn: Game.player.draw(Game.screen)
	if Game.playerOn: Game.screen.blit(Game.light.image, Game.light.rect, None, pygame.BLEND_MULT)
	# STARTED TO ADD SHADOWS BUT WE CAN A SUBSTANTIAL PERFORMANCE HIT
	#if Game.playerOn: Game.screen.blit(Game.light.shad, Game.light.shad_rect, None, pygame.BLEND_SUB)

	if Game.playerOn:
		if math.floor(Game.light.life/180.0*100) > 0:
			tex = 'Health: '+str(math.floor(Game.light.life/180.0*100))
		else:
			tex = 'Health: '+str(math.floor(0/180.0*100))
		Game.screen.blit(Game.font.render(tex, False, [255, 255, 255]), [Game.width-110, 0])

		tex = 'Flames Left: '+str(len(Game.groups[0].enemies.sprites()))
		Game.screen.blit(Game.font.render(tex, False, [255, 255, 255]), [Game.width-260, 0])

	# == display FPS and switch screen with buffer
	#textFps = 'FPS: '+str(int(Game.timer.get_fps()))
	#Game.screen.blit(Game.font.render(textFps, False, [255, 255, 255]), [0, 0])
	pygame.display.flip()

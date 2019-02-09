# import and initialize pygame
import pygame
from pygame.locals import *
pygame.init()

# import custom scripts and classes
import Constants
from Vector import *
from Enemy import *

# set display
screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
pygame.display.set_caption("Intro to Pygame")

# retrieve framerate of game
framerate = pygame.time.Clock()

# method to respond to in-game events
def EventHandler():
	for event in pygame.event.get():
		# if player attempts to quit, exit game
		if event.type == QUIT:
			pygame.quit()
			quit()

# starting position and movement speed of player-square
rectX = 388
rectY = 288
rectSpeed = 1

# spawn and initialize a new enemy
#newEnemy = Enemy(Vector(288, 288), Vector(1, 1), 30)

# game loop
while True:
	# respond to in-game events
	EventHandler()
			
	# lock framerate
	framerate.tick(Constants.FRAME_RATE)

	# move player-square using WASD
	pressed = pygame.key.get_pressed()
	if pressed[K_w]:
		rectY -= rectSpeed
	elif pressed[K_s]:
		rectY += rectSpeed
	if pressed[K_a]:
		rectX -= rectSpeed
	elif pressed[K_d]:
		rectX += rectSpeed

	# draw player-square on the screen
	pygame.draw.rect(screen, pygame.Color(0, 255, 0, 255), pygame.Rect(rectX, rectY, 25 ,25), 0)
	
	# update position of and draw enemy square
	#newEnemy.update()
	#newEnemy.draw(screen)

	# update display and erase residue of this frame before drawing the next
	pygame.display.update()
	screen.fill(Constants.BACKGROUND_COLOR)
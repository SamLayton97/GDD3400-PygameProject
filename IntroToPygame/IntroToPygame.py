# import and initialize pygame
import pygame
from pygame.locals import *
pygame.init()

# import custom scripts and classes
import Constants
from Vector import *
from Player import *
from Enemy import *

# set display
screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
pygame.display.set_caption("Moving Agents")

# retrieve framerate of game
framerate = pygame.time.Clock()

# method to respond to in-game events
def EventHandler():
	for event in pygame.event.get():
		# if player attempts to quit, exit game
		if event.type == QUIT:
			pygame.quit()
			quit()

# spawn and initialize player on center-screen
myPlayer = Player(Vector(Constants.WORLD_WIDTH / 2, Constants.WORLD_HEIGHT / 2), Constants.PLAYER_SIZE, Constants.PLAYER_SPEED)

# spawn and initialize a new enemy
#newEnemy = Enemy(Vector(288, 288), Vector(1, 1), 30)

# game loop
while True:
    # respond to in-game events
    EventHandler()

    # lock framerate
    framerate.tick(Constants.FRAME_RATE)

    # update and draw player
    myPlayer.update()
    myPlayer.draw(screen)

    # update position of and draw enemy square
	#newEnemy.update()
	#newEnemy.draw(screen)

    # update display and erase residue of current frame before drawing next
    pygame.display.update()
    screen.fill(Constants.BACKGROUND_COLOR)
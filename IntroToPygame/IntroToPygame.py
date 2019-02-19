# import libraries
import random
import pygame
from pygame.locals import *
pygame.init()

# import custom scripts and classes
import Constants
from Vector import *
from Player import *
from Sheep import *

# method to respond to in-game events
def EventHandler():
	for event in pygame.event.get():
		# if timer ends, allow "tag-backs"
		if event.type == USEREVENT:
			myPlayer.canTagBack = True
			for agent in sheep:
				agent.canTagBack = True
		# if player attempts to quit, exit game
		if event.type == QUIT:
			pygame.quit()
			quit()

# set display
screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
worldBounds = Vector(Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT)
pygame.display.set_caption("Herding Sheep")

# retrieve framerate of game
framerate = pygame.time.Clock()

# spawn player at center of screen
myPlayer = Player(Vector(Constants.WORLD_WIDTH / 2, Constants.WORLD_HEIGHT / 2), Constants.PLAYER_SIZE, Constants.PLAYER_SPEED, Constants.PLAYER_COLOR)

# spawn 10 sheep at random points on map
sheep = []
for i in range(10):
	randX = random.randint(1, Constants.WORLD_WIDTH - Constants.ENEMY_SIZE - 1)
	randY = random.randint(1, Constants.WORLD_HEIGHT - Constants.ENEMY_SIZE - 1)
	newSheep = Sheep(Vector(randX, randY), Constants.ENEMY_SIZE, Constants.ENEMY_SPEED, Constants.ENEMY_COLOR)
	sheep.append(newSheep)

# game loop
while True:
	# respond to in-game events
	EventHandler()

	# lock framerate
	framerate.tick(Constants.FRAME_RATE)

	# update and draw player and ai agents
	myPlayer.update(sheep[0], worldBounds)
	myPlayer.draw(screen)
	for agent in sheep:
		agent.update(myPlayer, worldBounds)
		agent.draw(screen)

	# update display and erase residue of current frame before drawing next
	pygame.display.update()
	screen.fill(Constants.BACKGROUND_COLOR)
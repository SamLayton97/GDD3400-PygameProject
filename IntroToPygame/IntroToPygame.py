# import libraries
import random
import pygame
from pygame.locals import *
pygame.init()

# import custom scripts and classes
import Constants
from Vector import *
from Player import *
from Dog import *
from Sheep import *

# method to respond to in-game events
def EventHandler():
	for event in pygame.event.get():
		# if timer ends, allow "tag-backs"
		if event.type == USEREVENT:
			myDog.canTagBack = True
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

# load in agents' sprites
sheepSurface = pygame.image.load('sheep.png')
dogSurface = pygame.image.load('collie.png')

# spawn player at center of screen
myDog = Dog(Vector(Constants.WORLD_WIDTH / 2, Constants.WORLD_HEIGHT / 2), Vector(Constants.DOG_WIDTH, Constants.DOG_HEIGHT), Constants.PLAYER_SPEED, Constants.PLAYER_COLOR, dogSurface)

# spawn 10 sheep at random points on map
sheep = []
for i in range(100):
	randX = random.randint(1, Constants.WORLD_WIDTH - Constants.SHEEP_WIDTH - 1)
	randY = random.randint(1, Constants.WORLD_HEIGHT - Constants.SHEEP_HEIGHT - 1)
	newSheep = Sheep(Vector(randX, randY), Vector(Constants.SHEEP_WIDTH, Constants.SHEEP_HEIGHT), Constants.ENEMY_SPEED, Constants.ENEMY_COLOR, sheepSurface)
	sheep.append(newSheep)

# for each sheep, send them info of all other sheep in game (from which to find neighbors from)
for agent in sheep:
	agent.herd = sheep

# game loop
while True:
	# respond to in-game events
	EventHandler()

	# lock framerate
	framerate.tick(Constants.FRAME_RATE)

	# update and draw player and ai agents
	myDog.update(sheep[0], worldBounds)
	myDog.draw(screen)
	for agent in sheep:
		agent.update(myDog, worldBounds)
		agent.draw(screen, myDog)

	# update display and erase residue of current frame before drawing next
	pygame.display.update()
	screen.fill(Constants.BACKGROUND_COLOR)
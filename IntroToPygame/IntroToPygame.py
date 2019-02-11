# import libraries
import random
import pygame
from pygame.locals import *
pygame.init()

# import custom scripts and classes
import Constants
from Vector import *
from Player import *
from Enemy import *
from EnemyHunter import *

# method to respond to in-game events
def EventHandler():
	for event in pygame.event.get():
		# if timer ends, allow "tag-backs"
		if event.type == USEREVENT:
			myPlayer.canTagBack = True
			for enemy in enemies:
				enemy.canTagBack = True
		# if player attempts to quit, exit game
		if event.type == QUIT:
			pygame.quit()
			quit()

# set display
screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
worldBounds = Vector(Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT)
pygame.display.set_caption("Moving Agents")

# retrieve framerate of game
framerate = pygame.time.Clock()

# spawn player at center of screen
myPlayer = Player(Vector(Constants.WORLD_WIDTH / 2, Constants.WORLD_HEIGHT / 2), Constants.PLAYER_SIZE, Constants.PLAYER_SPEED, Constants.PLAYER_COLOR)

# spawn 5 standard enemies at random points on map
enemies = []
for i in range(5):
	randX = random.randint(1, Constants.WORLD_WIDTH - Constants.ENEMY_SIZE - 1)
	randY = random.randint(1, Constants.WORLD_HEIGHT - Constants.ENEMY_SIZE - 1)
	newEnemy = Enemy(Vector(randX, randY), Constants.ENEMY_SIZE, Constants.ENEMY_SPEED, Constants.ENEMY_COLOR)
	enemies.append(newEnemy)

# spawn 5 hunter enemies at random points on map
for i in range(5):
	randX = random.randint(1, Constants.WORLD_WIDTH - Constants.ENEMY_SIZE - 1)
	randY = random.randint(1, Constants.WORLD_HEIGHT - Constants.ENEMY_SIZE - 1)
	newHunter = EnemyHunter(Vector(randX, randY), Constants.ENEMY_SIZE, Constants.ENEMY_SPEED, Constants.HUNTER_COLOR)
	enemies.append(newHunter)

# game loop
while True:
	# respond to in-game events
	EventHandler()

	# lock framerate
	framerate.tick(Constants.FRAME_RATE)

	# update and draw player and ai agents
	myPlayer.update(enemies[0], worldBounds)
	myPlayer.draw(screen)
	for enemy in enemies:
		enemy.update(myPlayer, worldBounds)
		enemy.draw(screen)

	# update display and erase residue of current frame before drawing next
	pygame.display.update()
	screen.fill(Constants.BACKGROUND_COLOR)
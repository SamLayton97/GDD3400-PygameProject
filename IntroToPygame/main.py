import pygame
import random
import Vector
import Agent
import Player
import Sheep
import Constants
import Graph
import Node

from pygame import *
from random import *
from Vector import *
from Agent import *
from Sheep import *
from Player import *
from Graph import *
from Node import *

#################################################################################
# Helper Functions
#################################################################################

def buildGates(graph):
	X = 0
	Y = 1
	# Add the gates to the game
	# pick one end, then pick the second end about 50 spaces away (pick a direction, generate the far end
	for gate in Constants.GATES:
		graph.placeObstacle(Vector(gate[0][X], gate[0][Y]), (0, 255, 0))
		graph.placeObstacle(Vector(gate[1][X], gate[1][Y]), (255, 0, 0))
		print("Placing Obstacles: " + str(gate[0]) + " " + str(gate[1]))

	# Add the final pen based on the final gate
	finalGate = gate[-2:]
	# If the gate is horizontally arranged
	if finalGate[0][Y] == finalGate[1][Y]:
		# If the green gate (the first gate) is on the right, paddock goes "up"
		if finalGate[0][X] > finalGate[1][X]:
			direction = -1
		else:
			direction = 1
		for y in range(finalGate[0][Y] + direction * 16, finalGate[0][Y] + direction * 112, direction * 16):
			graph.placeObstacle(Vector(finalGate[0][X], y), (0, 0, 0))
			graph.placeObstacle(Vector(finalGate[1][X], y), (0, 0, 0))
		for x in range(finalGate[0][X] + direction * 16, finalGate[1][X], direction * 16):
			graph.placeObstacle(Vector(x, finalGate[0][Y] + direction * 96), (0, 0, 0))
	# If the gate is vertically arranged
	else:
		# If the green gate (the first gate) is on the bottom, paddock goes "right"
		if finalGate[0][Y] < finalGate[1][Y]:
			direction = -1
		else:
			direction = 1
		for x in range(finalGate[0][X] + direction * 16, finalGate[1][X] + direction * 112, direction * 16):
			graph.placeObstacle(Vector(x, finalGate[0][Y]), (0, 0, 0))
			graph.placeObstacle(Vector(x, finalGate[1][Y]), (0, 0, 0))
		for y in range(finalGate[0][Y] - direction *  16, finalGate[1][Y], - direction * 16):
			graph.placeObstacle(Vector(finalGate[0][X] + direction * 96, y), (0, 0, 0))

def buildObstacles(graph):
	# Random Obstacles
	for i in range(Constants.NBR_RANDOM_OBSTACLES):
		start = Vector(randrange(0, Constants.WORLD_WIDTH), randrange(0, Constants.WORLD_HEIGHT))
		graph.placeObstacle(start, (0, 0, 0))
		for j in range(randrange(Constants.NBR_RANDOM_OBSTACLES)):
			start += Vector((randrange(3) - 1) * Constants.GRID_SIZE, (randrange(3) - 1) * Constants.GRID_SIZE)
			while(start.x >= Constants.WORLD_WIDTH - Constants.GRID_SIZE or start.y >= Constants.WORLD_HEIGHT - Constants.GRID_SIZE):
				start += Vector((randrange(3) - 1) * Constants.GRID_SIZE, (randrange(3) - 1) * Constants.GRID_SIZE)
			graph.placeObstacle(start, (0, 0, 0))

#################################################################################
# Main Functionality
#################################################################################

pygame.init();

screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
clock = pygame.time.Clock()
sheepImage = pygame.image.load('sheep.png')
dogImage = pygame.image.load('dog.png')
bounds = Vector(Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT)

# Setup the graph
graph = Graph()

# Setup the dog
dog = Player(dogImage, Vector(Constants.WORLD_WIDTH * .5, Constants.WORLD_HEIGHT * .5), 
			 Vector(Constants.DOG_WIDTH, Constants.DOG_HEIGHT), (0, 255, 0), 
			 Constants.DOG_SPEED, Constants.DOG_ANGULAR_SPEED)

# Setup the sheep (only 1 for now...)
herd = []
sheep = Sheep(sheepImage, Vector(randrange(int(bounds.x * .4), int(bounds.x * .6)),
								  randrange(int(bounds.y * .6), int(bounds.y * .8))), 
			   Vector(Constants.DOG_WIDTH, Constants.DOG_HEIGHT), (0, 255, 0), Constants.SHEEP_SPEED, Constants.SHEEP_ANGULAR_SPEED)
herd.append(sheep)

# Setup the gates and obstacles
buildGates(graph)
buildObstacles(graph)

# While the user has not selected quit
hasQuit = False
while not hasQuit:
	# Clear the screen
	screen.fill(Constants.BACKGROUND_COLOR)

	# Process all in-game events
	for event in pygame.event.get():
		if event.type == pygame.QUIT \
			or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			hasQuit = True

	# Update the agents onscreen
	dog.update(bounds, graph, herd, Constants.GATES)
	for sheep in herd:
		sheep.update(bounds, graph, dog, herd, Constants.GATES)	

	# Draw the agents onscreen
	graph.draw(screen)
	dog.draw(screen)
	for sheep in herd:
		sheep.draw(screen)

	# Double buffer
	pygame.display.flip()

	# Limit to 60 FPS
	clock.tick(Constants.FRAME_RATE)

# Quit
pygame.quit()
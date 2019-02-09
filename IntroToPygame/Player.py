from Vector import *
import pygame
from pygame.locals import *
pygame.init()

# A player-controlled agent
class Player:

    # public variables
    position
    velocity
    size
    speed
    objectCenter

    # Constructor:
    # Initializes player agent's starting position,
    # size, and speed according to parameters, and 
    # initializes player's velocity and center from that.
    def __init__(self, position, size, speed):
        # set position, size, and speed to parameters
        self.position = position
        self.size = size
        self.speed = speed

        # initialize velocity to 0 and calculate center of player object in world coordinates
        self.velocity = Vector(0, 0)
        self.objectCenter = Vector(position.numerator + (size / 2), position.denominator + (size / 2))

    # Prints player's size, position, velocity, and
    # center (in world coordinates) for debugging
    def __str__(self):
        print("Player Info:\n")
        print("Size: " + str(self.size))
        print("Position: (" + self.position.numerator + ", " + self.position.denominator + ")\n")
        print("Velocity: (" + self.velocity.numerator + ", " + self.velocity.denominator + ")\n")
        print("Center: (" + self.objectCenter.numerator + ", " + self.objectCenter.denominator + ")\n")

    # Draws colored square on screen representing player
    # and line representing their velocity
    def draw(self, screen):
        # draw self
        pygame.draw.rect(screen, pygame.Color(0, 255, 0, 255), pygame.Rect(self.position.numerator, self.position.denominator, self.size, self.size), 0)

from Vector import *
import pygame
from pygame.locals import *
pygame.init()

# A player-controlled agent
class Player:

    # public variables
    position = Vector(0, 0)
    velocity = Vector(0, 0)
    size = 0
    speed = 0
    objectCenter = Vector(0, 0)

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
        stringSize = "Size: " + str(self.size) + "\n"
        stringPosition = "Position: (" + str(self.position.numerator) + ", " + str(self.position.denominator) + ")\n"
        stringVelocity = "Velocity: (" + str(self.velocity.numerator) + ", " + str(self.velocity.denominator) + ")\n"
        stringCenter = "Center: (" + str(self.objectCenter.numerator) + ", " + str(self.objectCenter.denominator) + ")\n"
        return stringSize + stringPosition + stringVelocity + stringCenter

    # Draws colored square on screen representing player
    # and line representing their velocity
    def draw(self, screen):
        # draw self
        pygame.draw.rect(screen, pygame.Color(0, 255, 0, 255), pygame.Rect(self.position.numerator, self.position.denominator, self.size, self.size), 0)

        # for debugging, draw line representing player's velocity
        drawVector = self.velocity.scale(self.size)
        pygame.draw.line(screen, pygame.Color(0, 0, 255, 255), (self.objectCenter.numerator, self.objectCenter.denominator), 
				    (self.objectCenter.numerator + drawVector.numerator, self.objectCenter.denominator + drawVector.denominator), 4)

    # Moves player-object in response to player-input (WASD),
    # and updates velocity vector accordingly
    def update(self):
        # determine un-normalized movement vector according to player-input
        xInput = 0
        yInput = 0
        pressed = pygame.key.get_pressed()
        if pressed[K_w]:
            yInput = -1
        elif pressed[K_s]:
            yInput = 1
        if pressed[K_a]:
            xInput = -1
        elif pressed[K_d]:
            xInput = 1

        # move player in direction of normalized velocity, scaled up by their speed
        if xInput != 0 or yInput != 0:
            movementVector = Vector(xInput, yInput)
            self.velocity = movementVector.normalize()
            displacementVector = self.velocity.scale(self.speed)
            self.position += displacementVector
            self.objectCenter += displacementVector
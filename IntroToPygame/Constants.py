# Defines constants to use in game

# define screen display constants
FRAME_RATE = 60
WORLD_WIDTH = 800
WORLD_HEIGHT = 600
BACKGROUND_COLOR = (100, 149, 237)

# define game costants
NO_TAG_BACKS_DURATION = 1000

# define player constants
PLAYER_SIZE = 10
DOG_WIDTH = 16
DOG_HEIGHT = 32
PLAYER_SPEED = 5.5
PLAYER_COLOR = (0, 0, 255, 255)

# define enemy constants
ENEMY_SIZE = 10
SHEEP_WIDTH = 16
SHEEP_HEIGHT = 32
ENEMY_SPEED = 5
ENEMY_COLOR = (0, 0, 255, 255)
HUNTER_COLOR = (255, 0, 255, 255)
ATTACK_RANGE = 200

# define flocking behavior constants
SHEEP_NEIGHBOR_RADIUS = 50
SHEEP_BOUNDARY_RADIUS = 50
SHEEP_ALIGNMENT_WEIGHT = 0.3
SHEEP_SEPERATION_WEIGHT = 0.325
SHEEP_COHESION_WEIGHT = 0.3
SHEEP_DOG_INFLUENCE_WEIGHT = 0.2
SHEEP_BOUNDARY_INFLUENCE_WEIGHT = 0.2
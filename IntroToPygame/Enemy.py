import Constants
from Vector import *
from Agent import *

# Basic enemy agent with seek-flee capabilities
class Enemy(Agent):

	# Updates enemy's position, following target object if within attack range
	def update(self, target):
		# calculate direction and distance to target
		directionToTarget = target.position - self.position
		distToTarget = directionToTarget.length()

		# if target is within attack range, follow it
		if distToTarget < Constants.ATTACK_RANGE:
			self.velocity = directionToTarget.normalize()
			displacementVector = self.velocity.scale(self.speed)
			self.position += displacementVector
			self.objectCenter += displacementVector
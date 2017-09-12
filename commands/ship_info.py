

import numpy as np
import logging
from space_coordinate import space_coordinate as sc

logger = logging.getLogger("ship info")

#return received arguments excluding the first one
class ship_info():
   def __init__(self, ship):
      self.ship = ship

   def parse(self, args):
      commands = {
      "position":self.getPosition,
      "velocity":self.getVelocity,
      "heading":self.getHeading,
      }
      try:
         return commands[args[1]](args)
      except:
         return "Error. Usage: ship position/velocity"

   def simulate(self, dt):
      pass

   def getPosition(self, args):
      return str(self.ship.position)

   def getVelocity(self, args):
      return str(self.ship.velocity)
      
   def getHeading(self, args):
      try:
        return str(self.ship.heading.rotate(np.array([0.0, 0.0, 1.0])))
      except:
        logger.exception("Heading")
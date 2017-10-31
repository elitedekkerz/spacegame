

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
      "power":self.getPower,
      }
      try:
         return commands[args[1]](args)
      except:
         logging.exception("exception when running command")
         return "Usage", "ship position/velocity/heading/power"

   def simulate(self, dt, power_factor):
      pass

   def getPosition(self, args):
      return "Ok", str(self.ship.position)

   def getVelocity(self, args):
      return "Ok",  str(self.ship.velocity)
      
   def getHeading(self, args):
      try:
        return "Ok", str(self.ship.heading.rotate(np.array([0.0, 0.0, 1.0])))
      except:
        logger.exception("Heading")

   def getPower(self, args):
      return str(self.ship.power_needed / 1000) + "/" + str(self.ship.power_generated / 1000) + " kW"

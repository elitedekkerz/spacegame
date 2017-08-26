import numpy as np
from pyquaternion import Quaternion
import logging

class thrusters():

   def __init__(self, ship, power_vect):
      #thruster names and their values
      self.ship = ship
      self.thruster_power = power_vect
      self.set_value = 0.0

   def simulate(self, dt):
      self.ship.thrust_acc += self.thruster_power / self.ship.mass * self.set_value

   def set(self, args):
      try:
         val = np.clip(float(args[2]), 0, 1)
         self.set_value = val
         return "{0} thruster set to: {1}".format(args[2], val)
      except:
         logging.exception("exception when setting thruster value")
         return "Error. Usage: set thruster <name> {float = 0.0 - 1.0}"

   def get(self, args):
      return str(self.set_value)
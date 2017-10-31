import numpy as np
from pyquaternion import Quaternion
import logging

class thrusters():

   def __init__(self, ship, power_vect):
      #thruster names and their values
      self.ship = ship
      self.thruster_power = power_vect
      self.set_value = 0.0

      #Watts needed for 1 newton
      self.power_consumption = 50

   def parse(self, args):
      commands = {
      "set":self.set,
      "get":self.get,
      }
      try:
         return commands[args[1]](args)
      except:
         return "Usage", "thruster set {float = 0.0 - 1.0}"

   def simulate(self, dt, power_factor):
      self.ship.thrust_acc += self.thruster_power / self.ship.mass * self.set_value * power_factor

   def set(self, args):
      try:
         val = np.clip(float(args[2]), 0, 1)
         self.set_value = val
         return "Ok", "{0} thruster set to: {1}".format(args[2], val)
      except:
         logging.exception("exception when setting thruster value")
         return "Usage", "set thruster <name> {float = 0.0 - 1.0}"

   def get(self, args):
      return "Ok", str(self.set_value)

   def getPowerNeeded(self):
      return self.set_value * self.power_consumption * np.linalg.norm(self.thruster_power)

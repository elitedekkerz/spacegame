import numpy as np
from pyquaternion import Quaternion
import logging

class thrusters():
   #Thruster powers in N
   thruster_power_front = 100000.0
   thruster_power_back = 1000000.0

   def __init__(self, ship):
      #thruster names and their values
      self.thruster_by_name = {
         "front":0.0,
         "back":0.0
      }
      self.ship = ship

   def simulate(self, dt):
      acceleration = np.array([0.0, 0.0, 0.0])
      acceleration[0] = (self.thruster_by_name['back'] * self.thruster_power_back - self.thruster_by_name['front'] * self.thruster_power_front) / self.ship.mass
      self.ship.velocity += acceleration * dt
      self.ship.position += self.ship.velocity * dt

   def set(self, args):
      try:
         val = np.clip(float(args[3]), 0, 1)
         self.thruster_by_name[args[2]] = val
         return "{0} thruster set to: {1}".format(args[2], val)
      except:
         logging.exception("exception when setting thruster value")
         return "Error. Usage: set thruster <name> {float = 0.0 - 1.0}"

   def get(self, args):
      return str(self.thruster_by_name[args[2]])

   def thrust(self,data):
      try:
         val = float(data[2])
         self.thruster_by_name['back'] = np.clip(val, 0, 1)
         return "Back thruster set to: {0}".format(self.thruster_by_name['back'])
      except:
         return "Error. Usage: thrust {float = 0.0 - 1.0}"
   
   def fthrust(self,data):
      try:
         val = float(data[2])
         self.thruster_['front'] = np.clip(val, 0, 1)
         return "Front thruster set to: {0}".format(self.thruster_by_name['front'])
      except:
         return "Error. Usage: fthrust {float = 0.0 - 1.0}"

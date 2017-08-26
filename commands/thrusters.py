import numpy as np
from pyquaternion import Quaternion
import logging

class thrusters():
   #Thruster powers in N
   thruster_power_front = 100000.0
   thruster_power_back = 1000000.0

   #Ships current control settings
   thruster_front = 0.0
   thruster_back = 0.0

   def __init__(self, ship):
      self.ship = ship

   def simulate(self, dt):
      acceleration = np.array([0.0, 0.0, 0.0])
      acceleration[0] = (self.thruster_back * self.thruster_power_back - self.thruster_front * self.thruster_power_front) / self.ship.mass
      self.ship.velocity += acceleration * dt
      self.ship.position += self.ship.velocity * dt

   def thrust(self,data):
      try:
         val = float(data[2])
         self.thruster_back = np.clip(val, 0, 1)
         return "Back thruster set to: {0}".format(self.thruster_back)
      except:
         return "Error. Usage: thrust {float = 0.0 - 1.0}"
   
   def fthrust(self,data):
      try:
         val = float(data[2])
         self.thruster_front = np.clip(val, 0, 1)
         return "Front thruster set to: {0}".format(self.thruster_front)
      except:
         return "Error. Usage: fthrust {float = 0.0 - 1.0}"

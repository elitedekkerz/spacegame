import numpy as np
from pyquaternion import Quaternion
import logging

#game modules
import commands.radio
import commands.thrusters

class ship():
   ##Ships physical properties
   #Mass in kg
   mass = 1000000.0

   #Ships position
   position = np.array([0.0, 0.0, 0.0])
   #Vector for telling where the ship is facing
   heading = Quaternion(scalar=1.0, vector=[0.0, 0.0, 1.0]) 
   #Vector for telling  where ship is going
   velocity = np.array([0.0, 0.0, 0.0])
   thrust_acc = np.array([0.0, 0.0, 0.0])
   
   modules = {}

   def __init__(self):
      __init__(position)

   def __init__(self, position):

      self.modules = {
         "radio": commands.radio(),
         "thrust_front": commands.thrusters(self, np.array([0.0, 0.0, -10000.0])),
         "thrus_back": commands.thrusters(self, np.array([0.0, 0.0, 100000.0])),
         "echo": commands.echo(),
      }
      self.position = np.array(position)

   def simulate(self, dt):

      self.thrust_acc = np.array([0.0, 0.0, 0.0])

      for module in self.modules:
         self.modules[module].simulate(dt)

      acceleration = np.array([0.0, 0.0, 0.0])
      acceleration += self.heading.rotate(self.thrust_acc)

      self.velocity += acceleration * dt
      self.position += self.velocity * dt

   def rot(self,data):
      try:
         r = float(data[2])
         r = r / 180.0 * np.pi
         
         self.heading = Quaternion(axis=[1, 0, 0], angle=r) * self.heading
         return "rotated by: {0}".format(r)

      except:
         return "Error. Usage: rot {float}"

   def getPosition(self, args):
      return str(self.position)

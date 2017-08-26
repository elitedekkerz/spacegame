#!/usr/bin/python3
import numpy as np
from pyquaternion import Quaternion

class ship():
   position = np.array([0,0,0])
   velocity = np.array([0,0,0])

   def __init__(self, position):
      self.commands = {'echo':self.echo}
      self.position = np.array(position)
      self.velocity = np.array(0)

   def simulate(self, dt):
      
      pass

   def echo(self,data):
      return str.join(' ', data)

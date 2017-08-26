#!/usr/bin/python3
from types import *
import logging
import numpy as np
from pyquaternion import Quaternion

class ship():
   ##Ships physical properties
   #Mass in kg
   mass = 1000000.0
   #Thruster powers in N
   thruster_power_front = 100000.0
   thruster_power_back = 1000000.0

   #Ships current control settings
   thruster_front = 0.0
   thruster_back = 0.0

   #Ships position
   position = np.array([0.0, 0.0, 0.0])
   #Vector for telling where the ship is facing
   front = np.array([0.0, 0.0, 0.0])
   #Vector for telling  where ship is going
   velocity = np.array([0.0, 0.0, 0.0])

   def __init__(self):
      __init__(position)

   def __init__(self, position):
      self.commands = {
         'echo':self.echo,
         'thrust':self.thrust,
         'fthrust':self.fthrust
      }

      self.position = np.array(position)

   def simulate(self, dt):
      acceleration = np.array([0.0, 0.0, 0.0])
      acceleration[0] = (self.thruster_back * self.thruster_power_back - self.thruster_front * self.thruster_power_front) / self.mass
      self.velocity += acceleration * dt
      self.position += self.velocity * dt

   def echo(self,data):
      return str.join(' ', data)

   def thrust(self,data):
      try:
         val = float(data[0])
         self.thruster_back = np.clip(val, 0, 1)
         return "Back thruster set to: {0}".format(self.thruster_back)
      except:
         return "Error. Usage: thrust {float = 0.0 - 1.0}"
   
   def fthrust(self,data):
      try:
         val = float(data[0])
         self.thruster_front = np.clip(val, 0, 1)
         return "Front thruster set to: {0}".format(self.thruster_front)
      except:
         return "Error. Usage: fthrust {float = 0.0 - 1.0}"

class player():
   #player as a class which can send user input commands to a ship

   def __init__(self):
      self.ship = ship([0,0,0])

   #current command waiting for execution
   command = []
   def tryCommand(self):
      #don't parse if command is empty
      if not len(self.command):
         return ''

      #do command
      if self.command[0] in self.ship.commands:
         output = self.ship.commands[self.command[0]](self.command[1:])
         logging.debug("executing command %s", str.join(' ', self.command))
         #command complete, remove it so we don't re-run it next time
         self.command = []
         return output+'\n'

      return ''

   #string for collecting command
   inputString = ''
   def readInput(self, data):
      assert type(data) is str, 'data is not a string %s' % data
      for char in data:

         #command complete?
         if char == '\n':
            logging.debug("received command %s", self.inputString)
            self.command = self.inputString.split()
            self.inputString = ''

         else:
            self.inputString += char

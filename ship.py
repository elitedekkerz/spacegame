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
   front = np.array([0.0, 0.0, 0.0])
   #Vector for telling  where ship is going
   velocity = np.array([0.0, 0.0, 0.0])

   def __init__(self):
      __init__(position)

   def __init__(self, position):
      self.radio = commands.radio()
      self.thrusters = commands.thrusters(self)

      #set functionality
      self.setCommands ={
         #radio
         'radio':self.radio.set,

         #thrusters
         'thruster':self.thrusters.set,
         'thrust':self.thrusters.thrust,
         'fthrust':self.thrusters.fthrust
      }

      #get functionality
      self.getCommands ={
         #radio
         'radio':self.radio.get,

         #thrusters
         'thruster':self.thrusters.get,

         #ship info
         'position':self.getPosition
      }

      #basic commands
      self.commands = {
         'echo':self.echo,
         'set':self.setCommand,
         'get':self.getCommand,
      }

      self.position = np.array(position)

   def setCommand(self, data):
      return self.setCommands[data[1]](data)

   def getCommand(self, data):
      return self.getCommands[data[1]](data)

   def simulate(self, dt):
      self.thrusters.simulate(dt)

   def echo(self,data):
      return str.join(' ', data)

   def getPosition(self, args):
      return str(self.position)

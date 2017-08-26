import numpy as np
from pyquaternion import Quaternion

#game modules
import commands.radio

class ship():
   position = np.array([0,0,0])
   velocity = np.array([0,0,0])

   def __init__(self, position):
      self.radio = commands.radio()

      #set functionality
      self.setCommands ={
         'radio':self.radio.set
      }

      #get functionality
      self.getCommands ={
         'radio':self.radio.get
      }

      #basic commands
      self.commands = {
         'echo':self.echo,
         'set':self.setCommand,
         'get':self.getCommand
      }

      self.position = np.array(position)
      self.velocity = np.array(0)

   def setCommand(self, data):
      return self.setCommands[data[1]](data)

   def getCommand(self, data):
      return self.getCommands[data[1]](data)

   def simulate(self, dt):
      
      pass

   def echo(self,data):
      return str.join(' ', data)

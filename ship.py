import numpy as np
from pyquaternion import Quaternion

#game modules
import commands.radio

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
   heading = Quaternion(scalar=1.0, vector=[0.0, 0.0, 1.0]) 
   #Vector for telling  where ship is going
   velocity = np.array([0.0, 0.0, 0.0])

   def __init__(self):
      __init__(position)

   def __init__(self, position):
      self.radio = commands.radio()

      #set functionality
      self.setCommands ={
         'radio':self.radio.set,
         'thrust':self.thrust,
         'fthrust':self.fthrust,
         'rot':self.rot
      }

      #get functionality
      self.getCommands ={
         'radio':self.radio.get
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

      thrust_acc = np.array([0.0, 0.0, (self.thruster_back * self.thruster_power_back)  / self.mass])
      thrust_acc += np.array([0.0, 0.0, -(self.thruster_front * self.thruster_power_front)  / self.mass])

      acceleration = np.array([0.0, 0.0, 0.0])
      acceleration += self.heading.rotate(thrust_acc)

      print (thrust_acc, self.heading, self.heading.degrees, self.heading.axis, acceleration)

      self.velocity += acceleration * dt
      self.position += self.velocity * dt

   def echo(self,data):
      return str.join(' ', data)

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

   def rot(self,data):
      try:
         r = float(data[2])
         r = r / 180.0 * np.pi
         
         print (self.heading)
         print (self.heading.degrees)
         print (self.heading.norm)
         self.heading = Quaternion(axis=[1, 0, 0], angle=r) * self.heading
         print (self.heading)
         print (self.heading.degrees)
         return "rotated by: {0}".format(r)

      except:
         return "Error. Usage: rot {float}"


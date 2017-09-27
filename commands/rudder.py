import numpy as np
from pyquaternion import Quaternion
import logging

class rudder():

   def __init__(self, ship, axis_power):
      #thruster names and their values
      self.ship = ship
      #Control thrusters in array [yaw, roll, pitch]
      self.axis_power = axis_power  #Power of the control thrusters
      self.axis_set = np.array([0.0, 0.0, 0.0]) #User settting of the thruster power
      self.axis_speed = np.array([0.0, 0.0, 0.0]) #Current rotation speed in radians/s
      self.dampening_p = 0 #Proportional part of dampening. TODO: Should this be debug only?

   def parse(self, args):
      commands = {
         "yaw":self.yaw,
         "roll":self.roll,
         "pitch":self.pitch,
         "get":self.get,
         "heading":self.heading,
         "speed":self.speed,
         "damp":self.setDampening,
      }
      try:
         return commands[args[1]](args)
      except:
         return "Error. Usage: rudder {yaw/roll/pitch} {float = -1.0 ... 1.0}"

   def simulate(self, dt, power_factor):

      #If no rotation is set go dampening mode 
      if(np.linalg.norm(self.axis_set) < 0.0001 and self.dampening_p != 0):
         damp_set = -np.clip(self.axis_speed, -1.0, 1.0) * self.dampening_p
         acc = (self.axis_power * damp_set) / (self.ship.mass * 100)
      else:
         #axial accelration: a = F/(mr), assume ship is sphere with 100 radius
         acc = (self.axis_power * self.axis_set) / (self.ship.mass * 100)

      self.axis_speed += acc * dt
      axis_pos = self.axis_speed * dt
      rot = Quaternion(axis = [1, 0, 0], radians = axis_pos[0])   #yaw
      rot *= Quaternion(axis = [0, 0, 1], radians = axis_pos[1])  #roll
      rot *= Quaternion(axis = [0, 1, 0], radians = axis_pos[2])  #pitch
      self.ship.heading = rot * self.ship.heading
      

   def yaw(self, args):
      try:
         self.axis_set[0] = np.clip(float(args[2]), -1, 1)
         return "yaw set to: {0}".format(self.axis_set[0])
      except:
         logging.exception("exception when setting yaw value")
         return "Error. Usage: rudder yaw {float = -1.0 ... 1.0}"

   def roll(self, args):
      try:
         self.axis_set[1] = np.clip(float(args[2]), -1, 1)
         return "roll set to: {0}".format(self.axis_set[1])
      except:
         logging.exception("exception when setting roll value")
         return "Error. Usage: rudder roll {float = -1.0 ... 1.0}"
   
   def pitch(self, args):
      try:
         self.axis_set[2] = np.clip(float(args[2]), -1, 1)
         return "pitch set to: {0}".format(self.axis_set[2])
      except:
         logging.exception("exception when setting pitch value")
         return "Error. Usage: rudder pitch {float = -1.0 ... 1.0}"

   def get(self, args):
      return "yaw: {0}, roll: {1}, pitch: {2}".format(self.axis_set[0], self.axis_set[1], self.axis_set[2])

   def heading(self, args):
      heading_vect = self.ship.heading.rotate([0.0, 0.0, 1.0])
      return "heading {0}".format(heading_vect)

   def speed(self, args):
      return "speed {0}".format(self.axis_speed)

   def setDampening(self, args):
      try:
         self.dampening_p = float(args[2])
         return "dampening set to: {0}".format(self.dampening_p)
      except:
         logging.exception("exception when setting rudder value")
         return "Error. Usage: rudder damp {float >= 0.0 }"
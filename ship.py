import numpy as np
from pyquaternion import Quaternion
import logging
from space_coordinate import space_coordinate as sc

#game modules
import commands.radio
import commands.thrusters

logger = logging.getLogger('ship')

class ship():
   ##Ships physical properties
   #Mass in kg
   mass = 1000000.0
   name = 'Восток'

   #Ships position
   position = sc([0, 0, 0])
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
         "thrust_back": commands.thrusters(self, np.array([0.0, 0.0, 100000.0])),
         "rudder": commands.rudder(self, np.array([100000.0, 100000.0, 100000.0])),
         "echo": commands.echo(),
         "ship": commands.ship_info(self),
         "log": commands.log(),
         "time": commands.timer(),
      }
      self.position = sc(position)

   def parse(self, args):
      logger.debug('forwarding command %s', str(args))
      reply = self.modules[args[0]].parse(args)
      logger.debug('received data %s', reply)
      return reply

   def simulate(self, dt):

      self.thrust_acc = np.array([0.0, 0.0, 0.0])

      for module in self.modules:
         self.modules[module].simulate(dt)

      acceleration = np.array([0.0, 0.0, 0.0])
      acceleration += self.heading.rotate(self.thrust_acc)

      self.velocity += acceleration * dt
      dpos = self.velocity * dt
      self.position += dpos

import numpy as np
import logging
from space_coordinate import space_coordinate as sc
from gameObject import gameObject

#game modules
import commands.radio
import commands.thrusters

logger = logging.getLogger('ship')

class ship(gameObject):
   ##Ships physical properties

   name = 'Восток'

   #Vector for telling  where ship is going
   velocity = np.array([0.0, 0.0, 0.0])
   thrust_acc = np.array([0.0, 0.0, 0.0])
   
   modules = {}

   def __init__(self, position = sc([0, 0, 0])):
      self.modules = {
         "radio": commands.radio(),
         "thrust_front": commands.thrusters(self, np.array([0.0, 0.0, -100000.0])),
         "thrust_back": commands.thrusters(self, np.array([0.0, 0.0, 500000.0])),
         "rudder": commands.rudder(self, np.array([100000.0, 100000.0, 100000.0])),
         "echo": commands.echo(),
         "ship": commands.ship_info(self),
         "log": commands.log(),
         "time": commands.timer(),
         "radar": commands.radar(self),
         "crew": commands.crew(self),
         "generator": commands.generator(self, 25000000)
      }
      super().__init__("ship", position)

   def parse(self, args):
      logger.debug('forwarding command %s', str(args))
      try:
         reply = self.modules[args[0]].parse(args)
      except:
         logging.exception("exception when executing module: " + str(args[0]) + " with arguments:" + str(args[1:]))

      logger.debug('received data %s', reply)
      return reply

   def simulate(self, dt):

      self.thrust_acc = np.array([0.0, 0.0, 0.0])
      power_factor = self.calc_power()

      for module in self.modules:
         self.modules[module].simulate(dt, power_factor)

      acceleration = np.array([0.0, 0.0, 0.0])
      acceleration += self.heading.rotate(self.thrust_acc)

      self.velocity += acceleration * dt
      dpos = self.velocity * dt
      self.position += sc(dpos)

   def calc_power(self):
      self.power_generated = 0
      self.power_needed = 0

      #Get power needs and power generation form all modules
      for module in self.modules:
         try:
            self.power_generated += self.modules[module].getPowerGenerated()
         except:
            pass
         try:
            self.power_needed += self.modules[module].getPowerNeeded()
         except:
            pass

      #If we generate more power than is needed all modules can run in full power.
      #Else we calculate multiplier to limit the modules functionality
      if self.power_needed < self.power_generated:
         return 1.0
      else:
         return self.power_generated / self.power_needed
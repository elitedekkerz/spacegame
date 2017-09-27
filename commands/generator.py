import logging

logger = logging.getLogger('generator')

class generator():
   def __init__(self, ship, power):
      #Maximum power generated in watts
      self.max_power_output = power
      self.reactor_level = 0.5 

   def parse(self, args):
      commands = {
      "":self.get,
      "set":self.set,
      }
      try:
         return commands[args[1]](args)
      except:
         logger.debug('incorrect command %s', str.join(' ', args))
         return self.help()

   def set(self, args):
      try:
         self.reactor_level = np.clip(float(args[2]), 0 , 1)
      except:
         return self.help()

      logger.info("rector set to %s", self.volume)
      return ""

   def get(self, args):
      logger.debug('rector info requested')
      reply = "Reactor is set to %.0f" % self.reactor_level
      reply += " and generates %.2f MW of power." %  self.reactor_level * self.max_power_output
      return reply

   def help(self):
      return "Error. Usage: generator <set> <value>"

   def simulate(self, dt, power_factor):
      pass
   
   def getPowerGenerated(self):
      return self.reactor_level * self.max_power_output

import logging

class radio():
   def __init__(self):
      self.volume = 0

   def set(self, args):
      self.volume = int(args[2])
      logging.info("cranked the radio to %s", self.volume)
      return ''

   def get(self, args):
      return str(self.volume)

   def simulate(self,dt):
      pass

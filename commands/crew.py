import logging
logger = logging.getLogger('crew')

class crew():
   def __init__(self, ship):
      self.ship = ship
      self.ship.crew = []

   def simulate(self, dt):
      pass

   def parse(self, args):
      try:
         if args[1] == 'list':
            reply = ''
            for member in self.ship.crew:
               reply += member.name+'\n'
            return reply
         return self.help()
      except:
         logger.exception('unable to parse')
         return self.help()

   def help(self):
      return "Error. usage: crew list"

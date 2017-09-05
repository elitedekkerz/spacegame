#return received arguments excluding the first one
class ship_info():
   def __init__(self, ship):
      self.ship = ship

   def parse(self, args):
      commands = {
      "position":self.getPosition,
      }
      try:
         return commands[args[1]](args)
      except:
         return "Error. Usage: ship position"

   def simulate(self, dt):
      pass

   def getPosition(self, args):
      return str(self.ship.position)
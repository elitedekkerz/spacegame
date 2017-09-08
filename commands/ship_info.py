#return received arguments excluding the first one
class ship_info():
   def __init__(self, ship):
      self.ship = ship

   def parse(self, args):
      commands = {
      "position":self.getPosition,
      "velocity":self.getVelocity,
      }
      try:
         return commands[args[1]](args)
      except:
         return "Error. Usage: ship position/velocity"

   def simulate(self, dt):
      pass

   def getPosition(self, args):
      return str(self.ship.position)

   def getVelocity(self, args):
      return str(self.ship.velocity)
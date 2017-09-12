
#import server
import gameObject
import logging

#return received arguments excluding the first one
class radar():

   #Scan distance of the radar 
   range = 30000

   def __init__(self, ship):
      self.ship = ship

   def parse(self, args):
      commands = {
      "scan":self.scan,
      }
      try:
         return commands[args[1]](args)
      except:
         logging.exception('Radar exception')
         return "Error. Usage: radar scan"

   def simulate(self, dt):
      pass

   def scan(self, args):
      result = ""

      for obj in gameObject.objects:
         if obj.getDistanceTo(self.ship) < self.range: 
            result += str(obj) + "\n"
      return result
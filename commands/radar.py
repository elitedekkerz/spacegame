import math

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
         return("Error. Usage: radar scan\n"
                "output format:\n"
                "identifier: <range>(meters) <elevation>(degrees) <azimuth>(degrees)\n")

   def simulate(self, dt):
      pass

   def scan(self, args):
      found_objects = []

      for obj in gameObject.objects:
         if obj.getDistanceTo(self.ship) < self.range: 
            if obj != self.ship:
               found_objects.append(obj) 

      found_objects.sort(key=lambda tup: tup.getDistanceTo(self.ship))

      result = ""
      for i in found_objects:
         dist, azimuth, inclination = self.ship.getSphericalCoordinateTo(i, inDeg = True)
         result += "{}: {:06.3E} {:+06.1f} {:+06.1f}\n".format(i.identifier, dist, azimuth, inclination)

      return result

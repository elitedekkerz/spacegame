import math
import numpy as np

#import server
import gameObject
import logging

#return received arguments excluding the first one
class radar():

   #Scan distance of the radar 
   range = 30000
   sector = 180

   def __init__(self, ship):
      self.ship = ship

   def parse(self, args):
      commands = {
      "scan":self.scan,
      "sector":self.setSector,
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

      eff_range = self.range * (180 / self.sector)

      for obj in gameObject.objects:
         if obj.getDistanceTo(self.ship) < eff_range and self.ship.getAngleTo(obj, True) < self.sector: 
            if obj != self.ship:
               found_objects.append(obj) 

      found_objects.sort(key=lambda tup: tup.getDistanceTo(self.ship))

      result = ""
      for i in found_objects:
         dist, azimuth, inclination = self.ship.getSphericalCoordinateTo(i, inDeg = True)
         result += "{}: {:06.3E} {:+06.1f} {:+06.1f}\n".format(i.identifier, dist, azimuth, inclination)

      return result

   def setSector(self, args):
      try:
         self.sector = np.clip(float(args[2]), 0, 180)
         return "sector set to: {0}".format(self.sector)
      except:
         logging.exception("exception when setting secotr value")
         return "Error. Usage: radar sector {float = 0.0 ... 180.0}"
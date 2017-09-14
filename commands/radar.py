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
               dPos = obj.position - self.ship.position
               x = dPos.position[0]
               y = dPos.position[1]
               z = dPos.position[2]
               class info:
                  identifier = obj.identifier
                  elevation = math.atan2(z,math.sqrt(x**2+y**2))*180/math.pi
                  azimuth = math.atan2(y,x)*180/math.pi
                  distance = abs(dPos)
               found_objects.append(info) 

      found_objects.sort(key=lambda tup: tup.distance)

      result = ""
      for i in found_objects:
         result += "{}: {:06.3E} {:+06.1f} {:+06.1f}\n".format(i.identifier, i.distance, i.azimuth, i.elevation)

      return result

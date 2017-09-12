
import numpy as np
import logging
from space_coordinate import space_coordinate as sc

id_count = 0
objects = []

class gameObject():
   position = sc([0, 0, 0])
   identifier = ""

   def __init__(self, id_prefix, pos = sc([0, 0, 0])):
      global id_count
      if type(pos) == sc:
         self.position = pos
      else:
         self.position = sc(pos)

      self.identifier = id_prefix + "-" + "%06i"%id_count
      id_count += 1
      global objects
      objects.append(self)
      logging.info("New object: " + str(self))

   def getPosition(self):
      return self.position
   
   def getDistanceTo(self, target):
      return abs(target.position - self.position)

   def getAngleTo(self,target):
      dot = np.vdot(self.position.position, self.position.position)
      return dot / (self.position.abs * self.position.abs) 

   def __str__(self):
      return self.identifier + ", " + str(self.position)
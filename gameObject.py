
import numpy as np
import logging
from pyquaternion import Quaternion
from space_coordinate import space_coordinate as sc

id_count = 0
objects = []

class gameObject():
   position = sc([0, 0, 0])
   identifier = ""

   #Vector for telling where the object is facing
   heading = Quaternion() #(scalar=1.0, vector=[0.0, 0.0, 1.0]) 

   def __init__(self, id_prefix, pos = sc([0, 0, 0]), mass = 100000.0):
      global id_count
      if type(pos) == sc:
         self.position = pos
      else:
         self.position = sc(pos)

      self.identifier = id_prefix + "-" + "%06i"%id_count
      self.mass = mass
      id_count += 1
      global objects
      objects.append(self)
      logging.info("New object: " + str(self))

   def __str__(self):
      return self.identifier + ", " + str(self.position)

   def remove(self):
      global objects
      objects.remove(self)
      logging.info("object removed: " + str(self))

   def getPosition(self):
      return self.position
   
   def getDistanceTo(self, target):
      return abs(target.position - self.position)

   def getAngleTo(self, target, inDeg = False):
      #Move target position to ships origo
      lpos = target.position - self.position
      #Calculate the heading vector
      heading_vect = self.heading.rotate([0.0, 0.0, 1.0])

      dot = np.vdot(heading_vect, lpos.getPosition())
      angle = np.arccos(dot / abs(lpos))
      if inDeg:
         angle *= 180 / np.pi

      return angle

   def getSphericalCoordinateTo(self, target, inDeg = False):

      #Move target position to ships origo
      lpos = target.position - self.position
      #Move the target to local coordinate
      ltarget = self.heading.rotate(lpos.getPosition())
      x, y, z = ltarget

      distance = abs(lpos)
      inclination = np.arccos(x / distance) - np.pi / 2
      azimuth = np.arctan2(y, z)

      if inDeg:
         inclination *= 180 / np.pi
         azimuth *= 180 / np.pi

      return distance, azimuth, inclination

   def getHeading(self):
      return self.heading.rotate([0.0, 0.0, 1.0])
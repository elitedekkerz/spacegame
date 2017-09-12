
import numpy as np

# Class to implement standard coorinate system.
# It's basic class with operation overloading to convert data types

class space_coordinate():

   position = np.array([0, 0, 0], dtype=np.int64)

   def __init__(self, position = [0, 0, 0]):
      tmp = np.array(position) * 1000
      self.position = tmp.astype(np.int64) 

   def __repr__(self):
      return repr(self.position / 1000.0)
   
   def __str__(self):
      return str(self.position / 1000.0)


   def __add__(self, other):
      tmp = space_coordinate()
      if isinstance(other, space_coordinate):
         tmp.position = self.position + other.position
      else:
         tmp.position = self.position + (other * 1000.0).astype(np.int64) 
      return tmp

   def __sub__(self, other):
      tmp = space_coordinate()
      if isinstance(other, space_coordinate):
         tmp.position = self.position - other.position
      else:
         tmp.position = self.position - (other.position * 1000.0).astype(np.int64) 
      return tmp

   def __radd__(self, other):  
      return __add__(self, other)

   def __rsub__(self, other):
      tmp = space_coordinate()
      if isinstance(other, space_coordinate):
         tmp.position = other.position - self.position
      else:
         tmp.position = (other.position * 1000.0).astype(np.int64) - self.position
      return tmp

   def __iadd__(self, other):
      if isinstance(other, space_coordinate):
         self.position = self.position + other.position
      else:
         self.position = self.position + (other.position * 1000.0).astype(np.int64) 
      return self

   def __isub__(self, other):
      if isinstance(other, space_coordinate):
         self.position = self.position - other.position
      else:
         self.position = self.position - (other.position * 1000.0).astype(np.int64) 
      return self

   def __abs__(self):
      return np.linalg.norm(self.position) / 1000
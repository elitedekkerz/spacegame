
import numpy as np

# Class to implement standard coorinate system.
# It's basic class with operation overloading to convert data types

class space_coordinate():

   position = np.array([0, 0, 0], dtype=np.int64)

   def __init__(self):
      __init__([0, 0, 0])

   def __init__(self, position):
      position = np.array(position, dtype=np.int64)
   
   def __repr__(self):
      return repr(self.position / 1000.0)
   
   def __str__(self):
      return str(self.position / 1000.0)


   def __add__(self, other):
      if isinstance(other, space_coordinate):
         return self.position + other
      else:
         return self.position + (other * 1000.0).astype(np.int64) 

   def __sub__(self, other):
      if isinstance(other, space_coordinate):
         return self.position - other
      else:
         return self.position - (other * 1000.0).astype(np.int64) 

   def __radd__(self, other):  
      return __add__(self, other)

   def __rsub__(self, other):
      if isinstance(other, space_coordinate):
         return other - self.position
      else:
         return (other * 1000.0).astype(np.int64) - self.other

   def __iadd__(self, other):
      if isinstance(other, space_coordinate):
         self.position = self.position + other
      else:
         self.position = self.position + (other * 1000.0).astype(np.int64) 
      return self

   def __isub__(self, other):
      if isinstance(other, space_coordinate):
         self.position = self.position - other
      else:
         self.position = self.position - (other * 1000.0).astype(np.int64) 
      return self
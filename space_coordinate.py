
import numpy as np

# Class to implement standard coorinate system.
# It's basic class with operation overloading to convert data types

class space_coordinate():
   def getPosition(self):
      return self.__position / 1000.0

   def __init__(self, position = [0, 0, 0]):
      if type(position) == space_coordinate:
        self.__position = position
      else:
        tmp = np.array(position) * 1000
        self.__position = tmp.astype(np.int64) 

   def __repr__(self):
      return repr(self.__position / 1000.0)
   
   def __str__(self):
      return str(self.__position / 1000.0)


   def __add__(self, other):
      tmp = space_coordinate()
      if isinstance(other, space_coordinate):
         tmp.__position = self.__position + other.__position
      else:
         tmp.__position = self.__position + (other * 1000.0).astype(np.int64) 
      return tmp

   def __sub__(self, other):
      tmp = space_coordinate()
      if isinstance(other, space_coordinate):
         tmp.__position = self.__position - other.__position
      else:
         tmp.__position = self.__position - (other.__position * 1000.0).astype(np.int64) 
      return tmp

   def __radd__(self, other):  
      return __add__(self, other)

   def __rsub__(self, other):
      tmp = space_coordinate()
      if isinstance(other, space_coordinate):
         tmp.__position = other.__position - self.__position
      else:
         tmp.__position = (other.__position * 1000.0).astype(np.int64) - self.__position
      return tmp

   def __abs__(self):
      return np.linalg.norm(self.__position) / 1000.0
from types import *
import logging
import ship

logger = logging.getLogger('player')

class player():
   #player as a class which can send user input commands to a ship

   #string for collecting command
   inputString = ''
   def readInput(self, data):
      assert type(data) is str, 'data is not a string %s' % data
      for char in data:
         #command complete?
         if char == '\n':
            args = self.inputString.split()
            self.inputString = ''
            logger.debug("constructed command %s", str(args))
            return {'command':args}

         else:
            self.inputString += char

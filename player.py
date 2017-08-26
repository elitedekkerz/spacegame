from types import *
import logging
import ship

class player():
   #player as a class which can send user input commands to a ship

   def __init__(self):
      self.ship = ship.ship([0,0,0])

   #current command waiting for execution
   command = []
   def tryCommand(self):
      #don't parse if command is empty
      if not len(self.command):
         return ''

      #do command
      if self.command[0] in self.ship.commands:
         output = self.ship.commands[self.command[0]](self.command)
         logging.debug("executing command %s", str.join(' ', self.command))
         #command complete, remove it so we don't re-run it next time
         self.command = []
         return output+'\n'

      return ''

   #string for collecting command
   inputString = ''
   def readInput(self, data):
      assert type(data) is str, 'data is not a string %s' % data
      for char in data:

         #command complete?
         if char == '\n':
            logging.debug("received command %s", self.inputString)
            self.command = self.inputString.split()
            self.inputString = ''

         else:
            self.inputString += char

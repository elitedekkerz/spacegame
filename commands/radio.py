import logging

logger = logging.getLogger('radio')

class radio():
   def __init__(self):
      self.volume = 0

   def parse(self, args):
      commands = {
      "set":self.set,
      "get":self.get,
      "on":self.on,
      "off":self.off,
      }
      try:
         return commands[args[1]](args)
      except:
         logger.debug('incorrect command %s', str.join(' ', args))
         return self.help()

   def on(self,args):
      return self.set(['','','0.3'])

   def off(self,args):
      return self.set(['','','0'])

   def set(self, args):
      #get the new volume
      try:
         newVolume = float(args[2])
      except:
         return self.help()

      #do some fancy calculations
      volumeDifference = newVolume - self.volume
      self.volume = newVolume
      reply = 'The radio is now a little '
      if volumeDifference > 0:
         reply += 'louder.'
      elif volumeDifference < 0:
         reply += 'quieter.'
      else:
         reply = 'You try to adjust the radio, but nothing happens.'

      logger.info("volume set to %s", self.volume)
      return reply

   def get(self, args):
      logger.debug('volume info requested')
      reply = 'the radio is '
      if self.volume > 1:
         reply += 'on fire'
      elif self.volume > 0.5:
         reply += 'on loud'
      elif self.volume > 0:
         reply += 'on'
      elif self.volume <0:
         reply += 'possibly broken'
      else:
         reply += 'off'
      return reply

   def help(self):
      logger.info('who doesn\'t know how to work a radio?')
      return "Error. Usage: radio <set/get/on/off> <value>"

   def simulate(self, dt, power_factor):
      pass

   def getPowerNeeded(self):
      #The bass needs its power 
      return 10 ** (7 ** self.volume)
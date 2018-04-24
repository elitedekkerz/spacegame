
"""radio

Usage:
  radio on
  radio off
  radio get
  radio set <volume>
"""

import logging
import player

class radio():
    def __init__(self):
        self.log = logging.getLogger("radio")
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
            self.log.info("Unknown command given: {}".format(' '.join(args)))
            return self.usage()

    def on(self,args):
        return self.set(['','','0.3'])

    def off(self,args):
        return self.set(['','','0'])

    def set(self, args):
        #get the new volume
        try:
            newVolume = float(args[2])
        except:
            self.log.info('who doesn\'t know how to work a radio?')
            return player.response.ok, "Radio 'set' function needs one argumet as float"

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

        self.log.info("volume set to %s", self.volume)
        return player.response.ok, reply

    def get(self, args):
        self.log.debug('volume info requested')
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
        return player.response.ok, reply

    def usage(self):
        return player.response.usage, self.__doc__

    def simulate(self, dt, power_factor):
        pass

    def getPowerNeeded(self):
        #The bass needs its power 
        return 10 ** (7 ** self.volume)

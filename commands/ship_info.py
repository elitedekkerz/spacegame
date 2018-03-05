

import numpy as np
import logging
from space_coordinate import space_coordinate as sc
import player

#return received arguments excluding the first one
class ship_info():
    def __init__(self, ship):
        self.log = logging.getLogger("ship_info")
        self.ship = ship

    def parse(self, args):
        commands = {
        "position":self.getPosition,
        "velocity":self.getVelocity,
        "heading":self.getHeading,
        "power":self.getPower,
        "cheat":self.getCheatInfo,
        }
        try:
            return commands[args[1]](args)
        except:
            self.log.info("Unknown command given: {}".format(' '.join(args)))
            return self.help()

    def getCheatInfo(self, args):
        reply = ''
        values = {
            'position':self.ship.position,
            'velocity':self.ship.velocity,
            'heading':self.ship.heading,
            'acceleration':self.ship.getAcceleration()
            }      
        for name, value in values.items():
            reply += name + ': ' + str(value) + '\n'
        return player.response.ok, reply

    def simulate(self, dt, power_factor):
        pass

    def getPosition(self, args):
        return player.response.ok, str(self.ship.position)

    def getVelocity(self, args):
        return player.response.ok,  str(self.ship.velocity)
        
    def getHeading(self, args):
        try:
          return player.response.ok, str(self.ship.heading.rotate(np.array([0.0, 0.0, 1.0])))
        except:
          self.log.exception("Heading")

    def getPower(self, args):
        return player.response.ok, str(self.ship.power_needed / 1000) + "/" + str(self.ship.power_generated / 1000) + " kW"

    def help(self):
        usage = (
            "ship position\n"
            "ship velocity\n"
            "ship heading\n"
            "ship power\n"
        )
        return player.response.usage, usage
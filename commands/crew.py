import logging
import player

class crew():
    def __init__(self, ship):
        self.log = logging.getLogger("crew")
        self.ship = ship
        self.ship.crew = []

    def simulate(self, dt, power_factor):
        pass

    def parse(self, args):
        try:
            if args[1] == 'list':
                reply = ''
                for member in self.ship.crew:
                    reply += member.name+'\n'
                return player.response.ok, reply
            return self.help()
        except:
            self.log.exception('unable to parse')
            return self.help()

    def help(self):
        return player.response.usage,  "crew list"

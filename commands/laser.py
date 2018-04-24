import logging
import numpy as np
import items
import player
import gameObject

class laser():
    def __init__(self, ship):
        self.log = logging.getLogger("laser")

        self.ship = ship
        self.charge = 0
        self.charge_rate = 0
        self.max_charge_rate = 1000000000 # 100 MW
        self.full_charge = 50000000000 # 50 GJ

    def parse(self, args):
        commands = {
        "fire": self.fire,
        "charge": self.charge_cmd,
        "status": self.status,
        }
        try:
            return commands[args[1]](args)
        except:
            self.log.info("Unknown command given: {}".format(' '.join(args)))
            return self.help()

    def fire(self, args):
        try:
            target = next(x for x in gameObject.objects if x.identifier == args[2])
        except:
            return self.help()

        if target == self.ship:
            return player.response.ok, "The turret likes the crew of this ship and refusese to shoot itself."

        halfing_distance = 1000 # Power of the laser will half every 1 km
        distance = self.ship.getDistanceTo(target)
        times_halved = distance / halfing_distance
        power = self.charge / 2 ** times_halved

        try:
            ret = target.hit(self.ship, power)
            return player.response.ok, ret
        except:
           return player.response.ok, "Laser hits target with {} J of energy, but nothing happens.".format(power)

    def status(self, args):
        charge_lvl = self.charge / self.full_charge * 100
        return player.response.ok, "Laser is charged to {:.0f} %.".format(charge_lvl)

    def charge_cmd(self, args):
        try:
            rate = np.clip(float(args[2]), 0, 100)
            self.charge_rate = (rate / 100.0) * self.max_charge_rate
            return player.response.ok, "Laser charge rate is set to {:.0f} % and is using {:.0f} J/s".format(rate, self.charge_rate)

        except:
            return self.help 

    def help(self):
        usage = (
            "laser fire <target>\n"
            "laser charge <percentage>\n"
            "laser status\n"
        )
        return player.response.usage, usage

    def getPowerNeeded(self):
        return self.charge_rate

    def simulate(self, dt, power_factor):
        self.charge += self.charge_rate * dt * power_factor
        if(self.charge > self.full_charge):
            self.charge = self.full_charge
            self.charge_rate = 0

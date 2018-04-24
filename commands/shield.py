import logging
import numpy as np
import items
import player
import gameObject

class shield():
    def __init__(self, ship):
        self.log = logging.getLogger("shield")
        self.ship = ship
        self.charge = 0
        self.charge_rate = 0
        self.max_charge_rate = 1000000000 # 100 MW
        self.full_charge = 50000000000 # 50 GJ
        self.upkeep = 100000 #kW

    def parse(self, args):
        commands = {
        "charge": self.charge_cmd,
        "status": self.status,
        }
        try:
            return commands[args[1]](args)
        except:
            self.log.info("Unknown command given: {}".format(' '.join(args)))
            return self.help()


    def status(self, args):
        shield_lvl = self.charge / self.full_charge * 100
        resp = "Shield is at {:.0f} %% and is using {:.0f} W of power.\n".format(shield_lvl, self.power - self.heat_energy)
        resp += "The rest {} W is turned to heat.".format(self.heat_energy)
        return player.response.ok, resp

    def charge_cmd(self, args):
        try:
            charge_rate = np.clip(float(args[2]), 0, 100)
            self.charge_rate = (charge_rate / 100.0) * self.max_charge_rate
            return player.response.ok, "Shield charge rate is set to {:.0f} %. That gives shields {:.0f} W of power.".format(charge_rate, self.charge_rate)
        except:
            return self.help 

    def help(self):
        usage = (
            "shield charge <percentage>\n"
            "shield status\n"
        )
        return player.response.usage, usage

    def getPowerNeeded(self):
        return self.charge_rate

    def simulate(self, dt, power_factor):
        self.power = self.charge_rate * power_factor
        self.charge += self.power * dt
        self.charge -= self.upkeep * dt
        self.heat_energy = 0
        if(self.charge > self.full_charge):
            self.heat_energy = (self.charge - self.full_charge) / dt
            self.charge = self.full_charge
        
        if(self.charge < 0):
            self.charge = 0

    def hit(self, power):
        self.charge -= power
        if self.charge < 0:
            self.charge = 0
        
        return self.charge / self.full_charge
import logging
import player
import numpy as np

class reactor():
    def __init__(self, ship, power):
        self.log = logging.getLogger("reactor")
        #Maximum power generated in watts
        self.max_power_output = power
        self.reactor_level = 0.0
        self.ship = ship
        #Fuel rate is kg of uranium used to get 1 MW of power
        self.fuel_rate = 0.00001

    def parse(self, args):
        commands = {
        "status":self.get,
        "set":self.set,
        }
        try:
            return commands[args[1]](args)
        except:
            self.log.info("Unknown command given: {}".format(' '.join(args)))
            return self.help()

    def set(self, args):
        try:
            new_level = np.clip(float(args[2]), 0 , 1)
        except:
            return self.help()

        if new_level == 0:
            if self.reactor_level == 0:
                self.reactor_level = 0
                return player.response.ok, "Reactor is already off."
            else:
                self.reactor_level = 0
                return player.response.ok, "Reactor slowly grinds to a halt."

        slots = self.ship.inventory.find("uranium")
        if len(slots) == 0:
            return player.response.ok, "Can't turn on the reactor. You are out of uranium."

        self.reactor_level = new_level

        self.log.info("Rector is set to %s", self.reactor_level)
        return player.response.ok, "reactor is now set to {:.0f} %.".format(new_level * 100.0)

    def get(self, args):
        self.log.debug('rector info requested')

        slots = self.ship.inventory.find("uranium")
        if len(slots) == 0:
            return player.response.ok, "Reactor is out of fuel."

        if self.reactor_level == 0:
            return player.response.ok, "Reactor is offline."

        reply = "Reactor is running at {:.0f} %".format(self.reactor_level * 100.0)
        power = (self.reactor_level * self.max_power_output / 1000)
        uranium = self.fuel_rate * (power / 1000) 
        reply += " and generates {:.0f} kW of power by using {:.3f} grams of uranium per second.".format(power, uranium * 1000)
        return player.response.ok, reply

    def help(self):
        usage = (
            "reactor set <value>\n"
            "reactor status\n"
        )

        return player.response.usage, usage

    def simulate(self, dt, power_factor):
        slots = self.ship.inventory.find("uranium")
        if len(slots) == 0:
            self.reactor_level = 0

        power = (self.reactor_level * self.max_power_output / 1000000)
        uranium_needed = self.fuel_rate * power * dt
        uranium_taken = 0

        for slot in slots:
            item = self.ship.inventory.take_from_slot(slot, uranium_needed - uranium_taken)
            uranium_taken += item.count

        if uranium_needed < uranium_taken:
            self.reactor_level = 0
    
    def getPowerGenerated(self):
        return self.reactor_level * self.max_power_output

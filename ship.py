import numpy as np
import logging
from space_coordinate import space_coordinate as sc
from gameObject import gameObject

#game modules
import commands.radio
import commands.thrusters
import items

logger = logging.getLogger('ship')

class ship(gameObject):
    def __init__(self, position = sc([0, 0, 0])):
        super().__init__("ship", position)
        self.modules = {
            "radio": commands.radio(),
            "thruster": commands.thrusters(self),
            "rudder": commands.rudder(self, np.array([100000.0, 100000.0, 100000.0])),
            "ship": commands.ship_info(self),
            "log": commands.log(),
            "time": commands.timer(),
            "radar": commands.radar(self),
            "crew": commands.crew(self),
            "reactor": commands.reactor(self, 1000000000),
            "cargo" : commands.cargo(self),
            "laser": commands.laser(self),
            "shield": commands.shield(self),
        }

        self.name = 'Восток'
        self.inventory.insert(items.item("uranium", 10.0))

        #Vector for telling  where ship is going
        self.velocity = np.array([0.0, 0.0, 0.0])
        self.thrust_acc = np.array([0.0, 0.0, 0.0])
  

    def simulate(self, dt):
            
        self.thrust_acc = np.array([0.0, 0.0, 0.0])
        power_factor = self.calc_power()

        for module in self.modules:
            self.modules[module].simulate(dt, power_factor)

        self.velocity += self.getAcceleration() * dt
        dpos = self.velocity * dt
        self.position += sc(dpos)

    def calc_power(self):
        self.power_generated = 0
        self.power_needed = 0

        #Get power needs and power generation form all modules
        for module in self.modules:
            try:
                self.power_generated += self.modules[module].getPowerGenerated()
            except:
                pass
            try:
                self.power_needed += self.modules[module].getPowerNeeded()
            except:
                pass

        #If we generate more power than is needed all modules can run in full power.
        #Else we calculate multiplier to limit the modules functionality
        if self.power_needed < self.power_generated:
            return 1.0
        else:
            return self.power_generated / self.power_needed

    def get_mass(self):
        return self.inventory.get_mass() + 100000

    def getAcceleration(self):
        return self.heading.rotate(self.thrust_acc)
    
    def destroy(self):
        logger.info("Ship {} has been destroyed".format(self.name))

        for player in self.crew:
            player.client.sendMessage("Your ship has been destroyed")
            player.client.stop()

        self.remove()

    def hit(self, source, power):
        ret = "{} got hit with {:.0E} J of energy from {}.\n".format(self.identifier, power, source.identifier)
        logger.info(ret)

        shield = 0
        try:
            shield = self.modules["shield"].hit(power)
        except:
            pass

        if shield == 0:
            self.destroy()
            return  "Your laser goes trough {} shields and penetrates its hull. The target is destoryed".format(self.identifier)
        else:
            return "The hit is absorbed by the ships shield. Their shield is now at {:.0f} %.".format(shield)

    def print_help(self, msg):
        msg = "Modules:\n"
        for module in self.modules:
            msg += module + "\n"

        return msg

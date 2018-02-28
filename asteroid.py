import numpy as np
import logging
from space_coordinate import space_coordinate as sc
from gameObject import gameObject
import items


logger = logging.getLogger('asteroid')

class asteroid(gameObject):
    def __init__(self, position = sc([0, 0, 0])):
        super().__init__("ast", position)

        self.velocity = np.array([0.0, 0.0, 0.0])
        self.thrust_acc = np.array([0.0, 0.0, 0.0])

        self.inventory.insert(items.item("ice", np.random.rand() * 100000.0)) 
        self.inventory.insert(items.item("iron", np.random.rand() * 1000.0))
        self.inventory.insert(items.item("gold", np.random.rand() * 1000.0))
        self.inventory.insert(items.item("stone", np.random.rand() * 100000.0))
        self.inventory.insert(items.item("uranium", np.random.rand() * 10.0))

    def simulate(self, dt):
            
        self.thrust_acc = np.array([0.0, 0.0, 0.0])

        acceleration = self.heading.rotate(self.thrust_acc)

        self.velocity += acceleration * dt
        dpos = self.velocity * dt
        self.position += sc(dpos)

    def hit(self, source, power):
        ret = "Asteroid {} got hit with {:.0E} J of energy from {}.\n".format(self.identifier, power, source.identifier)
        logger.debug(ret)

        hit = power / self.get_mass()
        logger.debug("Hit = {}".format(hit))

        if hit > 10:
            for slot in self.inventory:
                loot = slot.split(slot.count * (hit / 100.0))
                source.inventory.insert(loot)

        if hit < 10:
            ret += "Laser was too weak to pentrate the surface of the asteroid."
        elif hit < 50:
            ret += "Small chunk broke from the asteroid."
        elif hit < 100:
            ret += "Half of the asteroid is now missing."
        else:
            ret += "The whole asteroid pulverized in instant."
            self.remove()

        return ret
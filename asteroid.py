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

        self.inventory.insert(items.item("ice", np.random.rand() * 100000)) 
        self.inventory.insert(items.item("iron", np.random.rand() * 1000))
        self.inventory.insert(items.item("gold", np.random.rand() * 1000))
        self.inventory.insert(items.item("stone", np.random.rand() * 100000))
        self.inventory.insert(items.item("uranium", np.random.rand() * 10))

    def simulate(self, dt):
            
        self.thrust_acc = np.array([0.0, 0.0, 0.0])

        acceleration = self.heading.rotate(self.thrust_acc)

        self.velocity += acceleration * dt
        dpos = self.velocity * dt
        self.position += sc(dpos)

    def hit(self, source, power):
        ret = "Asteroid {} got hit with {} J of energy from {}".format(self.identifier, power, source.identifier)
        logger.debug(ret)

        return ret

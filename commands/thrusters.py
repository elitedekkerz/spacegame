import numpy as np
from pyquaternion import Quaternion
import logging
import player

class thrusters():

    def __init__(self, ship):
        self.log = logging.getLogger("thruster")
        self.ship = ship

        self.thruster_list = (
            thruster([0.0, 0.0, -100000.0], "front"),
            thruster([0.0, 0.0,  100000.0], "back"),
            thruster([0.0, -100000.0, 0.0], "top"),
            thruster([0.0,  100000.0, 0.0], "bottom"),
            thruster([-100000.0, 0.0, 0.0], "right"),
            thruster([ 100000.0, 0.0, 0.0], "left"),
        )


    def parse(self, args):
        commands = {
            "front":self.setCmd,
            "back":self.setCmd,
            "top":self.setCmd,
            "bottom":self.setCmd,
            "left":self.setCmd,
            "rigth":self.setCmd,
            "off":self.offCmd,
            "status":self.statusCmd,
        }
        try:
            return commands[args[1]](args)
        except:
            self.log.info("Unknown command given: {}".format(' '.join(args)))
            return self.help()

    def help(self):
        usage = (
            "thruster (front | back | top | bottom | left | right) <percantage>\n"
            "thruster off\n"
            "thruster status\n"
        )
        return player.response.usage, usage

    def simulate(self, dt, power_factor):
        thrust = np.array([0.0,0.0,0.0])
        for thruster in self.thruster_list:
            thrust += thruster.get_thrust_vector()

        self.ship.thrust_acc += thrust / self.ship.get_mass() * power_factor

    def setCmd(self, args):
        try:
            for thruster in self.thruster_list:
                if thruster.name == args[1]:
                    return thruster.set_value(args[2])
        except:
            return self.help()
    
    def offCmd(self, args):
        for thruster in self.thruster_list:
            thruster.set_value(0)
        return player.response.ok, "All thrusters are turned off"

    def statusCmd(self, args):
        msg = ""
        for thruster in self.thruster_list:
            thrust = np.linalg.norm(thruster.get_thrust_vector()) 
            msg += "Truster {} set to {:.0f} % producing {:.0f} N of thrust.\n".format(thruster.name, thruster.value * 100, thrust)

        return player.response.ok, msg

    def getPowerNeeded(self):
        usage = 0.0
        for thruster in self.thruster_list:
            usage += thruster.power_usage()

        return usage



class thruster():
    def __init__(self, vector, name):
        self.thrust_vector = np.array(vector)
        self.value = 0
        self.name = name
        self.max_power_usage = np.linalg.norm(self.thrust_vector)

        #Watts needed for 1 newton
        self.power_consumption = 50
        
    def set_value(self, string):
        val = np.clip(float(string), 0, 100)
        self.value = val / 100.0
        return player.response.ok, "{} thruster set to {:.0f} %.".format(self.name, val)

    def power_usage(self):
        return self.max_power_usage * self.value * self.power_consumption

    def get_thrust_vector(self):
        return self.thrust_vector * self.value

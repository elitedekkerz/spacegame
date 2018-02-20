import math
import numpy as np

#import server
import player
import gameObject
import logging

#return received arguments excluding the first one
class radar():
    def __init__(self, ship):
        self.ship = ship
        
        #Scan distance of the radar 
        self.range = 30000
        self.sector = 180
        #Power usage when on in watts
        self.power_consumption = 1000000
        self.powered = False
        self.power_factor = 1
        self.next_scan = 0

        #keep list of the objects that are in scan range
        self.objects_in_range = []

    def parse(self, args):
        commands = {
        "on":self.powerOn,
        "off":self.powerOff,
        "scan":self.scan,
        "sector":self.setSector,
        "identify":self.identify,
        }
        try:
            return commands[args[1]](args)
        except:
            logging.exception('Radar exception')
            return player.response.usage, ("radar scan/sector/on/off/identify\n"
                    "output format:\n"
                    "identifier: <range>(meters) <elevation>(degrees) <azimuth>(degrees)\n")

    def simulate(self, dt, power_factor):
        self.power_factor = power_factor
        
        #Update scan every 2 seconds
        self.next_scan -= dt
        if self.next_scan < 0 and self.powered:
            self.sim_scan()
            self.next_scan = 2

    def sim_scan(self):
        self.objects_in_range.clear()

        #Get scan range
        eff_range = self.range * (180 / self.sector) * self.power_factor

        #Find all object that are in the scan cone
        for obj in gameObject.objects:
            if self.isInRange(obj, eff_range):
                if obj != self.ship:
                    self.objects_in_range.append(obj) 

        #Sort found objects by distance
        self.objects_in_range.sort(key=lambda tup: tup.getDistanceTo(self.ship))


    def scan(self, args):
        if not self.powered:
            return player.response.error, "Radar is turned off"
        
        #Generate string from the scaned objects
        result = ""
        for i in self.objects_in_range:
            dist, azimuth, inclination = self.ship.getSphericalCoordinateTo(i, inDeg = True)
            result += "{}: {:06.3E} {:+06.1f} {:+06.1f}\n".format(i.identifier, dist, azimuth, inclination)

        return player.response.ok, result

    def setSector(self, args):
        try:
            self.sector = np.clip(float(args[2]), 1, 180)
            return player.response.ok, "sector set to: {0}".format(self.sector)
        except IndexError:
            return player.response.ok, "{0}".format(self.sector)
        except:
            logging.exception("exception when setting sector value")
            return player.response.ok, "Expected {float = 1.0 ... 180.0}"

    def powerOn(self, args):
        self.powered = True
        self.next_scan = 0
        return player.response.ok, " "
    
    def powerOff(self, args):
        self.powered = False
        return player.response.ok, " "

    def getPowerNeeded(self):
        if self.powered:
            return self.power_consumption
        else:
            return 0

    def isInRange(self, obj, eff_range):
        return obj.getDistanceTo(self.ship) < eff_range and self.ship.getAngleTo(obj, True) < self.sector

    def identify(self, args):
        if not self.powered:
            return player.response.error, "Radar is turned off"

        target = None
        eff_range = self.range * (180 / self.sector) * self.power_factor

        #find target from game objects
        for obj in gameObject.objects:
            if obj.identifier == args[2] and self.isInRange(obj, eff_range): 
                target = obj
                break
        
        if isinstance(target, gameObject.gameObject):
            dist, azimuth, inclination = self.ship.getSphericalCoordinateTo(target, inDeg = True)
            result = "{}: {:06.3E} {:+06.1f} {:+06.1f}\n".format(target.identifier, dist, azimuth, inclination)
            result += "mass: {:06.3E}\n".format(target.get_mass())
            result += "heading: "+ str(target.getHeading())
        else:
            return player.response.error, "unknown target"

        return player.response.ok, result

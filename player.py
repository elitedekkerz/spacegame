from types import *
import logging

class player():
    '''process data received from client'''
    def __init__(self, client):
        #functionality variables
        self.client = client
        self.log = logging.getLogger(self.client.addressString)
        #game variables
        self.name = 'Yuri'
        self.ship = None
        #self.prompt = '\n{}@{}>'.format(self.name,self.ship.name)
        self.log.info('ready')

    def disconnect(self):
        '''remove self from ship and kill client'''
        self.leaveShip()
        self.alive = False
        self.log.info('disconnected')

    def setName(self, name):
        '''change onscreen name'''
        self.name = name
        self.log.info('changed name to %s', self.name)

    def joinShip(self, ship):
        '''add self to ship'''
        self.leaveShip()
        self.ship = ship
        self.ship.crew.append(self)
        self.log.info('joined %s', self.ship.name)

    def leaveShip(self):
        '''remove self from current ship'''
        if self.ship:
            self.ship.crew.remove(self)
        self.ship = None

    def echo(self, message):
        '''return what was given'''
        return message

    def parse(self):
        '''process a command received from the client'''
        #echo as placeholder
        message = self.client.getMessage()
        if message:
            reply = self.echo(message)
            self.client.sendMessage(reply)

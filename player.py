from types import *
import logging

players = []
playerIDCounter = 0

class player():
    '''process data received from client'''
    def __init__(self, client):
        #functionality variables
        self.client = client
        #game variables
        self.name = 'Yuri'
        self.ship = None

        #add player to game
        global players, playerIDCounter
        self.id = playerIDCounter
        playerIDCounter += 1
        players.append(self)
        self.log = logging.getLogger('player-'+str(self.id))

        #send client some confirmation that they have connected
        self.updatePrompt()
        self.client.sendMessage(self.prompt.encode('utf-8'))
        self.log.info('ready')

    def disconnect(self):
        '''remove self from ship and kill client'''
        self.leaveShip()
        self.client.alive = False
        global players
        players.remove(self)
        self.log.info('disconnected')

    def updatePrompt(self):
        '''rebuild prompt string'''
        self.prompt = '\n'
        self.prompt += self.name
        if self.ship:
            self.prompt += self.ship.name
        self.prompt += '>'

    def setName(self, name):
        '''change onscreen name'''
        self.name = name
        self.updatePrompt()
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
        self.log.info('echoing: %s', message)
        return message

    def parse(self):
        '''process a command received from the client'''
        #echo as placeholder
        message = self.client.getMessage()
        if message:
            response = 'OK\n'
            reply = self.echo(message)
            self.client.sendMessage('{}{}{}'.format(response,reply ,self.prompt).encode('utf-8'))

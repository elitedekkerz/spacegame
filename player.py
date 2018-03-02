from types import *
import logging

import ship
import gameObject

players = []
playerIDCounter = 0

class response():
    ok = 'Ok\n'
    error = 'Error\n'
    usage = 'Usage\n'

class player():
    '''process data received from client'''
    def __init__(self, client):
        #functionality variables
        self.client = client

        #game variables
        self.name = 'Yuri'
        self.ship = None

        #player commands
        self.commands = {
            'disconnect': self.disconnect,
            'join': self.joinShip,
            'name': self.setName,
            'echo': self.echo,
            'help': self.printHelp,
            }

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

    def disconnect(self, message = ['', 'unknown']):
        '''remove self from ship and kill client'''
        self.leaveShip()
        self.client.alive = False
        global players
        players.remove(self)
        self.log.info('disconnected, (%s)', ' '.join(message[1:]))
        return response.ok, 'disconnecting'

    def updatePrompt(self):
        '''rebuild prompt string'''
        self.prompt = '\n'
        self.prompt += self.name
        if self.ship:
            self.prompt += '@'+self.ship.name
        self.prompt += '>'

    def setName(self, name):
        '''change onscreen name'''
        self.name = ' '.join(name[1:])
        self.updatePrompt()
        self.log.info('changed name to %s', self.name)
        return response.ok, 'your name is now {}'.format(self.name)

    def printHelp(self, arg):
        msg  = "disconnect           Disconnects form server\n"
        msg += "join <ship_name>     Joins to a ship (creates it if it doesn't exsist)\n"
        msg += "name <name>          Change player name\n"
        msg += "help                 This help"
        return response.ok, msg

    def joinShip(self, name):
        '''add self to ship'''
        name = ' '.join(name[1:])
        self.leaveShip()

        #try to find ship with given name
        for obj in gameObject.objects:
            try:
                if obj.name == name:
                    self.ship = obj
            except:
                continue

        #create new ship if not found
        if not self.ship:
            self.ship = ship.ship()
            self.ship.name = name

        #add self to crew
        self.ship.crew.append(self)
        self.updatePrompt()
        self.log.info('joined %s', self.ship.name)
        return response.ok, 'you have joined the crew of {}'.format(self.ship.name)

    def leaveShip(self):
        '''remove self from current ship'''
        if self.ship:
            self.ship.crew.remove(self)
        self.ship = None

    def echo(self, message):
        '''return what was given'''
        reply = ' '.join(message[1:])
        self.log.info('echoing: %s', reply)
        return response.ok, reply

    def parse(self):
        '''process a command received from the client'''
        #echo as placeholder
        message = self.client.getMessage()
        if message:
            message = message.decode('utf-8').strip('\n')
            #split by whitespace, or just put in an array
            if ' ' in message:
                message = message.split(' ')
            else:
                message = [message]

            #try to find a matching command
            if self.ship and message[0] == 'help':
                reply = self.ship.print_help(message)
                status = response.ok
            elif message[0] in self.commands:
                status, reply = self.commands[message[0]](message)
            elif self.ship and  message[0] in self.ship.modules:
                status, reply = self.ship.modules[message[0]].parse(message)
            else:
                status = response.error
                reply = 'unknown command'

            #reply to player
            self.client.sendMessage('{}{}{}'.format(status,reply ,self.prompt).encode('utf-8'))

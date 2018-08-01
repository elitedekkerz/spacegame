from types import *
import logging

import json
import ship
import gameObject

players = []
playerIDCounter = 0

class response():
    ok = 'Ok'
    error = 'Error'
    usage = 'Usage'

class player():
    '''process data received from client'''
    def __init__(self, client):
        #functionality variables
        self.client = client

        #game variables
        self.name = 'Yuri'
        self.ship = None
        self.outputJson = False

        #player commands
        self.commands = {
            'disconnect': self.disconnect,
            'join': self.joinShip,
            'name': self.setName,
            'echo': self.echo,
            'help': self.printHelp,
            'json': self.changeJson,
            }

        #add player to game
        global players, playerIDCounter
        self.id = playerIDCounter
        playerIDCounter += 1
        players.append(self)
        self.log = logging.getLogger('player-'+str(self.id))

        #send client some confirmation that they have connected
        self.updatePrompt()
        try:
            with open('./motd.txt', 'r') as f:
                motd = f.read()
        except FileNotFoundError:
            motd = ''
        self.client.sendMessage((motd+self.prompt).encode('utf-8'))
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
    
    def changeJson(self, value):
        '''Change output format'''
        if value[1] == 'on':
            self.outputJson = True
            return response.ok, 'using json output format'
        if value[1] == 'off':
            self.outputJson = False
            return response.ok, 'using standard output format'

        return response.error, "json on -> use json. json off -> use standard" 

    def printHelp(self, arg):
        msg  = (
            "disconnect           Disconnects form server\n"
            "join <ship_name>     Joins to a ship (creates it if it doesn't exsist)\n"
            "name <name>          Change player name\n"
            "json (on | off)      Enable or disable json output format"
            "help                 This help"
        )
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

            dir = None
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
            if self.outputJson:
                if self.ship:
                    ship = self.ship.name
                else:
                    ship = None
                json_data = {"status" : status, "name":self.name, "ship":ship, "text": reply, "data": dir}
                self.client.sendMessage(''.join((json.dumps(json_data), '\n')).encode('utf-8'))
            else:
                self.client.sendMessage('{}{}{}'.format(''.join((status, '\n')),reply ,self.prompt).encode('utf-8'))

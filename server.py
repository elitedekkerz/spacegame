#!/usr/bin/python3
"""
run an echo server for multiple clients
"""

import socket
import threading
import logging
import errno
import time
import numpy as np

#game modules
import ship
import player
from gameObject import gameObject

logging.basicConfig(level=logging.INFO)

try:
   with open('./motd.txt', 'r') as f:
      motd = f.read(1024)
except:
      motd = 'http://github.com/eliteDekkerz/spacegame'

class client():
   """
   handles data from and to client
   """
   def __init__(self, conn, address):
      self.conn = conn
      self.address = address
      self.changes = ''
      self.player = player.player()
      self.ship = None

   #move client to ship
   def joinShip(self, ship):
      try:
         self.leaveShip()
      except:
         pass
      self.ship = ship
      self.ship.crew.append(self.player)

   def leaveShip(self):
      self.ship.crew.remove(self.player)
      #remove old ship if left empty
      if len(self.ship.crew) < 1:
         self.ship.remove()
      self.ship = None
   
   def __str__(self):
      return self.address[0]+":"+str(self.address[1])
   
   def update(self, output=''):
      #send known changes to client
      output +='\n'+self.player.name+'@'+self.ship.name+'>'
      try:
         self.conn.send(output.encode('utf-8'))
      except socket.error as e:
         if e.args[0] == errno.EWOULDBLOCK:
            pass
      except:
         raise

class clientHandler():
   #a list for all the connected clients
   clientList = []
   ships = {}
   clientListLock = threading.Lock()
   run = False

   #provide basic help
   def help(self, client):
      commands =''
      for key in client.ship.modules:
         commands += key+"\n"
      return ("\n"
         "\\\\\\spacegame///\n"
         "version ?.?.?\n"
         "list of commands:\n\n"
         + commands +
         "\nfor more info, visit:\n"
         "https://github.com/elitedekkerz/spacegame\n"
      )

   #add a client to the list
   def addClient(self, cli):
      with self.clientListLock:
         logging.info('client %s connected',str(cli))
         cli.conn.setblocking(0)
         newShip = ship.ship()
         cli.joinShip(newShip)
         self.clientList.append(cli)
         cli.update(motd)
  
   #remove a client from the list 
   def removeClient(self, cli):
      with self.clientListLock:
         cli.leaveShip()
         cli.conn.close()
         self.clientList.remove(cli)
         logging.info('client %s removed', str(cli))

   #start thread for client handling
   def start(self):
      self.run = True
      #Create asteroids in 100 km radius 
      for i in range(100):
         pos = (np.random.rand(3) - 0.5) * 100000
         newAsteroid = gameObject("ast", pos)

      threading.Thread(target=clients.handleClients,args=()).start()

   #stop client handling thread
   def stop(self):
      self.run = False

   def config(self, cli, args):
      logging.debug('%s is configurig with args: %s', cli, str(args))
      try:
         #set player name
         if args[1] == 'name':
            cli.player.name = str.join(' ',args[2:])
            logging.info('%s is now known as %s', cli, cli.player.name)
            return 'your name is now '+cli.player.name

         #ship
         if args[1] == 'ship':
            shipName = str.join(' ', args[3:])

            #set ship name
            if args[2] == 'name':
               #make sure ship isn't named and name is available
               for name, ship in self.ships.items():
                  if name == shipName:
                     return 'sorry, that name is already taken'
                  if ship == cli.ship:
                     return 'your ship is already named '+name

               #name ship and add it to the list of ships
               self.ships.update({shipName:cli.ship})
               cli.ship.name = shipName
               logging.info('%s named their ship %s', cli.player.name, cli.ship.name)
               return 'you crudely engrave "' + shipName + '" on the side of your vessel'

            #join ship
            if args[2] == 'join':
               try:
                  cli.joinShip(self.ships[shipName])
                  logging.info('%s, joined %s', cli.player.name, cli.ship.name)
                  return 'you have joined the crew of '+shipName
               except:
                  return 'that ship doesn\'t exist'
            return 'unknown ship configuration command'
         return 'unknown configuration command'
      except:
         logging.exception('can\'t handle client config request')
         return 'invalid config command, read the documentation'

   #handle the clients in the list
   def handleClients(self):

      #Get start timr for the simulation
      prev_time = time.perf_counter()
      while self.run:
         for cli in self.clientList:
            #get input from client
            try: 
               data = cli.conn.recv(1024).decode('utf-8', 'ignore')

               #parse received data via an external class for some reason
               args = cli.player.readInput(data)
               if not args:
                  continue

               #ship commands
               if args[0] in cli.ship.modules:
                  try:
                     cli.update(cli.ship.parse(args))
                  except:
                     logging.exception('unable to parse %s', repr(args))

               #configurations
               elif args[0] == 'config':
                  try:
                     cli.update(self.config(cli, args))
                  except:
                     logging.exception('unable configure client with %s', repr(args))

               #disconnect commands
               elif args[0] in ['quit', 'bye', 'exit']:
                  logging.info('Client %s gracefully quit.', str(cli))
                  cli.update('bye!\n')
                  self.removeClient(cli)
                  break

               #help
               else:
                  logging.info('%s doesn\'t know what to do', cli)
                  cli.update(self.help(cli))
            except socket.error as e:
               if e.args[0] == errno.EWOULDBLOCK:
                  pass
            except AttributeError:
                    logging.info('Client %s has unexpectedly quit.', str(cli))
                    self.removeClient(cli)

         #See if we need to run the simulation
         dt = time.perf_counter() - prev_time
         if dt > 0.05:
            prev_time = time.perf_counter()
            #Run the simulation
            for cli in self.clientList:
               cli.ship.simulate(dt)
         else:
            time.sleep(0.05-dt)

#setup server socket for connecting
logging.info('opening socket')
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(('0.0.0.0',1961))
sock.listen(5)

#setup handler for clients
logging.info('setting up client handler')
clients = clientHandler()
clients.start()

#main loop
logging.info('accepting connections')
while True:
   try:
      conn, address = sock.accept()
      cli = client(conn, address)
      clients.addClient(cli)
   except KeyboardInterrupt:
      break
   except:
      logging.exception('')

#clean up
logging.info('shutting down')
clients.stop()
sock.close()
logging.info('bye!')

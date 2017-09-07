#!/usr/bin/python3
"""
run an echo server for multiple clients
"""

import socket
import threading
import logging
import errno
import time

#game modules
import ship
import player

logging.basicConfig(level=logging.DEBUG)

class client():
   """
   handles data from and to client
   """
   def __init__(self, conn, address):
      self.conn = conn
      self.address = address
      self.changes = ''
      self.player = player.player()
      self.ship = ship.ship([0.0, 0.0, 0.0])
   
   def __str__(self):
      return self.address[0]+":"+str(self.address[1])

   def getInput(self):
      #non-blockingly receive data from client
      try:
         data = self.conn.recv(1024)
         if data:
            return data.decode('utf-8', 'ignore')
         else:
            logging.info('no data received from %s', str(self))
            raise Exception
      except socket.error as e:
         if e.args[0] == errno.EWOULDBLOCK:
            pass
      except:
         logging.exception('unable to get client input')
         raise
   
   def update(self, output):
      #send known changes to client
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
         self.clientList.append(cli)
  
   #remove a client from the list 
   def removeClient(self, cli):
      with self.clientListLock:
         logging.info('client %s disconnected', str(cli))
         cli.conn.close()
         self.clientList.remove(cli)

   #start thread for client handling
   def start(self):
      self.run = True
      threading.Thread(target=clients.handleClients,args=()).start()

   #stop client handling thread
   def stop(self):
      self.run = False

   #handle the clients in the list
   def handleClients(self):

      #Get start timr for the simulation
      prev_time = time.perf_counter()
      while self.run:
         for cli in self.clientList:
            try:
               #get input from client
               clientInput = cli.getInput()
            except:
               logging.exception('exception while handling client')
               #remove client and restart loop
               self.removeClient(cli)
               break

            #do something
            if clientInput:
               logging.debug('received %s', repr(clientInput))
               #handle user input as a player
               output = cli.player.readInput(clientInput)
               try:
                  output.update({'output':cli.ship.modules[output['command'][0]].parse(output['command'])})
               except:
                  output.update({'output':self.help(cli)})
               cli.update(output['output'])

         #See if we need to run the simulation
         dt = time.perf_counter() - prev_time
         if dt > 0.05:
            prev_time = time.perf_counter()
            #Run the simulation
            for cli in self.clientList:
               cli.ship.simulate(dt)

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

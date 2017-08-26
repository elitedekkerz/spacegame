#!/usr/bin/python3
"""
run an echo server for multiple clients
"""

import socket
import threading
import logging
import errno
import ship
import time

logging.basicConfig(level=logging.DEBUG)

class client():
   """
   handles data from and to client
   """
   def __init__(self, conn, address):
      self.conn = conn
      self.address = address
      self.changes = ''
      self.player = ship.player()
   
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
   
   def update(self):
      #send known changes to client
      try:
         if self.changes:
            self.conn.send(self.changes.encode('utf-8'))
            self.changes = ''
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

               #do something
               if clientInput:
                  logging.debug('received %s', repr(clientInput))
                  #handle user input as a player
                  cli.player.readInput(clientInput)
                  cli.changes = cli.player.tryCommand()

               #reply to client
               cli.update()

            except:
               logging.exception('exception while handling client')
               #remove client and restart loop
               self.removeClient(cli)
               break

         #See if we need to run the simulation
         dt = time.perf_counter() - prev_time
         if dt > 0.05:
            prev_time = time.perf_counter()
            #Run the simulation
            for cli in self.clientList:
               cli.player.ship.simulate(dt)

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

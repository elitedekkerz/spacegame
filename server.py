import threading
import logging
import time

#game modules
import client
import ship
import player
import gameObject

class server():
    def __init__(self):
        self.log = logging.getLogger('server')
        self.clientHandler = client.clientHandler('0.0.0.0',1961)
        self.clientHandler.startAcceptingClients()
        #set client handler to create new player when client joins
        self.clientHandler.attachNewClientEvent(player.player)
        self.tickRate = 100 #how often do we update everything?
        self.run = True

        #setup threads
        self.threads = []
        self.threads.append(threading.Thread(target = self.tickLoop, args = (self.simulate,)))
        self.threads.append(threading.Thread(target = self.tickLoop, args = (self.processClients,)))

    def start(self):
        for th in self.threads:
            th.start()

    def stop(self):
        #stop game
        self.log.debug('stopping threads')
        self.run = False
        for th in self.threads:
            th.join()

        #get rid of clients
        self.clientHandler.stopAcceptingClients()
        self.clientHandler.removeAllClients()
        self.log.info('bye!')

    def processClients(self,dt):
        #process a single message from each client
        for pl in player.players:
            #make sure client is still connected
            if pl.client.alive:
                pl.parse()
            else:
                pl.disconnect()
                self.clientHandler.removeClient(pl.client)
    
    def simulate(self,dt):
        #process each game object once
        for obj in gameObject.objects:
            try:
                obj.simulate(dt)
            except AttributeError:
                continue
            except:
                self.log.exception('unable to simulate %s', obj)

    def tickLoop(self, method):
        #init timeke eping
        prev_time =  time.perf_counter()
        #try to call given metod at server tick rate
        while self.run:
            #get accurate representation of last time called
            now = time.perf_counter()
            dt = now - prev_time
            prev_time = now

            #call given method
            try:
                method(dt)
            except:
                self.log.exception('unable to call method: %s', method.__name__)

            #check if simulation is taking for too long
            simulationTime = (time.perf_counter() - now)
            try:
                #todo: get more accurate timing
                time.sleep(1/self.tickRate - simulationTime)
            except ValueError:
                self.log.warning('method %s call taking too long to match tick rate (%s > %s)', method.__name__, simulationTime, 1/self.tickRate)

if __name__ == '__main__':
    logging.basicConfig(level=logging.debug)
    s = server()
    s.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break
    s.stop()

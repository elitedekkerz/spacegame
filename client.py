import socket
import logging
import threading
import queue

class client():
    def __init__(self, connection):
        self.log = logging.getLogger('client')
        self.socket = connection
        self.socket.settimeout(1)
        self.receivedMessages = queue.Queue(64)
        self.sentMessages = queue.Queue(64)

    def start(self):
        self.log.debug('starting')
        self.alive = True
        self.threads =[]
        self.threads.append(threading.Thread(target=self.receiveMessages))
        self.threads.append(threading.Thread(target=self.sendMessages))
        for thread in self.threads:
            thread.start()
        self.log.info('client ready')

    def receiveMessages(self):
        while self.alive:
            try:
                data = self.socket.recv(1024)
                if not data:
                    raise Exception
                self.log.info('%s> %s',repr(self.socket.getpeername()), data)
                self.receivedMessages.put(data)
            except socket.timeout:
                pass
            except:
                logging.exception('unable to receive message from client')
                self.alive = False

    def sendMessages(self):
        while self.alive:
            try:
                data = self.sentMessages.get(timeout=1)
                #if not data:
                #    continue
                self.log.info('%s< %s',repr(self.socket.getpeername()), data)
                self.socket.send(data)
            except socket.timeout:
                pass
            except queue.Empty:
                pass
            except:
                logging.exception('unable to send message to client')
                self.alive = False

    def getMessage(self):
        try:
            return self.receivedMessages.get_nowait()
        except queue.Empty:
            return None

    def sendMessage(self, message):
        self.sentMessages.put(message)

    def stop(self):
        self.log.debug('stopping thread')
        self.alive = False
        for thread in self.threads:
            thread.join()
        self.socket.close()

class clientHandler():
    def __init__(self, address, port):
        self.log = logging.getLogger('clientHandler')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.bind((address, port))
        self.socket.listen(5)
        self.socket.settimeout(1)
        self.clients=[]

    def listClients(self):
        return self.clients

    def startAcceptingClients(self):
        self.run = True
        self.thread = threading.Thread(target=self.getClients)
        self.thread.start()

    def stopAcceptingClients(self):
        self.run = False
        self.thread.join()

    def removeAllClients(self):
        for client in self.clients:
            self.removeClient(client)

    def removeClient(self, client):
        self.log.info('removing client: %s', repr(client.socket.getpeername()))
        client.stop()
        self.clients.remove(client)

    def getClients(self):
        while self.run:
            try:
                connection, address = self.socket.accept()
                self.log.info('new client: %s', repr(address))
                cli = client(connection)
                cli.start()
                self.clients.append(cli)
            except socket.timeout:
                pass
            except:
                self.log.exception('unable to receive clients')
                self.run = False

if __name__ == "__main__":
    import time
    logging.basicConfig(level=logging.DEBUG)
    a = clientHandler('0.0.0.0',1961)
    a.startAcceptingClients()
    try:
        while True:
            for cli in a.listClients():
                if cli.alive:
                    echo = cli.getMessage()
                    if echo:
                        cli.sendMessage(echo)
                else:
                    a.removeClient(cli)
    except:
        logging.exception('unable to echo to clients')
    a.stopAcceptingClients()
    a.removeAllClients()

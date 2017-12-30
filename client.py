import socket
import logging
import threading
import queue

class client():
    '''run separate threads for sending and receiving data via given socket'''
    def __init__(self, connection):
        '''new client'''
        self.adressString = connection.getpeername()[0]+":"+str(connection.getpeername()[1])
        self.log = logging.getLogger(self.adressString)
        self.socket = connection
        self.socket.settimeout(1)
        self.receivedMessages = queue.Queue(64)
        self.sentMessages = queue.Queue(64)
        self.alive = True

    def start(self):
        '''start separate threads for sending/receiving via socket'''
        self.log.debug('starting')
        self.alive = True
        self.threads =[]
        self.threads.append(threading.Thread(target=self.receiveMessages))
        self.threads.append(threading.Thread(target=self.sendMessages))
        for thread in self.threads:
            thread.start()
        self.log.debug('ready')

    def receiveMessages(self):
        '''receive data via socket and add it to a queue'''
        while self.alive:
            try:
                data = self.socket.recv(1024)
                if not data:
                    raise Exception
                self.log.info('%s> %s',repr(self.socket.getpeername()), data)
                self.receivedMessages.put(data)
            except socket.timeout:
                pass
            except OSError:
                #socket has been closed
                self.run = False
            except:
                logging.exception('unable to receive message from client')
                self.alive = False

    def sendMessages(self):
        '''send messages from queue to socket'''
        while self.alive:
            try:
                data = self.sentMessages.get(timeout=1)
                self.log.info('%s< %s',repr(self.socket.getpeername()), data)
                self.socket.send(data)
            except socket.timeout:
                pass
            except queue.Empty:
                pass
            except:
                logging.exception('unable to send message to client')
                self.alive = False
        self.log.debug('send thread finished')

    def getMessage(self):
        '''give one received message from queue'''
        if not self.alive:
            return None
        try:
            return self.receivedMessages.get_nowait()
        except queue.Empty:
            return ''

    def sendMessage(self, message):
        '''add message to send queue'''
        self.sentMessages.put(message)

    def stop(self):
        '''stop threads for sending/receiving messages via socket'''
        self.log.debug('stopping thread')
        self.alive = False
        for thread in self.threads:
            thread.join()
        self.log.debug('closing socket')
        self.socket.close()
        self.log.info('disconnected')

class clientHandler():
    def __init__(self, address, port):
        '''new handler for accepting clients via given address and port'''
        self.log = logging.getLogger('clientHandler')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.socket.bind((address, port))
        self.socket.listen(5)
        self.socket.settimeout(1)
        self.clients=[]
        self.log.info('ready')

    def listClients(self):
        '''return array of current clients'''
        return self.clients

    def stop(self):
        '''stop properly'''
        self.log.info('stopping')
        self.stopAcceptingClients()
        self.kickAllClients()

    def startAcceptingClients(self):
        '''start thread which accepts clients'''
        self.run = True
        self.thread = threading.Thread(target=self.getClients)
        self.thread.start()
        self.log.debug('thread started')

    def stopAcceptingClients(self):
        '''stop thread which accepts clients'''
        self.log.debug('stopping thread')
        self.run = False
        self.thread.join()
        self.log.debug('thread stopped')
        self.log.debug('closing socket')
        self.socket.close()
        self.log.debug('socket closed')
        self.log.info('no longer accepting clients')

    def removeAllClients(self):
        '''drop all clients'''
        #kill all clients simultaniously in order to save time
        for client in self.clients:
            client.alive = False

        #remove them properly
        count = 0
        for client in self.clients:
            self.removeClient(cli)
            count += 1
        self.log.debug('%s clients kicked', str(count))

    def removeClient(self, cli):
        self.log.info('removing client: %s', repr(cli.socket.getpeername()))
        cli.stop()
        self.clients.remove(cli)

    def getClients(self):
        '''continuously accept new clients and add them to a array'''
        self.log.info('accepting clients')
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

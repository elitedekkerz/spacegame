import logging
import player
logger = logging.getLogger('log')

class log():
    data = ''

    def __init__(self, size=1024):
        self.size = size

    def parse(self, args):
        commands = {
            'write':self.write,
            'read':self.read,
            'clear':self.clear,
        }
        try:
            return commands[args[1]](args)
        except:
            logger.debug('incorrect command %s', str.join(' ', args))
            return self.help()

    def write(self,args):
        inData = str.join(' ', args[2:])+'\n'
        lengthSum = len(self.data + inData)
        if lengthSum > self.size:
            self.data = (self.data+inData)[-self.size:]
        else:
            self.data += inData
        logger.info('log updated: %s', inData[:-1])
        return player.response.ok, ''

    def read(self,args):
        return player.response.ok, self.data

    def clear(self,args):
        self.data = ''
        logger.info('log cleared')
        return player.response.ok, 'log cleared'

    def help(self):
        return player.response.usage, "log <write <message>/read/clear>"

    def simulate(self, dt, power_factor):
        pass

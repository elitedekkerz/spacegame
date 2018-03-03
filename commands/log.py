import logging
import player

class log():
    data = ''

    def __init__(self, size=1024):
        self.log = logging.getLogger("log")
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
            self.log.info("Unknown command given: {}".format(' '.join(args)))
            return self.help()

    def write(self,args):
        inData = str.join(' ', args[2:])+'\n'
        lengthSum = len(self.data + inData)
        if lengthSum > self.size:
            self.data = (self.data+inData)[-self.size:]
        else:
            self.data += inData
        self.log.info('log updated: %s', inData[:-1])
        return player.response.ok, ''

    def read(self,args):
        return player.response.ok, self.data

    def clear(self,args):
        self.data = ''
        self.log.info('log cleared')
        return player.response.ok, 'log cleared'

    def help(self):
        usage = (
            "log write\n"
            "log read\n"
            "log write <message>\n"
        )
        return player.response.usage, usage

    def simulate(self, dt, power_factor):
        pass

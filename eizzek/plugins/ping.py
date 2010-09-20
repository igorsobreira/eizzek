from twisted.internet import defer, protocol, reactor

from eizzek.lib.decorators import plugin


@plugin(r'^ping (?P<url>.+)$')
def ping(connection, url):
    '''
    Ping plugin. Usage:

        ping <url>
    '''
    deferred = defer.Deferred()
    reactor.spawnProcess(PingProtocol(deferred), '/sbin/ping', ['/sbin/ping', '-c', '3', url])
    return deferred


class PingProtocol(protocol.ProcessProtocol):
    
    def __init__(self, deferred):
        self.deferred = deferred
        self.data = ''
    
    def outReceived(self, data):
        self.data += data
     
    def processExited(self, reason):
        self.finish()
    
    def processEnded(self, reason):
        self.finish()
    
    def finish(self):
        try:
            self.deferred.callback(self.data)
        except defer.AlreadyCalledError:
            pass

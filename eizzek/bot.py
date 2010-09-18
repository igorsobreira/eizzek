from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence

from eizzek.lib.registry import registry
from eizzek.lib.resolver import PluginResolver

class EizzekProtocol(MessageProtocol):
    
    CANT_UNDERSTANT = u"Sorry, I can't understand..."
    
    @property
    def _my_jid(self):
        return self.parent.jid.full()
    
    def connectionMade(self):
        print 'Connected'
        self.send(AvailablePresence())
    
    def connectionLost(self, reason):
        print 'Disconnected'
    
    def onMessage(self, msg):
        if msg["type"] == 'chat' and hasattr(msg, "body") and msg.body:
            self.answer(msg)
    
    def answer(self, message):
        resolver = PluginResolver()
        try:
            defer = resolver.resolve(unicode(message.body))
            defer.addCallback(self.send_response, to=message['from'])
        except LookupError:
            self.send_response(self.CANT_UNDERSTANT, to=message['from'])
      
    def send_response(self, body, to):
        reply = self.build_response(to, body)
        self.send(reply)
    
    def build_response(self, to, body):
        reply = domish.Element((None, "message"))
        reply["to"] = to
        reply["from"] = self._my_jid
        reply["type"] = 'chat'
        reply.addElement("body", content=body)
        return reply


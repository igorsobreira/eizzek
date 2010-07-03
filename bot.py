from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence

class EizzekProtocol(MessageProtocol):
    
    def connectionMade(self):
        print 'Connected'
        self.send(AvailablePresence())
    
    def connectionLost(self, reason):
        print 'Disconnected'
    
    def onMessage(self, msg):
        
        if msg["type"] == 'chat' and hasattr(msg, "body"):
            reply = domish.Element((None, "message"))
            
            reply["to"] = msg["from"]
            reply["from"] = self.parent.jid.full()
            reply["type"] = 'chat'
            reply.addElement("body", content="hey there")
            
            self.send(reply)
    
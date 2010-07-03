from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence

from eizzek.lib.registry import registry

class EizzekProtocol(MessageProtocol):
    
    def connectionMade(self):
        print 'Connected'
        self.send(AvailablePresence())
    
    def connectionLost(self, reason):
        print 'Disconnected'
    
    def onMessage(self, msg):
        
        if msg["type"] == 'chat' and hasattr(msg, "body"):
            
            # TODO: use deferreds
            response = self.answer(str(msg.body))
            
            reply = domish.Element((None, "message"))
            
            reply["to"] = msg["from"]
            reply["from"] = self.parent.jid.full()
            reply["type"] = 'chat'
            reply.addElement("body", content=response)
            
            self.send(reply)
    
    def answer(self, message):
        for name, (regex, func) in registry.plugins.items():
            match = regex.match(message)
            if not match:
                continue
            
            # FIXME: for now, it's not possible to mix args and kwargs
            kwargs = match.groupdict()
            if kwargs:
                return func(**kwargs)
            args = match.groups()
            if args:
                return func(*args)
            return func()
        
        return u"I can't understand..."
    


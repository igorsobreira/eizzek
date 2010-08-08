from twisted.words.xish import domish
from wokkel.xmppim import MessageProtocol, AvailablePresence

from eizzek.lib.registry import registry

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
        defer = self.match( str(message.body) )
        if defer:
            defer.addCallback(self.send_response, to=message['from'])
        else:
            self.send_response(self.CANT_UNDERSTANT, to=message['from'])
    
    # FIXME: this logic should go to PluginRegistry
    def match(self, body):
        for name, (regex, func) in registry.plugins.items():
            match = regex.match(body)
            if not match:
                continue
            
            # TODO: for now, it's not possible to mix args and kwargs
            kwargs = match.groupdict()
            if kwargs:
                return func(**kwargs)
            
            args = match.groups()
            if args:
                return func(*args)
            
            return func()
    
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


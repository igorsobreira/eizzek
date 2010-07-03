#!/usr/bin/env python
import sleekxmpp
import config

class Eizzek(object):
    
    def __init__(self, jid, password):
        self.xmpp = sleekxmpp.ClientXMPP(jid, password)    
        self._connect_handlers()
    
    def _connect_handlers(self):
        self.xmpp.add_event_handler("session_start", self.handle_session_start) 
        self.xmpp.add_event_handler("message", self.handle_message)
    
    def run(self, address=()):
        self.xmpp.connect(address)
        self.xmpp.process(threaded=False)
    
    def handle_session_start(self, event): 
        self.xmpp.sendPresence(pstatus = "Hi, I'm a bot")
    
    def handle_message(self, message): 
        self.xmpp.sendMessage(message['from'].jid, message["body"])
    


def main():
    bot = Eizzek(config.JID, config.PASSWORD)
    bot.run((config.SERVER, config.PORT))


if __name__ == '__main__':
    main()
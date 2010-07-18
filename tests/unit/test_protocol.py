
from unittest import TestCase

from eizzek.bot import EizzekProtocol
from eizzek.lib.registry import registry
from eizzek.lib.decorators import plugin

class MessageMock(object):
    body = None
    
    def __getitem__(self, key):
        return 'eizzek@gmail.com/fun'
    


class EizzekProtocolTest(TestCase):
    
    def setUp(self):
        registry.clear()
        
        @plugin(r'^ping (?P<url>.+)$')
        def ping(url):
            return u'PING %s' % url
        
        self._my_jid = EizzekProtocol._my_jid
        EizzekProtocol._my_jid = 'eizzek@gmail.com/fun'
        def send(msg):
            self.response = msg
        
        self.protocol = EizzekProtocol()
        self.protocol.send = send
    
    def tearDown(self):
        EizzekProtocol._my_jid = self._my_jid
    
    def test_answer(self):
        message = MessageMock()
        
        message.body = u'ping http://igorsobreira.com'
        self.protocol.answer(message)
        
        assert 'PING http://igorsobreira.com' == str(self.response.body)
        
        message.body = u'no plugin'
        self.protocol.answer(message)
        
        assert "I can't understand..." == str(self.response.body)
    


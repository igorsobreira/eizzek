
from unittest import TestCase

from eizzek.bot import EizzekProtocol
from eizzek.lib.registry import registry
from eizzek.lib.decorators import plugin

class EizzekProtocolTest(TestCase):
    
    def setUp(self):
        registry.clear()
        
        @plugin(r'^ping (?P<url>.+)$')
        def ping(url):
            return u'PING %s' % url
        
        self.protocol = EizzekProtocol()
    
    
    def test_answer(self):
        response = self.protocol.answer(u'ping http://igorsobreira.com')
        
        assert response == u'PING http://igorsobreira.com'
        
        response = self.protocol.answer(u'no plugin')
        
        assert response == u"I can't understand..."
    


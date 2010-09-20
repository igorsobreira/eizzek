import time

from twisted.trial import unittest
from eizzek.plugins.ping import ping

class PingTest(unittest.TestCase):
    
    def test_ping(self):
        def assert_ping(response):
            assert 'PING igorsobreira.com (67.18.187.198): 56 data bytes' in response
        
        deferred = ping({}, 'igorsobreira.com')
        deferred.addCallback(assert_ping)
        return deferred
    

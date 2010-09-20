from twisted.trial import unittest

from eizzek.plugins.begin_end import begin
from eizzek.lib.registry import session_registry
from eizzek import session_plugin

class BeginTest(unittest.TestCase):

    def setUp(self):
        
        @session_plugin
        class Reverse(object):
            name = 'reverse'
            regex = r'^reverse (?P<string>.+)$'

            def begin(self):
                return u"Welcome to reverse!"

            def handle(self, message):
                return 

    def test_begin_plugin_not_found(self):
        session_registry.clear()
        
        def assert_begin(response):
            assert u"Plugin not found" == response

        deferred = begin({}, 'foo')
        deferred.addCallback(assert_begin)
        return deferred
    
    def test_begin_plugin_call_begin_method(self):
        def assert_begin(response):
            assert u"Welcome to reverse!" == response

        deferred = begin({}, 'reverse')
        deferred.addCallback(assert_begin)
        return deferred


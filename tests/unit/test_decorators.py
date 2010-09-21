from unittest import TestCase
import re

from eizzek.lib.decorators import plugin, session_plugin
from eizzek.lib.registry import registry, session_registry

class PluginTest(TestCase):
    
    def setUp(self):
        registry.clear()
    
    
    def test_plugin(self):
        
        assert len(registry.plugins) == 0
        
        @plugin(r'^ping (.+)$')
        def ping(**kwargs):
            return ''
        
        assert len(registry.plugins) == 1
        assert registry.plugins.has_key('ping')
    
    
    def test_named_plugin(self):
        
        assert len(registry.plugins) == 0
        
        @plugin(r'^ping (.+)$', name='ping_plugin')
        def ping(**kwargs):
            return ''
        
        assert len(registry.plugins) == 1
        assert registry.plugins.has_key('ping_plugin')
    
    
class SessionPluginTest(TestCase):

    def setUp(self):
        session_registry.clear()

    def test_create_session_plugin(self):

        assert 0 == len(session_registry.plugins)

        @session_plugin
        class Translate(object):
            name = 'translate'
            regex = r'^translate (?P<something>\w+)$'

        assert 1 == len(session_registry.plugins)
        assert session_registry.plugins.has_key('translate')

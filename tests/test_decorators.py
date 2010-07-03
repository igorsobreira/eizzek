from unittest import TestCase

from eizzek.lib.decorators import plugin
from eizzek.lib.registry import registry

class PluginTest(TestCase):
    
    def setUp(self):
        registry.clear()
    
    
    def test_plugin(self):
        
        assert len(registry.plugins) == 0
        
        @plugin(r'^ping (.+)$')
        def ping():
            return ''
        
        assert len(registry.plugins) == 1
        assert registry.plugins.has_key('ping')
    
    
    def test_named_plugin(self):
        
        assert len(registry.plugins) == 0
        
        @plugin(r'^ping (.+)$', name='ping_plugin')
        def ping():
            return ''
        
        assert len(registry.plugins) == 1
        assert registry.plugins.has_key('ping_plugin')
    
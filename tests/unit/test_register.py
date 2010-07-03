from unittest import TestCase

from eizzek.lib.registry import PluginRegistry

class PluginRegistryTest(TestCase):
    
    def setUp(self):
        PluginRegistry.clear()
        self.registry = PluginRegistry()
        
        def ping(): 
            return ''
        self.ping = ping
        self.regex = r'^ping (.+)$'
    
    
    def test_register_plugin(self):
        
        assert len(self.registry.plugins) == 0
        
        self.registry.register(self.ping.__name__, self.regex, self.ping)
        
        assert len(self.registry.plugins) == 1
        assert self.registry.plugins['ping'] == (self.regex, self.ping)
        
        def other_ping():
            return ''
        
        # ignore duplicates        
        self.registry.register('ping', self.regex, other_ping)
        
        assert len(self.registry.plugins) == 1
        assert self.registry.plugins['ping'] == (self.regex, self.ping)
    
    
    def test_unregister_plugin(self):
        
        assert len(self.registry.plugins) == 0
        
        self.registry.register(self.ping.__name__, self.regex, self.ping)
        
        assert len(self.registry.plugins) == 1
        
        self.registry.unregister('ping')     # by name
        
        assert len(self.registry.plugins) == 0
        
        self.registry.register(self.ping.__name__, self.regex, self.ping)
        
        assert len(self.registry.plugins) == 1
        
        self.registry.unregister(self.ping)     # by callable, with __name__ attribute
        
        assert len(self.registry.plugins) == 0
    
    
    def test_clear(self):
        self.registry.register(self.ping.__name__, self.regex, self.ping)
        
        assert len(self.registry.plugins) == 1
        
        self.registry.clear()
        
        assert len(self.registry.plugins) == 0
    
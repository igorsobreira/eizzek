from unittest import TestCase

from eizzek.lib.registry import PluginRegistry, SessionPluginRegistry

class PluginRegistryTest(TestCase):
    
    def setUp(self):
        self.registry = PluginRegistry()
        
        def ping(**kwargs):
            return ''
        self.ping = ping
        self.regex = r'^ping (.+)$'
    

    def test_register_plugin(self):
        
        assert len(self.registry.plugins) == 0
        
        self.registry.register(self.ping.__name__, self.regex, self.ping)
        
        assert len(self.registry.plugins) == 1
        assert self.registry.plugins['ping'] == (self.regex, self.ping)
        
        def other_ping(**kw):
            return ''
        
        # ignore duplicates        
        self.registry.register('ping', self.regex, other_ping)
        
        assert len(self.registry.plugins) == 1
        assert self.registry.plugins['ping'] == (self.regex, self.ping)
    
    def test_unregister_plugin_by_name(self):
        
        assert len(self.registry.plugins) == 0
        
        self.registry.register(self.ping.__name__, self.regex, self.ping)
        
        assert len(self.registry.plugins) == 1
        
        self.registry.unregister('ping')     # by name
        
        assert len(self.registry.plugins) == 0
    
    def test_unregister_plugin_by_callable(self):

        self.registry.register(self.ping.__name__, self.regex, self.ping)
        
        assert len(self.registry.plugins) == 1
        
        self.registry.unregister(self.ping)     # by callable, using __name__ attribute
        
        assert len(self.registry.plugins) == 0
    
    
    def test_clear(self):
        self.registry.register(self.ping.__name__, self.regex, self.ping)
        
        assert len(self.registry.plugins) == 1
        
        self.registry.clear()
        
        assert len(self.registry.plugins) == 0


class SessionPluginRegistryTest(TestCase):

    def setUp(self):
        self.session_registry = SessionPluginRegistry()
         
        class TranslateSessionPlugin(object):
            name = 'translate'
            regex = r'^translate (?P<from>\w+) (?P<to>\w+)$'
        
        self.translate = TranslateSessionPlugin


    def test_register_plugin(self):
        
        assert 0 == len(self.session_registry.plugins)
        
        self.session_registry.register(self.translate)

        assert 1 == len(self.session_registry.plugins)
        assert (self.translate.regex, self.translate) == self.session_registry.plugins[self.translate.name]
        
        class OtherTranslatePlugin(object):
            name = 'translate'
            regex = r'*'

        # ignore duplicates
        self.session_registry.register(OtherTranslatePlugin)
        
        assert 1 == len(self.session_registry.plugins)

        assert (self.translate.regex, self.translate) == self.session_registry.plugins[self.translate.name]


    def test_unregister_plugin_by_name(self):
        
        assert 0 == len(self.session_registry.plugins)
        
        self.session_registry.register(self.translate)
        
        assert 1 == len(self.session_registry.plugins)
        
        self.session_registry.unregister(self.translate.name)
        
        assert 0 == len(self.session_registry.plugins)


    def test_unregister_plugin_by_callable(self):
        
        self.session_registry.register(self.translate)
        
        assert 1 == len(self.session_registry.plugins)
        
        self.session_registry.unregister(self.translate)     # by callable, using ``name`` attribute
        
        assert 0 == len(self.session_registry.plugins)


    def test_clear(self):
        self.session_registry.register(self.translate)
        
        assert 1 == len(self.session_registry.plugins)
        
        self.session_registry.clear()
        
        assert 0 == len(self.session_registry.plugins)

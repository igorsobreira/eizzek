from twisted.trial import unittest

from eizzek.lib.registry import registry
from eizzek.lib.decorators import plugin
from eizzek.lib.resolver import PluginResolver
from eizzek.plugins.help import help

class HelpRegexTest(unittest.TestCase):

    def setUp(self):
        self.resolver = PluginResolver()
    
    def test_help_no_arguments(self):
        assert self.resolver.resolve('help')
    
    def test_help_with_argument(self):
        assert self.resolver.resolve('help plugin_name')


class HelpTest(unittest.TestCase):

    def setUp(self):
        
        @plugin(r'^simple (\d+)$')
        def simple_plugin(**kwargs):
            '''nothing special'''
        
        @plugin(r'^no_help_here$')
        def no_help_plugin(**kwargs):
            pass

    def tearDown(self):
        registry.unregister('simple_plugin')
        registry.unregister('no_help_plugin')

    def test_error_message_for_plugin_not_found(self):
        def assert_error(response):
            assert u"Plugin not found" == response

        deferred = help(plugin='foo')
        deferred.addCallback(assert_error)
        return deferred
    
    def test_show_plugin_help(self):
        def assert_help(response):
            assert u"nothing special" == response

        deferred = help(plugin='simple_plugin')
        deferred.addCallback(assert_help)
        return deferred
   
    def test_show_self_help_if_no_plugin_is_passed(self):
        def assert_self_help(response):
            assert "Eizzek help" in response

        deferred = help()
        deferred.addCallback(assert_self_help)
        return deferred
    
    def test_show_error_message_when_plugin_has_no_help(self):
        def assert_no_help(response):
            assert u"No help found" == response

        deferred = help('no_help_plugin')
        deferred.addCallback(assert_no_help)
        return deferred
    
    def test_list_available_plugins(self):
        def assert_list(response):
            assert u"no_help_plugin" in response
            assert u"simple_plugin" in response

        deferred = help('-l')
        deferred.addCallback(assert_list)
        return deferred

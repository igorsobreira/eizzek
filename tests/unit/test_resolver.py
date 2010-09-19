import unittest

from eizzek import PluginResolver, plugin, registry

class PluginResolverTest(unittest.TestCase):

    def setUp(self):
        registry.clear()
        
        @plugin(r"age (\d+)")
        def age(num, **kwargs):
            return "you're %d" % int(num)
        
        @plugin(r"aged ?(\d+)?")
        def age_default(num=0, **kwargs):
            return "you're %s" % num
        
        @plugin(r"hello ?(?P<name>\w+)?")
        def hello(name='stranger', **kwargs):
            return "hello %s" % name

        self.resolver = PluginResolver()
 
    def test_dont_find_plugin(self):
        try:
            self.resolver.resolve("no plugin")
            assert 0, u"Shouldn't find any plugin"
        except LookupError:
            pass
    
    def test_call_plugin_with_args(self):
        result = self.resolver.resolve('age 22')
        
        assert u"you're 22" == result

    def test_call_plugin_with_kwargs(self):
        result = self.resolver.resolve('hello igor')
        
        assert u"hello igor" == result
    
    def test_call_plugin_with_kwargs_and_default_argument(self):
        result = self.resolver.resolve('hello')
        
        assert u"hello stranger" == result

    def test_call_plugin_with_args_and_default_argument(self):
        result = self.resolver.resolve('aged')

        assert "you're 0"
    
    def test_find_callable_function(self):
        func, _ = self.resolver.find('age 22')
        
        print func.__name__
        assert 'age' == func.__name__


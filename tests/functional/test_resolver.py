import unittest
import redis

from eizzek import config, PluginResolver, plugin, session_plugin, registry, session_registry
from eizzek.lib.persistence import SessionPersistence

class PluginResolverTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self._redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
        self.session = SessionPersistence()

    def setUp(self):
        registry.clear()
        session_registry.clear()
        self._create_simple_plugins()
        self._create_session_plugins()
        self.resolver = PluginResolver()

        self.jid = 'igor@igorsobreira.com/Adium1234'
        self.conn_data = {'message': {'from': self.jid}}
        self._redis.hdel(self.jid, 'plugin')
    
    def _create_simple_plugins(self):
        @plugin(r"age (\d+)")
        def age(conn, num):
            return "you're %d" % int(num)
        
        @plugin(r"aged ?(\d+)?")
        def age_default(conn, num=0):
            return "you're %s" % num
        
        @plugin(r"hello ?(?P<name>\w+)?")
        def hello(conn, name='stranger'):
            return "hello %s" % name
    
    def _create_session_plugins(self):
        @session_plugin
        class Translate(object):
            name = 'translate'
            regex = '^translate (?P<from_lang>[\w-]+) (?P<to_lang>[\w-]+)$'

            def begin(self, conn, from_lang, to_lang):
                return u"translating from %s to %s" % (from_lang, to_lang)
            
            def handle(self, conn, msg):
                return u"qual o seu nome?"
    
        @session_plugin
        class Twitter(object):
            name = 'twitter'
            regex = '^twitter (\w+)$'

            def begin(self, conn, account):
                return u"twitter account @%s" % account
            
            def handle(self, conn, msg):
                return u"message: '%s'" % msg
        
        @session_plugin
        class DummyPlugin(object):
            name = 'dummy'
            regex = r'^dummy$'

            def begin(self, conn):
                return u"I'm dummy"
            
            def handle(self, conn, msg):
                return "message: '%s'" % msg

    # tests for simple plugins

    def test_dont_find_plugin(self):
        try:
            self.resolver.resolve("no plugin", self.conn_data)
            assert 0, u"Shouldn't find any plugin"
        except LookupError:
            pass
    
    def test_call_plugin_with_args(self):
        result = self.resolver.resolve('age 22', self.conn_data)
        
        assert u"you're 22" == result

    def test_call_plugin_with_kwargs(self):
        result = self.resolver.resolve('hello igor', self.conn_data)
        
        assert u"hello igor" == result
    
    def test_call_plugin_with_kwargs_and_default_argument(self):
        result = self.resolver.resolve('hello', self.conn_data)
        
        assert u"hello stranger" == result

    def test_call_plugin_with_args_and_default_argument(self):
        result = self.resolver.resolve('aged', self.conn_data)

        assert "you're 0"
   
    # tests for session plugins

    def test_session_plugin_with_kwargs(self):
        result = self.resolver.resolve('twitter igorsobreira', self.conn_data)

        assert u"twitter account @igorsobreira" == result

    def test_session_plugin_with_kwargs(self):
        result = self.resolver.resolve('translate en pt-br', self.conn_data)

        assert u"translating from en to pt-br" == result
   
    def test_session_plugin_with_no_arguments(self):
        result = self.resolver.resolve('dummy', self.conn_data)

        assert u"I'm dummy" == result
    
    def test_session_plugin_starts_session(self):
        result = self.resolver.resolve('translate en pt-br', self.conn_data)

        assert u"translating from en to pt-br" == result
        assert u"translate" == self._redis.hget(self.jid, 'plugin')
    
    def test_trying_to_start_two_sessions_closes_the_first_one(self):
        result = self.resolver.resolve('translate en pt-br', self.conn_data)
        
        assert u"translating from en to pt-br" == result
        assert u"translate" == self._redis.hget(self.jid, 'plugin')
        
        result = self.resolver.resolve('twitter igorsobreira', self.conn_data)
        
        assert u"twitter account @igorsobreira" == result
        assert u"twitter" == self._redis.hget(self.jid, 'plugin')
    
    def test_handle_session_plugin_should_call_handle_method_of_the_plugin(self):
        self.resolver.resolve('translate en pt-br', self.conn_data)
        result = self.resolver.handle_session_plugin("what's your name?", self.conn_data)

        assert u"qual o seu nome?" == result


import re
from abc import ABCMeta, abstractmethod

class BaseRegistry(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self._plugins = {}
    
    @property
    def plugins(self):
        return self._plugins
    
    def clear(self):
        self._plugins = {}
    
    @abstractmethod
    def register(self):
        pass
    
    @abstractmethod
    def unregister(self):
        pass


class PluginRegistry(BaseRegistry):
    '''
    Register simple plugins.
    '''    
    
    def register(self, name, regex, callable_obj):
        if name in self.plugins:
            return
        self._plugins[name] = (re.compile(regex), callable_obj)

    def unregister(self, name_or_callable):
        name = getattr(name_or_callable, '__name__', name_or_callable)
        self._plugins.pop(name, None)
    

class SessionPluginRegistry(BaseRegistry):
    '''
    Register session plugins
    '''

    def register(self, klass):
        if klass.name in self.plugins:
            return
        self._plugins[klass.name] = (re.compile(klass.regex), klass)

    def unregister(self, name_or_klass):
        name = getattr(name_or_klass, 'name', name_or_klass)
        self._plugins.pop(name, None)


registry = PluginRegistry()
session_registry = SessionPluginRegistry()

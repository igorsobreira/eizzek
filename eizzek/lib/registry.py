
class PluginRegistry(object):
    '''
    Register Eizzek plugins.
    '''
    
    _plugins = {}
    
    def register(self, name, regex, callable_obj):
        if name in self.plugins:
            return
        self._plugins[name] = (regex, callable_obj)
    
    def unregister(self, name_or_callable):
        if hasattr(name_or_callable, '__name__'):
            name_or_callable = name_or_callable.__name__
        self._plugins.pop(name_or_callable, None)
    
    @property
    def plugins(self):
        return self._plugins
    
    
    @classmethod
    def clear(cls):
        cls._plugins = {}
    



registry = PluginRegistry()
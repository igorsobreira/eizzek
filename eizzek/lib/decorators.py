import re
from eizzek.lib.registry import registry, session_registry

class plugin(object):
    '''
    Decorator used do create a plugin.
    '''
    
    def __init__(self, regex, name=None):
        self.regex = re.compile(regex)
        self.name = name
    
    def __call__(self, func):
        name = self.name or func.__name__
        registry.register(name, self.regex, func)
        return func
    

def session_plugin(klass):
    '''
    Decorator used to create a session plugin
    '''
    session_registry.register(klass)
    return klass

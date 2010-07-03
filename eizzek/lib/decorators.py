
from eizzek.lib.registry import registry

class plugin(object):
    '''
    Decorator used do create a plugin.
    '''
    
    def __init__(self, regex, name=None):
        self.regex = regex
        self.name = name
    
    def __call__(self, func):
        name = self.name or func.__name__
        registry.register(name, self.regex, func)
        return func
    





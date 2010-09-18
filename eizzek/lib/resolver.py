from eizzek.lib.registry import registry

class PluginResolver(object):

    def resolve(self, string):
        for name, (regex, func) in registry.plugins.items():
            match = regex.match(string)
            if match: break
        else:
            raise LookupError(u"Plugin not found")

        kwargs = self._clear_kwargs(match.groupdict())
        if kwargs:
            return func(**kwargs)
        
        args = self._clear_args(match.groups())
        if args:
            return func(*args)
        
        return func()
    
    def _clear_kwargs(self, kwargs):
        ''' Don't pass parameters where the value is None '''
        for k,v in kwargs.items():
            if v is None:
                del kwargs[k]
        return kwargs
    
    def _clear_args(self, args):
        ''' Don't pass None parameters '''
        return [ arg for arg in args if arg is not None ]


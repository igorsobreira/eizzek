from eizzek.lib.registry import registry

class PluginResolver(object):
    '''
    This has a way to find and call plugins.
    '''
    
    def resolve(self, string):
        '''
        Returns the result of a plugin call. ``string`` is the 
        message body received by the bot.

        Raises ``LookupError`` if the plugin is not found.
        '''
        func, match = self.find(string)

        kwargs = self._clear_kwargs(match.groupdict())
        if kwargs:
            return func(**kwargs)
        
        args = self._clear_args(match.groups())
        if args:
            return func(*args)
        
        return func()
    
    def find(self, string):
        '''
        Returns a tuple: the plugin callable and the match result object. 
        ``string`` is the message body received by the bot.

        Raises ``LookupError`` if the plugin is not found.
        '''
        for name, (regex, func) in registry.plugins.items():
            match = regex.match(string)
            if match: break
        else:
            raise LookupError(u"Plugin not found")
        return func, match

    def _clear_kwargs(self, kwargs):
        ''' Don't pass parameters where the value is None '''
        for k,v in kwargs.items():
            if v is None:
                del kwargs[k]
        return kwargs
    
    def _clear_args(self, args):
        ''' Don't pass None parameters '''
        return [ arg for arg in args if arg is not None ]


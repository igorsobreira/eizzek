from eizzek.lib.registry import registry, session_registry
from eizzek.lib.persistence import session

class PluginResolver(object):
    '''
    The way to find and call plugins.
    '''
    
    def resolve(self, message, connection_data):
        '''
        Returns the result of a plugin call. ``message`` is the 
        message body received by the bot.

        Searches for simple plugins then session plugins. If a simple
        plugin is found just call the callable passing the connection
        dict and arguments from the regex.

        If a session plugin is found verify if the session is
        open, if it is, call the ``handle()`` method of the plugin passing
        the connection dict and the raw message received. 
        If the session is not open yet, open it and call the ``begin()`` method
        passing the connection dict and arguments from the regex.
        
        Raises ``LookupError`` if no plugin is not found.

        '''
        try:
            return self._resolve_simple_plugin(message, connection_data)
        except LookupError:
            return self._resolve_session_plugin(message, connection_data)
    
    def handle_session_plugin(self, message, connection_data):
        '''
        This method is called when a new message arrives and there is
        an open session for the JID.
        '''
        jid = connection_data['message']['from']
        plugin_name = session.get_current(jid)['plugin']
        _, plugin_class = session_registry.plugins[plugin_name]
        plugin = plugin_class()
        return plugin.handle(connection_data, message)
    
    def _resolve_simple_plugin(self, message, connection_data):
        func, match = self.find(message, registry)
        return self._call_function(func, connection_data, match)

    def _resolve_session_plugin(self, message, connection_data):
        klass, match = self.find(message, session_registry)
        plugin = klass()
        jid = connection_data.get('message',{}).get('from', '')

        if session.is_open(jid):
            session.end(jid)

        session.begin(jid, plugin.name)
        return self._call_function(plugin.begin, connection_data, match)

    def find(self, message, registry):
        '''
        Searches for a plugin in ``registry`` trying to match on each 
        regex. If found, returns a tuple (callable_obj, match). Else,
        raises ``LookupError``.
        
        Where ``message`` is the message body received by the bot.
        
        '''
        for name, (regex, callable_obj) in registry.plugins.items():
            match = regex.match(message)
            if match: break
        else:
            raise LookupError(u"Plugin not found")
        return callable_obj, match

    def _call_function(self, function, connection_data, match):
        kwargs = self._clear_kwargs(match.groupdict())
        if kwargs:
            return function(connection_data, **kwargs)
        
        args = self._clear_args(match.groups())
        if args:
            return function(connection_data, *args)

        return function(connection_data)

    def _clear_kwargs(self, kwargs):
        ''' Don't pass parameters where the value is None '''
        for k,v in kwargs.items():
            if v is None:
                del kwargs[k]
        return kwargs
    
    def _clear_args(self, args):
        ''' Don't pass None parameters '''
        return [ arg for arg in args if arg is not None ]


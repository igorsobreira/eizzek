from twisted.internet import defer, protocol, reactor

from eizzek import plugin, registry

@plugin(r'^help ?(?P<plugin>.*)$')
def help(connection, plugin=None):
    '''
    Eizzek help. Usage:

    help [plugin name]
    
    Options:
        -l       list all available plugins
    '''
    deferred = defer.Deferred()
    reactor.callWhenRunning(answer, deferred, plugin=plugin, help=help)
    return deferred

def answer(deferred, plugin, help):
    if not plugin:
        deferred.callback(help.__doc__)
        return
     
    try:
        deferred.callback( OPTIONS[plugin]() )
        return
    except KeyError:
        pass
    
    try:
        _, func = registry.plugins[plugin]
    except KeyError:
        deferred.callback("Plugin not found")
        return
    
    if not func.__doc__:
        deferred.callback("No help found")
        return

    deferred.callback(func.__doc__)

def list_plugins():
    return (u"Available plugins:\n\n %s\n\nType help <plugin name> for more details" %
            "\n ".join(registry.plugins.keys()))

OPTIONS = {
    '-l': list_plugins,
}

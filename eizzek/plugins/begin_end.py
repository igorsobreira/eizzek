from twisted.internet import defer, reactor

from eizzek import plugin, session_registry

@plugin(r'^begin (?P<plugin_name>\w+)$')
def begin(connection, plugin_name):
    '''
    This plugin is used to start a Session with 
    any Session Plugin available.

    '''
    deferred = defer.Deferred()
    reactor.callWhenRunning(do_begin, deferred=deferred, plugin_name=plugin_name)
    return deferred


@plugin(r'^end$')
def end(connection):
    '''
    This plugin is used to finish a Session with 
    the current Session Plugin in use.
    '''
    deferred = defer.Deferred()
    return deferred



def do_begin(deferred, plugin_name):
    try:
        _, plugin = session_registry.plugins[plugin_name]
        deferred.callback(plugin().begin())
    except KeyError:
        deferred.callback(u"Plugin not found")


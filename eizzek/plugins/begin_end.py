from twisted.internet import defer, reactor

from eizzek.lib.decorators import plugin

@plugin(r'^begin (?P<plugin_name>\w+)$')
def begin(plugin_name):
    '''
    This plugin is used to start a Session with 
    any Session Plugin available.

    '''
    deferred = defer.Deferred()
    reactor.callWhenRunning(do_begin, deferred=deferred, plugin_name=plugin_name)
    return deferred


@plugin(r'^end$')
def end():
    '''
    This plugin is used to finish a Session with 
    the current Session Plugin in use.
    '''
    deferred = defer.Deferred()
    return deferred



def do_begin(deferred, plugin_name):
    response = u"'%s' plugin not found" % plugin_name
    deferred.callback(response)


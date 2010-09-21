Eizzek Bot
==========

Eizzek is a simple g-talk bot built on top of [Twisted](http://twistedmatrix.com/) and [Wokkel](http://wokkel.ik.nu/).

To start just execute the command:

    make start

To run tests use:

    make unit
    make functional

Dependencies
------------

 - Twisted
 - Wokkel
 - PyOpenSSL
 - py.test
 - lxml
 - redis

config.py
---------

You need to create a config.py file with some variables:

    JID = 'username@gmail.com/fun'
    PASSWORD = 'secret'
    SERVER = 'talk.google.com'
    PORT = 5222

Plugins
=======

A plugin is a way to make the bot do something.

Simple Plugins
--------------

A simple plugin is just a regex associated with a callabe that returs a ``defer.Deferred`` object. There are examples in eizzek/plugins. The first parameter is a dict with connection data (currenty just the message object).

When a message arrives first regex that matches is called. 

Session Plugin
--------------------

A session plugin works a bit different, the client starts a session using the plugin name:

    client: math
    eizzek: Wellcome to Math plugin

from now on, all the messages are handled by the plugin: 

    client: 3 + 4
    eizzek: 7
    client: 4 * 3 - 10 / 2
    eizzek: 7
    client: end
    eizzek: The Math plugin says goodbye

The API is shown below:
    
    @session_plugin
    class TranslateSessionPlugin(object):
        name = "translate"
        regex = "^translate (?P<from_language>\w+) (?P<to_language>\w+)$"
        
        def begin(self, connection, from_language, to_language):
            # called when the user types the plugin name
            # returns defer.Deferred()

        def handle(self, connection, message):
            # called for every new message, after begin() was called
            # returns defer.Deferred()
        
        def end(self, connection):
            # called when the user types "end"
            # returns defer.Deferred()

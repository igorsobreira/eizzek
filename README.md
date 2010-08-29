Eizzek Bot
==========

Eizzek is a simple g-talk bot built on top of [Twisted](http://twistedmatrix.com/) and [Wokkel](http://wokkel.ik.nu/).

To start just execute the command:

    make start

To run all tests use:

    make test

Dependencies
------------

 - Twisted
 - Wokkel
 - PyOpenSSL
 - Nose
 - lxml


config.py
---------

You need to create a config.py file with some variables:

    JID = 'username@gmail.com/fun'
    PASSWORD = 'secret'
    SERVER = 'talk.google.com'
    PORT = 5222

Plugins
=======

A plugin is a way to make the bot do something. There are (will be) two types of plugins: simple and session plugins.

Simple Plugins
--------------

A simple plugin is just a regex and a function that returns a string. There is an example in plugins/ping.py.

When a message arrives, if any simple plugin regex matches the function will be called. This is already working :)

SessionPlugin (IDEA)
--------------------

A session plugin works a bit different, the client starts a session using the plugin name:

    client: use math
    eizzek: Wellcome to Math plugin
    
from now on, all the messages typed are handled by the plugin: 

    client: 3 + 4
    eizzek: 7
    client: 4 * 3 - 10 / 2
    eizzek: 7
    client: end
    eizzek: The Math plugin says goodbye

The API is shown below:
    
    @session_plugin
    class MathSessionPlugin(object):
        welcome = "Welcome to Math 
        help = "Use +, -, /, *"
        bye = "The Math plugin says goodbye"
        
        def answer(self, message):
            # return a string with your answer

note the use of decorators in classes, it's new in Python 2.6. If you're stuck with an older python version, you can register like this:

    from eizzek.registry import registry

    registry.session_plugin('math', MathSessionPlugin)


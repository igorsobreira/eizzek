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


config.py
---------

You need to create a config.py file with some variables:

    JID = 'username@gmail.com/fun'
    PASSWORD = 'secret'
    SERVER = 'talk.google.com'
    PORT = 5222


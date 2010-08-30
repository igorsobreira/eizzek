from twisted.trial import unittest
from eizzek.plugins.begin_end import begin

class BeginTest(unittest.TestCase):

    def test_begin_plugin_not_found(self):
        def assert_begin(response):
            assert u"'foo' plugin not found" == response

        deferred = begin('foo')
        deferred.addCallback(assert_begin)
        return deferred

